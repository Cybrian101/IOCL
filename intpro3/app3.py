from flask import Flask, render_template, request, redirect, url_for , session
import sqlite3
import datetime

app = Flask(__name__)

# Function to create database connection
def get_db_connection():
    conn = sqlite3.connect('database3.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for displaying the initial login page (login3.html)
@app.route('/', methods=['GET'])
def login_page():
    max_serial = 0  # Default value
    return render_template('test3.html', max_serial=max_serial)

@app.route('/submit_login', methods=['POST'])
def submit_login():
    entered_id = request.form['id']
    entered_password = request.form['password']

    # Assuming validation logic here, redirect based on user type
    if entered_id == 'User1' and entered_password == 'iocl2024':
        session['user_id'] = 'User1'
        return redirect(url_for('user_page'))
    elif entered_id == 'User2' and entered_password == 'iocl2024':
        session['user_id'] = 'User2'
        return redirect(url_for('user_page'))
    elif entered_id == 'User3' and entered_password == 'iocl2024':
        session['user_id'] = 'User3'
        return redirect(url_for('user_page'))
    elif entered_id == 'Admin' and entered_password == 'iocl2024':
        session['user_id'] = 'Admin'
        return redirect(url_for('admin_page'))
    else:
        return redirect(url_for('login_page'))  # Redirect to login page if credentials are invalid


# Route for user page after successful login
@app.route('/login3.html', methods=['GET'])
def user_page():
    user_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the maximum serial_number currently in the activities table
    cursor.execute('SELECT MAX(serial_number) AS max_serial FROM activities')
    row = cursor.fetchone()
    max_serial = row['max_serial'] if row and row['max_serial'] else 0  # Get the maximum serial_number

    conn.close()

    return render_template('login3.html', max_serial=max_serial, currentDate=get_current_date(), user_id=user_id)


# Route for admin page after successful login
@app.route('/submission3.html', methods=['GET'])
def admin_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all rows from the activities table
    cursor.execute('SELECT * FROM activities')
    rows = cursor.fetchall()

    conn.close()

    return render_template('submission3.html', currentDate=get_current_date(), rows=rows)

# Route for handling form submission from login3.html
@app.route('/submit_form', methods=['POST'])
def submit_form_post():
    user_id = request.form['user_id']
    current_date = request.form['currentDate']
    down_date = request.form['downDate']
    down_time = request.form['downTime']
    main_category = request.form['mainCategory']
    sub_category = request.form['subCategory']
    ticket_id = request.form['ticketId']
    remarks = request.form['remarks']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the last inserted row to get the latest serial number
    cursor.execute('SELECT * FROM activities ORDER BY serial_number DESC LIMIT 1')
    row = cursor.fetchone()

    # Calculate the new serial number and id number
    if row and row['serial_number'] is not None:
        serial_number = row['serial_number'] + 1
        id_number = '{:04d}'.format(int(row['id_number']) + 1)
    else:
        serial_number = 1
        id_number = '1111'

    # Generate ticket ID with current year, month, date, and serial number
    # current_datetime = datetime.datetime.now()
    # ticket_id = f"{current_datetime.year:02d}{current_datetime.month:02d}{current_datetime.day:02d}{serial_number}{ticket_id}"

    # Insert data into activities table
    cursor.execute('''
        INSERT INTO activities (user_id, serial_number, id_number, current_date,down_date, down_time, main_category, sub_category, ticket_id, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)
    ''', (user_id, serial_number, id_number, current_date,down_date, down_time, main_category, sub_category, ticket_id, remarks))

    conn.commit()
    conn.close()

    # Redirect to user_page to update idNumber
    return redirect(url_for('login_page'))



# Route for success page
@app.route('/submit_success', methods=['GET'])
def submit_success():
    return 'Form submitted successfully!'

# Route for rendering modify3.html with form
@app.route('/modify3.html', methods=['GET'])
def modify_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activities')
    rows = cursor.fetchall()
    conn.close()
    return render_template('modify3.html', rows=rows)

# Route to display modify_form.html with pre-filled data
@app.route('/modifyform/<int:serial_number>', methods=['GET'])
def modify_form(serial_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activities WHERE serial_number = ?', (serial_number,))
    row = cursor.fetchone()
    conn.close()
    return render_template('modify_form3.html', row=row)

# Route to handle form submission from modify_form.html
@app.route('/save_modifications', methods=['POST'])
def save_modifications():
    serial_number = request.form['serialNumber']
    modify_engineer_name = request.form['modifyEngineerName']
    up_time = request.form['upTime']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE activities
        SET modify_engineer_name = ?,
            up_time = ?
        WHERE serial_number = ?
    ''', (modify_engineer_name, up_time, serial_number))
    conn.commit()
    conn.close()

    return 'Modifications saved successfully!'

# Route to handle deletion of a row
@app.route('/delete/<int:serial_number>', methods=['POST'])
def delete_entry(serial_number):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the row from the database
    cursor.execute('DELETE FROM activities WHERE serial_number = ?', (serial_number,))
    conn.commit()

    conn.close()

    # Redirect to the modify page after deletion
    return redirect(url_for('modify_page'))

# for cancellll bruuhhhhh
@app.route('/cancel/<int:serial_number>', methods=['POST'])
def cancel_entry(serial_number):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the row to mark it as cancelled
    cursor.execute('UPDATE activities SET status = "Cancelled" WHERE serial_number = ?', (serial_number,))
    conn.commit()

    conn.close()

    return redirect(url_for('admin_page'))

# Function to format date string if needed
def format_date(date_string):
    try:
        date_obj = datetime.datetime.strptime(date_string, '%d-%m-%Y')
        return date_obj.strftime('%d-%m-%Y')
    except ValueError:
        return date_string  # Return original string if format is incorrect

# Function to get current date in YYYY-MM-DD format
def get_current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    app.run(debug=True)
