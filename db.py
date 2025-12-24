import sqlite3
from pathlib import Path

SCHEMA = '''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    address TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    activity TEXT,
    start TEXT,
    end TEXT,
    duration_hours REAL,
    notes TEXT
);
'''


def init_db(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()


def get_connection(path):
    return sqlite3.connect(path)


def get_customers(path):
    conn = get_connection(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM customers ORDER BY name")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def add_customer(path, name):
    conn = get_connection(path)
    try:
        conn.execute("INSERT INTO customers (name, address, email, phone) VALUES (?, ?, ?, ?)", (name, '', '', ''))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def get_customer(path, name):
    conn = get_connection(path)
    cur = conn.cursor()
    cur.execute("SELECT id, name, address, email, phone FROM customers WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row


def update_customer(path, name, address='', email='', phone=''):
    conn = get_connection(path)
    try:
        conn.execute("UPDATE customers SET address = ?, email = ?, phone = ? WHERE name = ?", (address, email, phone, name))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def rename_customer(path, old_name, new_name):
    conn = get_connection(path)
    try:
        conn.execute("UPDATE customers SET name = ? WHERE name = ?", (new_name, old_name))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def update_customer_full(path, old_name, new_name=None, address='', email='', phone=''):
    # Optionally rename and update details
    if new_name and new_name != old_name:
        rename_customer(path, old_name, new_name)
        target_name = new_name
    else:
        target_name = old_name
    conn = get_connection(path)
    try:
        conn.execute("UPDATE customers SET address = ?, email = ?, phone = ? WHERE name = ?", (address, email, phone, target_name))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def delete_customer(path, name):
    conn = get_connection(path)
    try:
        conn.execute("DELETE FROM customers WHERE name = ?", (name,))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def add_entry(path, customer, activity, start, end, duration):
    conn = get_connection(path)
    conn.execute("INSERT INTO entries (customer,activity,start,end,duration_hours) VALUES (?,?,?,?,?)",
                 (customer, activity, start, end, duration))
    conn.commit(); conn.close()


def get_entries(path, customer=None):
    conn = get_connection(path)
    cur = conn.cursor()
    if customer and customer != '—':
        cur.execute("SELECT * FROM entries WHERE customer = ? ORDER BY start DESC", (customer,))
    else:
        cur.execute("SELECT * FROM entries ORDER BY start DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_recent_activities(path, prefix=None, limit=10):
    conn = get_connection(path)
    cur = conn.cursor()
    if prefix:
        like = f"{prefix}%"
        cur.execute("SELECT activity, COUNT(*) as c FROM entries WHERE activity LIKE ? GROUP BY activity ORDER BY c DESC LIMIT ?", (like, limit))
    else:
        cur.execute("SELECT activity, COUNT(*) as c FROM entries WHERE activity IS NOT NULL GROUP BY activity ORDER BY c DESC LIMIT ?", (limit,))
    rows = [r[0] for r in cur.fetchall() if r[0]]
    conn.close()
    return rows


def delete_entry(path, entry_id):
    conn = get_connection(path)
    try:
        conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()
