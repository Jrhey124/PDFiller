#!/usr/bin/env python
"""
Quick test script to verify all components work correctly
"""
import os
import sys
import json

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("TESTING DOCUMENT GENERATOR COMPONENTS")
print("=" * 60)

# Test 1: Check resources.json
print("\n[TEST 1] Checking resources.json...")
try:
    from pathlib import Path
    json_path = Path(__file__).parent / 'utils' / 'resources.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    addressees = data.get("addressees", {})
    print(f"✓ Found {len(addressees)} addressees")
    for name in addressees:
        print(f"  - {name}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Check template file
print("\n[TEST 2] Checking template file...")
try:
    template_path = Path(__file__).parent / 'utils' / 'Templates' / 'ORIGINAL FORMAT of Request Letter (026).docx'
    if template_path.exists():
        print(f"✓ Template found: {template_path}")
    else:
        print(f"✗ Template NOT found: {template_path}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Check python-docx
print("\n[TEST 3] Checking python-docx module...")
try:
    from docx import Document
    print("✓ python-docx is installed")
except ImportError:
    print("✗ python-docx is NOT installed")
    print("  Run: pip install python-docx")

# Test 4: Check LibreOffice
print("\n[TEST 4] Checking LibreOffice...")
libreoffice_paths = [
    r'C:\Program Files\LibreOffice\program\soffice.exe',
    r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
]
found = False
for path in libreoffice_paths:
    if os.path.exists(path):
        print(f"✓ LibreOffice found: {path}")
        found = True
        break
if not found:
    print("⚠ LibreOffice NOT found (PDF generation will fallback to DOCX)")
    print("  Download from: https://www.libreoffice.org/download/")

# Test 5: Test document generation
print("\n[TEST 5] Testing document generation...")
try:
    from utils.reader import Request_Letter
    doc = Request_Letter(
        addressee="Dr. Maria C. Santos",
        adviser="Test Adviser",
        students=["Student 1", "Student 2"],
        course_section="TEST 101",
        details="Test details",
        gender="Mr."
    )
    print("✓ Document generation successful")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 6: Check Django settings
print("\n[TEST 6] Checking Django configuration...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docxsite.settings')
    import django
    django.setup()
    from django.conf import settings
    print(f"✓ DEBUG = {settings.DEBUG}")
    print(f"✓ ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
