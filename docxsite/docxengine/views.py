import os
import subprocess
import json
import uuid
from pathlib import Path
from io import BytesIO
from tempfile import NamedTemporaryFile
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from utils.reader import Request_Letter
from django.utils.safestring import mark_safe
from django.conf import settings


def find_libreoffice():
    """Try to find LibreOffice executable on Windows."""
    possible_paths = [
    "/usr/lib/libreoffice/program/soffice", # actual binary
    "/usr/bin/soffice",
    ]
    for path in possible_paths:
        print("DEBUG checking:", path, "exists?", os.path.exists(path))
        if os.path.exists(path):
            return path
    return None


def generate_and_preview(request):
    if request.method == 'POST':
        # Check LibreOffice first
        libreoffice_path = find_libreoffice()
        if not libreoffice_path:
            return render(request, 'error.html', {
                'message': 'LibreOffice is required for PDF generation. Please install LibreOffice from https://www.libreoffice.org/download/ and restart the server.'
            })
        
        # 1. Collect form data
        template       = request.POST.get('template', 'Request_Letter.docx')
        addressee      = request.POST.get('addressee', '')
        adviser        = request.POST.get('adviser', '')
        students       = request.POST.getlist('students')
        course_section = request.POST.get('course_section', '')
        details        = request.POST.get('details', '')
        gender         = request.POST.get('gender', 'Mr.')
        
        # Validate required fields
        if not addressee or not adviser or not students or not course_section or not details:
            return render(request, 'error.html', {'message': 'Please fill in all required fields.'})
        
        # Filter out empty student names
        students = [s.strip() for s in students if s.strip()]
        if not students:
            return render(request, 'error.html', {'message': 'Please add at least one student name.'})

        # 2. Generate DOCX in memory
        try:
            doc = Request_Letter(addressee, adviser, students, course_section, details, gender)
            docx_stream = BytesIO()
            doc.save(docx_stream)
            docx_stream.seek(0)
        except Exception as e:
            return render(request, 'error.html', {'message': f'Document generation failed: {str(e)}'})

        # 3. Write DOCX to temp file
        with NamedTemporaryFile(suffix='.docx', delete=False) as temp_docx:
            temp_docx.write(docx_stream.read())
            temp_docx_path = temp_docx.name

        # 4. Convert to PDF using LibreOffice
        temp_dir = os.path.dirname(temp_docx_path)
        
        try:
            result = subprocess.run([
                libreoffice_path,
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', temp_dir,
                temp_docx_path
            ], check=True, timeout=30, capture_output=True, text=True)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            try:
                os.remove(temp_docx_path)
            except:
                pass
            error_msg = f'PDF conversion failed. Please ensure LibreOffice is properly installed. Error: {str(e)}'
            if hasattr(e, 'stderr') and e.stderr:
                error_msg += f'\nDetails: {e.stderr}'
            return render(request, 'error.html', {'message': error_msg})
        
        # 5. Check if PDF was created (LibreOffice creates it with same base name)
        temp_pdf_path = os.path.splitext(temp_docx_path)[0] + '.pdf'
        
        if not os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_docx_path)
            except:
                pass
            return render(request, 'error.html', {
                'message': f'PDF file was not created at expected location: {temp_pdf_path}. Please check LibreOffice installation.'
            })
        
        # 6. Move PDF to media folder with unique name
        media_dir = settings.MEDIA_ROOT
        os.makedirs(media_dir, exist_ok=True)
        
        unique_filename = f"document_{uuid.uuid4().hex[:8]}.pdf"
        final_pdf_path = os.path.join(media_dir, unique_filename)
        
        # Copy PDF to media folder
        try:
            import shutil
            shutil.copy2(temp_pdf_path, final_pdf_path)
            # Clean up temp files
            os.remove(temp_pdf_path)
        except Exception as e:
            return render(request, 'error.html', {
                'message': f'Failed to save PDF file. Error: {str(e)}'
            })
        
        # Cleanup temp DOCX
        try:
            os.remove(temp_docx_path)
        except Exception:
            pass
        
        # 7. Render preview page
        # Build absolute URL, ensuring we use localhost for iframe compatibility
        pdf_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{unique_filename}")
        pdf_url = pdf_url.replace('0.0.0.0', 'localhost')
        return render(request, 'preview.html', {
            'pdf_url': pdf_url,
            'pdf_filename': unique_filename
        })

    # GET request - show form
    json_path = Path(__file__).resolve().parent.parent / 'utils' / 'resources.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    addresses = data.get("addressees", {})
    names_only = list(addresses.keys())

    return render(request, 'form.html', {
        "addressees_json": mark_safe(json.dumps(names_only))
    })
