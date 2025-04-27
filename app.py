from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os
import uuid
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

USERS_FILE = 'users.json'
KEYS_FILE = 'keys.json'

app.config['ADMIN_PASSWORD'] = 'admin123'


def init_db():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(KEYS_FILE):
        sample_keys = [
            {"key": generate_key_string('1month'), "tier": '1month', "used": False},
        ]
        with open(KEYS_FILE, 'w') as f:
            json.dump(sample_keys, f)

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_keys():
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def is_logged_in():
    return 'user_id' in session

def has_active_subscription(user):
    if 'subscription_end' in user:
        return datetime.strptime(user['subscription_end'], '%Y-%m-%d') > datetime.now()
    return False

def get_current_user():
    if is_logged_in():
        users = load_users()
        for user in users:
            if user['id'] == session['user_id']:
                return user
    return None

@app.route('/')
def index():
    return render_template('index.html', user=get_current_user())

def generate_key_string(tier): # Format: TIER-XXXX-XXXX-XXXX
    return f"{tier.upper()}-{uuid4().hex[:4].upper()}-{uuid4().hex[:4].upper()}-{uuid4().hex[:4].upper()}"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_authenticated = session.get('admin', False)
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'login':
            password = request.form.get('password')
            if password == app.config['ADMIN_PASSWORD']:
                session['admin'] = True
                admin_authenticated = True
                flash('Admin login successful', 'success')
            else:
                flash('Invalid admin password', 'error')
                return render_template('admin.html', admin_authenticated=False, keys=[])
        
        elif form_type == 'action':
            if not admin_authenticated:
                flash('Please login as admin first', 'error')
                return redirect(url_for('admin'))
            
            action = request.form.get('action')
            keys = load_keys()
            
            if action == 'generate':
                tier = request.form.get('tier')
                new_key = generate_key_string(tier)
                new_key_data = {"key": new_key, "tier": tier, "used": False}
                keys.append(new_key_data)
                save_keys(keys)
                flash(f'Key {new_key} generated', 'success')
            
            elif action == 'delete':
                key_value = request.form.get('key_value')
                new_keys = [k for k in keys if k['key'] != key_value]
                if len(new_keys) == len(keys):
                    flash(f'Key {key_value} not found', 'error')
                else:
                    save_keys(new_keys)
                    flash(f'Key {key_value} deleted', 'success')
        
        keys = load_keys() if admin_authenticated else []
        return render_template('admin.html', admin_authenticated=admin_authenticated, keys=keys)
    
    # GET request
    if admin_authenticated:
        keys = load_keys()
        return render_template('admin.html', admin_authenticated=True, keys=keys)
    else:
        return render_template('admin.html', admin_authenticated=False, keys=[])
        
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Admin logged out', 'success')
    return redirect(url_for('admin'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'register':
            # Handle registration
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            users = load_users()
            
            # Check if user exists
            if any(u['email'] == email for u in users):
                flash('Email already registered', 'error')
                return redirect(url_for('auth'))
            
            # Create new user
            new_user = {
                'id': str(uuid.uuid4()),
                'username': username,
                'email': email,
                'password': generate_password_hash(password),
                'tier': 'free',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'subscription_end': None
            }
            
            users.append(new_user)
            save_users(users)
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth'))
        
        elif action == 'login':
            # Handle login
            email = request.form.get('email')
            password = request.form.get('password')
            
            users = load_users()
            user = next((u for u in users if u['email'] == email), None)
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
                return redirect(url_for('auth'))
    
    return render_template('auth.html', user=get_current_user())

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please login to access the dashboard', 'error')
        return redirect(url_for('auth'))
    
    user = get_current_user()
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/redeem_key', methods=['POST'])
def redeem_key():
    if not is_logged_in():
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    key = request.form.get('key')
    keys = load_keys()
    users = load_users()
    
    # Find the key
    key_data = next((k for k in keys if k['key'] == key and not k['used']), None)
    
    if not key_data:
        return jsonify({'success': False, 'message': 'Invalid or already used key'}), 400
    
    # Find current user
    user_index = next((i for i, u in enumerate(users) if u['id'] == session['user_id']), None)
    if user_index is None:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    user = users[user_index]
    
    # Calculate subscription end date
    today = datetime.now()
    if key_data['tier'] == '1month':
        end_date = today + timedelta(days=30)
    elif key_data['tier'] == '3month':
        end_date = today + timedelta(days=90)
    elif key_data['tier'] == '12month':
        end_date = today + timedelta(days=365)
    else:
        return jsonify({'success': False, 'message': 'Invalid key tier'}), 400
    
    # Update user
    user['tier'] = key_data['tier']
    user['subscription_end'] = end_date.strftime('%Y-%m-%d')
    
    # Mark key as used
    key_data['used'] = True
    key_data['used_by'] = user['id']
    key_data['used_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_users(users)
    save_keys(keys)
    
    return jsonify({
        'success': True,
        'message': f'Key redeemed! Your account is now {key_data["tier"]} tier until {end_date.strftime("%Y-%m-%d")}',
        'tier': key_data['tier'],
        'subscription_end': user['subscription_end']
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)