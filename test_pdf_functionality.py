#!/usr/bin/env python
"""Test PDF Export Functionality"""

import os
import sys
import datetime
import traceback

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Test imports
print("=" * 50)
print("Testing PDF Export Dependencies")
print("=" * 50)

# Test reportlab
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    print("✅ ReportLab: OK")
except ImportError as e:
    print(f"❌ ReportLab: FAILED - {e}")
    sys.exit(1)

# Test db module
try:
    import db
    print("✅ DB Module: OK")
except ImportError as e:
    print(f"❌ DB Module: FAILED - {e}")
    sys.exit(1)

print("")
print("=" * 50)
print("Testing PDF Generation")
print("=" * 50)

# Create test PDF
try:
    # Get temp directory
    out_dir = os.path.expanduser("~/Documents/Zeiterfassung")
    os.makedirs(out_dir, exist_ok=True)
    
    test_pdf = os.path.join(out_dir, "test_export.pdf")
    
    # Create PDF document
    doc = SimpleDocTemplate(test_pdf, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=30,
    )
    elements.append(Paragraph("Test PDF Export", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Test table
    data = [
        ['Datum', 'Tätigkeit', 'Stunden'],
        ['2026-01-16', 'Programmierung', '2.5'],
        ['2026-01-15', 'Testing', '3.0'],
        ['2026-01-14', 'Documentation', '1.5'],
    ]
    
    t = Table(data, colWidths=[3*cm, 10*cm, 3*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 1*cm))
    
    # Total
    total_data = [[
        Paragraph('<b>Gesamtstunden:</b>', styles['Heading3']),
        Paragraph(f'<b>7.0 Std</b>', styles['Heading3'])
    ]]
    total_table = Table(total_data, colWidths=[10*cm, 6*cm])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(total_table)
    
    # Build PDF
    doc.build(elements)
    
    print(f"✅ PDF Created: {test_pdf}")
    print(f"   Size: {os.path.getsize(test_pdf) / 1024:.2f} KB")
    
except Exception as e:
    print(f"❌ PDF Generation FAILED:")
    print(f"   Error: {str(e)}")
    print(f"   Traceback: {traceback.format_exc()}")
    sys.exit(1)

print("")
print("=" * 50)
print("✅ All Tests Passed!")
print("=" * 50)
