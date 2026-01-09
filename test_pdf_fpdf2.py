"""Test PDF generation with fpdf2"""
from fpdf import FPDF
import datetime

# Create simple test PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'Test PDF - Zeiterfassung', ln=True, align='C')
pdf.ln(5)

pdf.set_font('Helvetica', '', 10)
pdf.cell(0, 6, f'Erstellt: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}', ln=True)
pdf.ln(5)

# Table
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(35, 8, 'Datum', border=1)
pdf.cell(110, 8, 'Tätigkeit', border=1)
pdf.cell(30, 8, 'Stunden', border=1, align='R')
pdf.ln()

pdf.set_font('Helvetica', '', 9)
pdf.cell(35, 6, '08.01.2026', border=1)
pdf.cell(110, 6, 'Programmierung', border=1)
pdf.cell(30, 6, '2.50', border=1, align='R')
pdf.ln()

pdf.output('test_fpdf2_output.pdf')
print("✅ PDF erfolgreich erstellt: test_fpdf2_output.pdf")
