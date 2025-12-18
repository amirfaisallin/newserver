from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime
import sqlite3
import secrets
import hashlib
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
CORS(app)


# Database setup
DB_NAME = 'license_management.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Admin users table
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    # Licenses table
    c.execute('''CREATE TABLE IF NOT EXISTS licenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  amount REAL NOT NULL,
                  license_key TEXT UNIQUE NOT NULL,
                  is_active INTEGER DEFAULT 1,
                  is_blocked INTEGER DEFAULT 0,
                  created_at TEXT NOT NULL)''')
    
    # Active devices table
    c.execute('''CREATE TABLE IF NOT EXISTS active_devices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  license_key TEXT NOT NULL,
                  device_id TEXT NOT NULL,
                  device_name TEXT,
                  last_active TEXT NOT NULL,
                  FOREIGN KEY (license_key) REFERENCES licenses(license_key))''')
    
    # Create default admin if not exists
    default_password = hashlib.sha256('admin123'.encode()).hexdigest()
    c.execute('INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)',
              ('admin', default_password))
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'admin_logged_in' in session:
        return render_template('admin.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ? AND password = ?',
                            (username, password_hash)).fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/license/generate', methods=['POST'])
@login_required
def generate_license_key():
    """Generate a random license key"""
    license_key = secrets.token_urlsafe(16).upper()[:12]
    return jsonify({'license_key': license_key})

@app.route('/api/license/create', methods=['POST'])
@login_required
def create_license():
    data = request.get_json()
    username = data.get('username')
    amount = data.get('amount', 0)
    license_key = data.get('license_key')
    
    if not username or not license_key:
        return jsonify({'error': 'Username and license key are required'}), 400
    
    conn = get_db_connection()
    
    # Check if license key already exists
    existing = conn.execute('SELECT * FROM licenses WHERE license_key = ?',
                           (license_key,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'License key already exists'}), 400
    
    created_at = datetime.now().isoformat()
    
    try:
        cursor = conn.execute('''INSERT INTO licenses (username, amount, license_key, is_active, is_blocked, created_at)
                       VALUES (?, ?, ?, 1, 0, ?)''',
                    (username, amount, license_key, created_at))
        conn.commit()
        license_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'License created successfully',
            'license_id': license_id
        })
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/license/list', methods=['GET'])
@login_required
def list_licenses():
    search = request.args.get('search', '').strip()
    
    conn = get_db_connection()
    
    if search:
        query = '''SELECT l.*, 
                          COUNT(DISTINCT ad.id) as device_count
                   FROM licenses l
                   LEFT JOIN active_devices ad ON l.license_key = ad.license_key
                   WHERE l.username LIKE ? OR l.license_key LIKE ?
                   GROUP BY l.id
                   ORDER BY l.created_at DESC'''
        licenses = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        query = '''SELECT l.*, 
                          COUNT(DISTINCT ad.id) as device_count
                   FROM licenses l
                   LEFT JOIN active_devices ad ON l.license_key = ad.license_key
                   GROUP BY l.id
                   ORDER BY l.created_at DESC'''
        licenses = conn.execute(query).fetchall()
    
    result = []
    for license in licenses:
        result.append({
            'id': license['id'],
            'username': license['username'],
            'amount': license['amount'],
            'license_key': license['license_key'],
            'is_active': bool(license['is_active']),
            'is_blocked': bool(license['is_blocked']),
            'device_count': license['device_count'],
            'created_at': license['created_at']
        })
    
    conn.close()
    return jsonify({'licenses': result})

@app.route('/api/license/<int:license_id>/block', methods=['POST'])
@login_required
def block_license(license_id):
    conn = get_db_connection()
    conn.execute('UPDATE licenses SET is_blocked = 1 WHERE id = ?', (license_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'License blocked successfully'})

@app.route('/api/license/<int:license_id>/unblock', methods=['POST'])
@login_required
def unblock_license(license_id):
    conn = get_db_connection()
    conn.execute('UPDATE licenses SET is_blocked = 0 WHERE id = ?', (license_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'License unblocked successfully'})

