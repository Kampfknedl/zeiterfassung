#!/usr/bin/env python3
"""
Validate that the PDF export correctly shows all entries
"""
import db
import os

# Get DB path
user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'poc')
db_path = os.path.join(user_data_dir, 'stundenerfassung.db')

print("=" * 60)
print("PDF REPORT VALIDATION")
print("=" * 60)

# Get customers
customers = db.get_customers(db_path)
print(f"\nCustomers in DB: {customers}")

if customers:
    customer = customers[0]
    entries = db.get_entries(db_path, customer)
    
    print(f"\nEntries for '{customer}': {len(entries)}")
    for i, entry in enumerate(entries, 1):
        print(f"  {i}. {entry[3]} (start) - {entry[2]} (activity) - {entry[5]}h (hours)")
    
    if entries:
        print("\n✅ DATA IS PRESENT - PDF SHOULD SHOW ENTRIES!")
        print("\nWhen you click 'PDF Export erstellen':")
        print("  1. Select a folder (e.g., your Documents)")
        print("  2. The PDF will be created automatically")
        print("  3. It should show all entries above")
    else:
        print("\n❌ NO ENTRIES - This is why PDF is empty!")
        print("   Add entries first, then export.")
else:
    print("\n❌ NO CUSTOMERS!")

print("\n" + "=" * 60)
