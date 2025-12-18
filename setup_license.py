"""
Quick script to setup the license key YQ8EJR4LTBSM in the database
"""
import sqlite3
from datetime import datetime

DB_NAME = 'license_management.db'

def setup_license():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    license_key = "YQ8EJR4LTBSM"
    
    # Check if license exists
    existing = c.execute('SELECT * FROM licenses WHERE license_key = ?', 
                        (license_key,)).fetchone()
    
    if existing:
        print(f"[OK] License key {license_key} already exists!")
        print(f"   Username: {existing[1]}")
        print(f"   Amount: {existing[2]}")
        print(f"   Status: {'Active' if existing[4] else 'Inactive'}")
        print(f"   Blocked: {'Yes' if existing[5] else 'No'}")
    else:
        # Create license
        created_at = datetime.now().isoformat()
        c.execute('''INSERT INTO licenses (username, amount, license_key, is_active, is_blocked, created_at)
                     VALUES (?, ?, ?, 1, 0, ?)''',
                 ('demo_user', 100.0, license_key, created_at))
        conn.commit()
        print(f"[OK] License key {license_key} created successfully!")
        print(f"   Username: demo_user")
        print(f"   Amount: 100.0")
        print(f"   Status: Active")
    
    conn.close()

if __name__ == '__main__':
    setup_license()

