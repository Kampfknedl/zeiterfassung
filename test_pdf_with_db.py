#!/usr/bin/env python
"""Test PDF Export with Real Database Data"""

import os
import sys
import datetime
import traceback
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))

import db
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

print("=" * 60)
print("Testing PDF Export with Database")
print("=" * 60)

# Get database path
db_path = os.path.join(os.path.expanduser('~'), '.kivy', 'stundenerfassung.db')
print(f"Database: {db_path}")
print(f"Exists: {os.path.exists(db_path)}")

# Initialize database
db.init_db(db_path)

# Get customers
customers = db.get_customers(db_path)
print(f"\nCustomers in DB: {customers}")

if not customers:
    print("\n⚠️  No customers found. Creating test data...")
    # Add test customer
    db.add_customer(db_path, "Test Kunde", "Test Adresse", "test@example.com", "0123456789")
    
    # Add test entries
    db.add_entry(db_path, "Test Kunde", "Programmierung", 
                 "2026-01-16", "2026-01-16", 2.5, "Test Entry 1")
    db.add_entry(db_path, "Test Kunde", "Testing",
                 "2026-01-15", "2026-01-15", 3.0, "Test Entry 2")
    db.add_entry(db_path, "Test Kunde", "Dokumentation",
                 "2026-01-14", "2026-01-14", 1.5, "Test Entry 3")
    
    customers = db.get_customers(db_path)
    print(f"Created test customer: {customers}")

# Test PDF export for each customer
for customer in customers:
    print(f"\n--- Testing PDF for: {customer} ---")
    
    rows = db.get_entries(db_path, customer)
    print(f"Entries: {len(rows)}")
    
    if not rows:
        print("  ⚠️  No entries for this customer")
        continue
    
    try:
        out_dir = os.path.expanduser("~/Documents/Zeiterfassung")
        os.makedirs(out_dir, exist_ok=True)
        
        base_name = f"report_{customer.replace(' ', '_')}.pdf"
        file_path = os.path.join(out_dir, base_name)
        
        # Create PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)
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
            if cust[2]:  # address
                info_data.append([Paragraph('<b>Adresse:</b>', styles['Normal']), cust[2]])
            if cust[3]:  # email
                info_data.append([Paragraph('<b>Email:</b>', styles['Normal']), cust[3]])
            if cust[4]:  # phone
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
            
            t = Table(data, colWidths=[3*cm, 10*cm, 3*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E3F2FD')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
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
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(Spacer(1, 1*cm))
        elements.append(total_table)
        
        # Build PDF
        doc.build(elements)
        
        size_kb = os.path.getsize(file_path) / 1024
        print(f"✅ PDF created: {base_name} ({size_kb:.2f} KB)")
        print(f"   Entries: {len(rows)}")
        print(f"   Total Hours: {grand_total:.2f}")
        print(f"   Path: {file_path}")
        
    except Exception as e:
        print(f"❌ PDF Export FAILED for {customer}:")
        print(f"   {str(e)}")
        print(traceback.format_exc())

print("\n" + "=" * 60)
print("✅ PDF Export Test Complete!")
print("=" * 60)
