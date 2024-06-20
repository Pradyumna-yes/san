# app/routes.py

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from app import app, mysql, login_manager
from datetime import datetime

# In-memory user store for demonstration purposes
users = {'admin': {'password': 'password'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('page_datatable'))
        else:
            error = 'Invalid credentials, please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('Dashboard.html')

@app.route('/data')
def get_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM stations")
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return jsonify(results)

@app.route('/add-station', methods=['POST'])
def add_station():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1 FROM stations WHERE number = %s", (data['number'],))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Station already exists"}), 409

    last_update = parse_datetime(data.get('last_update'))
    values = (data['number'], data['name'], data['address'], data['position_lat'], data['position_lng'],
              data.get('banking') == 'true', data.get('bonus') == 'true', data.get('status', 'CLOSED'),
              data['contract_name'], data['bike_stands'], data['available_bike_stands'], data['available_bikes'],
              last_update)

    query = """
    INSERT INTO stations (number, name, address, position_lat, position_lng, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
    return jsonify({"message": "Station added successfully"}), 201

@app.route('/edit-station/<int:number>', methods=['PUT'])
def edit_station(number):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    last_update = parse_datetime(data.get('last_update'))
    values = (data['name'], data['address'], data['position_lat'], data['position_lng'],
              data.get('banking') == 'true', data.get('bonus') == 'true', data.get('status', 'CLOSED'),
              data['contract_name'], data['bike_stands'], data['available_bike_stands'], data['available_bikes'],
              last_update, number)

    query = """
    UPDATE stations SET name = %s, address = %s, position_lat = %s, position_lng = %s, 
    banking = %s, bonus = %s, status = %s, contract_name = %s, bike_stands = %s, 
    available_bike_stands = %s, available_bikes = %s, last_update = %s WHERE number = %s
    """
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
    return jsonify({"message": "Station updated successfully"}), 200

@app.route('/delete-station/<int:number>', methods=['DELETE'])
def delete_station(number):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM stations WHERE number = %s", (number,))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
    return jsonify({"message": "Station deleted successfully"}), 200

@app.route('/dashboard')
def page_dashboard():
    return render_template('Dashboard.html')

@app.route('/about')
def page_about():
    return render_template('About.html')

@app.route('/contact')
def page_contact():
    return render_template('Contact.html')

@app.route('/datatable')
@login_required
def page_datatable():
    return render_template('Datatable.html')

def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return datetime.now()