@app.route('/api/license/<int:license_id>/delete', methods=['DELETE'])
@login_required
def delete_license(license_id):
    conn = get_db_connection()
    
    # Get license key before deleting
    license = conn.execute('SELECT license_key FROM licenses WHERE id = ?',
                          (license_id,)).fetchone()
    
    if not license:
        conn.close()
        return jsonify({'error': 'License not found'}), 404
    
    # Delete associated devices
    conn.execute('DELETE FROM active_devices WHERE license_key = ?',
                (license['license_key'],))
    
    # Delete license
    conn.execute('DELETE FROM licenses WHERE id = ?', (license_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'License deleted successfully'})

@app.route('/api/license/<int:license_id>/devices', methods=['GET'])
@login_required
def get_license_devices(license_id):
    conn = get_db_connection()
    
    license = conn.execute('SELECT license_key FROM licenses WHERE id = ?',
                          (license_id,)).fetchone()
    
    if not license:
        conn.close()
        return jsonify({'error': 'License not found'}), 404
    
    devices = conn.execute('''SELECT * FROM active_devices 
                             WHERE license_key = ? 
                             ORDER BY last_active DESC''',
                          (license['license_key'],)).fetchall()
    
    result = []
    for device in devices:
        result.append({
            'id': device['id'],
            'device_id': device['device_id'],
            'device_name': device['device_name'],
            'last_active': device['last_active']
        })
    
    conn.close()
    return jsonify({'devices': result})

# User API endpoints (for client applications)
@app.route('/api/user/validate', methods=['POST'])
def validate_license():
    """Validate license for user applications"""
    data = request.get_json()
    license_key = data.get('license_key')
    device_id = data.get('device_id')
    device_name = data.get('device_name', 'Unknown Device')
    
    if not license_key or not device_id:
        return jsonify({'error': 'License key and device ID are required'}), 400
    
    conn = get_db_connection()
    
    license = conn.execute('''SELECT * FROM licenses 
                             WHERE license_key = ?''',
                          (license_key,)).fetchone()
    
    if not license:
        conn.close()
        return jsonify({'valid': False, 'message': 'Invalid license key'}), 404
    
    if license['is_blocked']:
        conn.close()
        return jsonify({'valid': False, 'message': 'License is blocked'}), 403
    
    if not license['is_active']:
        conn.close()
        return jsonify({'valid': False, 'message': 'License is inactive'}), 403
    
    # Update or insert device
    existing_device = conn.execute('''SELECT * FROM active_devices 
                                     WHERE license_key = ? AND device_id = ?''',
                                  (license_key, device_id)).fetchone()
    
    last_active = datetime.now().isoformat()
    
    if existing_device:
        conn.execute('''UPDATE active_devices 
                       SET last_active = ?, device_name = ?
                       WHERE license_key = ? AND device_id = ?''',
                    (last_active, device_name, license_key, device_id))
    else:
        conn.execute('''INSERT INTO active_devices (license_key, device_id, device_name, last_active)
                       VALUES (?, ?, ?, ?)''',
                    (license_key, device_id, device_name, last_active))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'valid': True,
        'username': license['username'],
        'amount': license['amount'],
        'message': 'License validated successfully'
    })

@app.route('/api/user/check', methods=['POST'])
def check_license():
    """Quick check if license is valid (without updating device)"""
    data = request.get_json()
    license_key = data.get('license_key')
    
    if not license_key:
        return jsonify({'error': 'License key is required'}), 400
    
    conn = get_db_connection()
    license = conn.execute('''SELECT * FROM licenses 
                             WHERE license_key = ?''',
                          (license_key,)).fetchone()
    conn.close()
    
    if not license:
        return jsonify({'valid': False, 'message': 'Invalid license key'}), 404
    
    if license['is_blocked']:
        return jsonify({'valid': False, 'message': 'License is blocked'}), 403
    
    if not license['is_active']:
        return jsonify({'valid': False, 'message': 'License is inactive'}), 403
    
    return jsonify({
        'valid': True,
        'username': license['username'],
        'amount': license['amount']
    })

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
