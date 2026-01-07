# Test Script - PDF Export Demo
# Erstellt Test-Daten und generiert PDF zum Testen

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from collections import defaultdict

def create_test_database():
    """Create test data"""
    db_path = 'test_zeiterfassung.db'
    
    # Initialize DB
    db.init_db(db_path)
    
    # Add test customer
    test_customer = "Acme Corporation"
    db.add_customer(db_path, test_customer)
    db.update_customer(db_path, test_customer,
                      address="Industriestraße 42, 12345 Berlin",
                      email="contact@acme.corp",
                      phone="+49 30 12345678")
    
    # Add test entries for current month and previous month
    today = datetime.date.today()
    
    # Previous month entries
    for day in range(1, 26):
        prev_month = today.replace(day=1) - datetime.timedelta(days=1)
        entry_date = prev_month.replace(day=day)
        db.add_entry(db_path, test_customer, 
                    f"Activity Day {day}", 
                    entry_date.isoformat(), 
                    entry_date.isoformat(),
                    5.0 + (day % 3))
    
    # Current month entries
    for day in range(1, 8):
        entry_date = today.replace(day=day)
        db.add_entry(db_path, test_customer,
                    f"Development Task {day}",
                    entry_date.isoformat(),
                    entry_date.isoformat(),
                    6.0 + (day % 4))
    
    print(f"✓ Test database created: {db_path}")
    return db_path

def generate_test_pdf(db_path, output_path="test_report.pdf"):
    """Generate test PDF"""
    
    customer = "Acme Corporation"
    rows = db.get_entries(db_path, customer)
    
    if not rows:
        print("✗ No entries found")
        return
    
    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
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
    elements.append(Paragraph(f"Zeiterfassung - {customer}", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Customer info
    cust = db.get_customer(db_path, customer)
    info_data = []
    info_data.append([Paragraph('<b>Kunde:</b>', styles['Normal']), customer])
    info_data.append([Paragraph('<b>Datum:</b>', styles['Normal']), 
                    datetime.datetime.now().strftime('%d.%m.%Y')])
    
    if cust:
        if cust[2]:
            info_data.append([Paragraph('<b>Adresse:</b>', styles['Normal']), cust[2]])
        if cust[3]:
            info_data.append([Paragraph('<b>Email:</b>', styles['Normal']), cust[3]])
        if cust[4]:
            info_data.append([Paragraph('<b>Telefon:</b>', styles['Normal']), cust[4]])
    
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 1*cm))
    
    # Group by month
    months_data = defaultdict(list)
    for r in rows:
        date_str = (r[3] or '')[:10]
        month_key = date_str[:7] if date_str else "Undatiert"
        months_data[month_key].append(r)
    
    sorted_months = sorted(months_data.keys(), reverse=True)
    grand_total = 0.0
    
    # Create table for each month
    for month_key in sorted_months:
        month_style = ParagraphStyle(
            'MonthHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1976D2'),
            spaceAfter=10,
        )
        elements.append(Paragraph(f"Monat: {month_key}", month_style))
        
        # Table data
        data = [['Datum', 'Tätigkeit', 'Stunden']]
        rows_in_month = months_data[month_key]
        month_total = 0.0
        
        for r in rows_in_month:
            date = (r[3] or '')[:10]
            act = r[2] or ''
            hrs = float(r[5] or 0)
            data.append([date, act, f"{hrs:.2f}"])
            month_total += hrs
        
        # Month total
        data.append(['', Paragraph('<b>Monatssumme</b>', styles['Normal']), 
                   Paragraph(f'<b>{month_total:.2f}</b>', styles['Normal'])])
        
        # Create table
        t = Table(data, colWidths=[3*cm, 10*cm, 3*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E3F2FD')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 0.5*cm))
        grand_total += month_total
    
    # Grand total
    total_data = [[
        Paragraph('<b>Gesamtstunden:</b>', styles['Heading3']),
        Paragraph(f'<b>{grand_total:.2f} Std</b>', styles['Heading3'])
    ]]
    total_table = Table(total_data, colWidths=[10*cm, 6*cm])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(Spacer(1, 1*cm))
    elements.append(total_table)
    
    # Build PDF
    doc.build(elements)
    
    print(f"✓ PDF generated: {output_path}")
    return output_path

def main():
    print("\n" + "="*50)
    print("PDF EXPORT TEST")
    print("="*50 + "\n")
    
    # Create test database
    db_path = create_test_database()
    
    # Generate PDF
    pdf_path = generate_test_pdf(db_path, "test_report.pdf")
    
    print("\n" + "="*50)
    print("✓ Test completed successfully!")
    print("="*50)
    print("\nGenerated files:")
    print(f"  - Database: test_zeiterfassung.db")
    print(f"  - PDF Report: test_report.pdf")
    print("\nOpen 'test_report.pdf' to see the result!")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
