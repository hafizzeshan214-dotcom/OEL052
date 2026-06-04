from flask import Flask, render_template, request, redirect, session, flash, url_for
from database import get_db_connection, init_db
import os

app = Flask(__name__)
app.secret_key = 'hospital_secret_key_123'

# Initialize database on startup
init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Username or Password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()
    
    return render_template('dashboard.html', patients=patients)

@app.route('/add', methods=['POST'])
def add_patient():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    disease = request.form.get('disease')
    
    if not name:
        flash('Name is required!', 'danger')
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    conn.execute('INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)',
                 (name, age, gender, disease))
    conn.commit()
    conn.close()
    
    flash('Patient Added Successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update/<int:id>', methods=['POST'])
def update_patient(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    disease = request.form.get('disease')
    
    conn = get_db_connection()
    conn.execute('UPDATE patients SET name=?, age=?, gender=?, disease=? WHERE id=?',
                 (name, age, gender, disease, id))
    conn.commit()
    conn.close()
    
    flash('Patient Updated Successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Patient Deleted Successfully', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
