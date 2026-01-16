#!/usr/bin/env python
"""Quick test script to simulate export flow and capture logs."""
import os
import sys
import datetime
from collections import defaultdict

# Setup Python path
sys.path.insert(0, os.path.dirname(__file__))
import db

# Test database path
test_db_path = os.path.join(os.path.expanduser('~'), 'test_zeiterfassung.db')

print("[TEST] Initializing database...")
db.init_db(test_db_path)

print("[TEST] Adding test customer...")
db.add_customer(test_db_path, 'TestKunde')
db.update_customer(test_db_path, 'TestKunde', 'Test Adresse', 'test@example.com', '123456')

print("[TEST] Adding test entries...")
db.add_entry(test_db_path, 'TestKunde', 'Entwicklung', datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat(), 4.5)
db.add_entry(test_db_path, 'TestKunde', 'Testing', datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat(), 2.0)

print("[TEST] Retrieving entries...")
entries = db.get_entries(test_db_path, 'TestKunde')
print(f"[TEST] Found {len(entries)} entries:")
for r in entries:
    print(f"  {r}")

print("\n[TEST] Simulating CSV export...")
export_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'Zeiterfassung_Test')
os.makedirs(export_dir, exist_ok=True)
print(f"[TEST] Export directory: {export_dir}")
print(f"[TEST] Export directory exists: {os.path.exists(export_dir)}")
print(f"[TEST] Export directory is writable: {os.access(export_dir, os.W_OK)}")

# Simulate CSV creation
import csv
customer_name = 'TestKunde'
csv_path = os.path.join(export_dir, f"report_{customer_name}.csv")
print(f"\n[TEST] CSV path: {csv_path}")

try:
    months_data = defaultdict(list)
    for r in entries:
        date_str = (r[3] or '')[:10]
        month_key = date_str[:7] if date_str else 'Undatiert'
        months_data[month_key].append(r)
    
    sorted_months = sorted(months_data.keys(), reverse=True)
    grand_total = 0.0
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Zeiterfassung', customer_name])
        writer.writerow([])
        writer.writerow([f'Erstellt am: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'])
        
        cust = db.get_customer(test_db_path, customer_name)
        if cust and len(cust) > 2 and cust[2]:
            writer.writerow([f'Adresse: {cust[2]}'])
        
        writer.writerow([])
        writer.writerow(['Datum', 'Tätigkeit', 'Stunden'])
        
        for month_key in sorted_months:
            rows_in_month = months_data[month_key]
            month_total = 0.0
            writer.writerow([f'Monat: {month_key}'])
            
            for r in rows_in_month:
                date = (r[3] or '')[:10]
                act = r[2] or ''
                hrs = float(r[5] or 0)
                writer.writerow([date, act, f'{hrs:.2f}'])
                month_total += hrs
            
            writer.writerow(['', f'Monatssumme {month_key}:', f'{month_total:.2f}'])
            writer.writerow([])
            grand_total += month_total
        
        writer.writerow(['Gesamtstunden', f'{grand_total:.2f}'])
    
    if os.path.exists(csv_path):
        file_size = os.path.getsize(csv_path)
        print(f"[TEST] ✅ CSV created! Size: {file_size} bytes")
        print(f"[TEST] CSV contents (first 500 chars):")
        with open(csv_path, 'r', encoding='utf-8') as f:
            print(f.read()[:500])
    else:
        print(f"[TEST] ❌ CSV file not created")
        
except Exception as e:
    import traceback
    print(f"[TEST] ❌ CSV creation failed: {e}")
    print(traceback.format_exc())

# Clean up
if os.path.exists(test_db_path):
    os.remove(test_db_path)
    print(f"\n[TEST] Cleaned up test database")
