"""
Datenbank-Modul für Zeiterfassung
Tabellen: customers (Über-Kunden), entries (Zeiteinträge)
"""
import sqlite3
from datetime import datetime


def get_connection(db_path):
    """Erstelle Datenbankverbindung und Tabellen falls nicht vorhanden."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            hourly_rate REAL DEFAULT 0.0,
            address TEXT,
            email TEXT,
            phone TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            activity TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration_hours REAL NOT NULL,
            comment TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    return conn


def add_customer(db_path, name, hourly_rate=0.0, address="", email="", phone=""):
    """Füge neuen Über-Kunden hinzu."""
    try:
        conn = get_connection(db_path)
        conn.execute(
            "INSERT INTO customers (name, hourly_rate, address, email, phone) VALUES (?, ?, ?, ?, ?)",
            (name, hourly_rate, address, email, phone)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Name bereits vorhanden


def get_all_customers(db_path):
    """Hole alle Über-Kunden."""
    conn = get_connection(db_path)
    cursor = conn.execute("SELECT id, name, hourly_rate, address, email, phone FROM customers ORDER BY name")
    customers = cursor.fetchall()
    conn.close()
    return customers


def get_customer_by_name(db_path, name):
    """Hole Über-Kunden anhand Name."""
    conn = get_connection(db_path)
    cursor = conn.execute(
        "SELECT id, name, hourly_rate, address, email, phone FROM customers WHERE name = ?",
        (name,)
    )
    customer = cursor.fetchone()
    conn.close()
    return customer


def update_customer(db_path, customer_id, name, hourly_rate, address, email, phone):
    """Aktualisiere Über-Kunden."""
    try:
        conn = get_connection(db_path)
        conn.execute(
            "UPDATE customers SET name=?, hourly_rate=?, address=?, email=?, phone=? WHERE id=?",
            (name, hourly_rate, address, email, phone, customer_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def delete_customer(db_path, customer_id):
    """Lösche Über-Kunden (inkl. aller Einträge durch CASCADE)."""
    conn = get_connection(db_path)
    conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()


def add_entry(db_path, customer_id, activity, start_time, end_time, duration_hours, comment=""):
    """Füge Zeiteintrag hinzu."""
    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO entries (customer_id, activity, start_time, end_time, duration_hours, comment) VALUES (?, ?, ?, ?, ?, ?)",
        (customer_id, activity, start_time, end_time, duration_hours, comment)
    )
    conn.commit()
    conn.close()


def get_entries_by_customer(db_path, customer_id):
    """Hole alle Einträge für einen Über-Kunden."""
    conn = get_connection(db_path)
    cursor = conn.execute(
        "SELECT id, activity, start_time, end_time, duration_hours, comment FROM entries WHERE customer_id = ? ORDER BY start_time DESC",
        (customer_id,)
    )
    entries = cursor.fetchall()
    conn.close()
    return entries


def get_all_entries(db_path):
    """Hole alle Einträge (für Übersicht)."""
    conn = get_connection(db_path)
    cursor = conn.execute(
        "SELECT e.id, c.name, e.activity, e.start_time, e.end_time, e.duration_hours, e.comment FROM entries e JOIN customers c ON e.customer_id = c.id ORDER BY e.start_time DESC"
    )
    entries = cursor.fetchall()
    conn.close()
    return entries


def delete_entry(db_path, entry_id):
    """Lösche Zeiteintrag."""
    conn = get_connection(db_path)
    conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def get_recent_activities(db_path, customer_id=None, limit=10):
    """Hole häufigste Aktivitäten für Autocomplete."""
    conn = get_connection(db_path)
    if customer_id:
        cursor = conn.execute(
            "SELECT activity, COUNT(*) as cnt FROM entries WHERE customer_id = ? GROUP BY activity ORDER BY cnt DESC LIMIT ?",
            (customer_id, limit)
        )
    else:
        cursor = conn.execute(
            "SELECT activity, COUNT(*) as cnt FROM entries GROUP BY activity ORDER BY cnt DESC LIMIT ?",
            (limit,)
        )
    activities = [row[0] for row in cursor.fetchall()]
    conn.close()
    return activities

