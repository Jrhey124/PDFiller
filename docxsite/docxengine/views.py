import os
import subprocess
import json
from pathlib import Path
from io import BytesIO
from tempfile import NamedTemporaryFile
from django.shortcuts import render
from django.http import FileResponse
from utils.reader import Request_Letter
from django.utils.safestring import mark_safe


def generate_and_preview(request):
    if request.method == 'POST':
        # 1. Collect form data
        addressee      = request.POST['addressee']
        adviser        = request.POST['adviser']
        students       = request.POST.getlist('students')
        course_section = request.POST['course_section']
        details        = request.POST['details']
        gender         = request.POST['gender']

        # 2. Generate DOCX in memory
        doc = Request_Letter(addressee, adviser, students, course_section, details, gender)
        docx_stream = BytesIO()
        doc.save(docx_stream)
        docx_stream.seek(0)

        # 3. Write DOCX to temp file
        with NamedTemporaryFile(suffix='.docx', delete=False) as temp_docx:
            temp_docx.write(docx_stream.read())
            temp_docx_path = temp_docx.name

        # 4. Convert to PDF using LibreOffice
        temp_pdf_path = temp_docx_path.replace('.docx', '.pdf')
        try:
            subprocess.run([
                r'C:\Program Files\LibreOffice\program\soffice.exe',  # adjust path
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(temp_pdf_path),
                temp_docx_path
            ], check=True)
        except subprocess.CalledProcessError:
            os.remove(temp_docx_path)
            return render(request, 'error.html', {'message': 'PDF conversion failed.'})

        # 5. Serve PDF and clean up
        if os.path.exists(temp_pdf_path):
            f = open(temp_pdf_path, 'rb')  # Keep file open
            response = FileResponse(f, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="preview.pdf"'

            # Attach cleanup to response.close
            def cleanup():
                try:
                    f.close()
                    os.remove(temp_docx_path)
                    os.remove(temp_pdf_path)
                except Exception:
                    pass

            response.close = cleanup
            return response
        else:
            os.remove(temp_docx_path)
            return render(request, 'error.html', {'message': 'PDF file not found.'})


    json_path = Path(__file__).resolve().parent.parent / 'utils' / 'resources.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    addresses = data.get("addressees", {})
    names_only = list(addresses.keys())  # ✅ Extract just the names

    return render(request, 'form.html', {
        "addressees_json": mark_safe(json.dumps(names_only))
    })
