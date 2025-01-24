from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
 
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/login')
def login():
    return render_template('login.htm')

@app.route('/register')
def register():
    return render_template('register.htm')
 
# Database initialization
def init_db():
    conn = sqlite3.connect('translator.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_description TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()
 
init_db()
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Hent data fra skjemaet
        full_name = request.form['full_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # Krypter passordet
        
        # Prøv å legge til brukeren i databasen
        
        try:
            conn = sqlite3.connect('translator.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password, full_name) VALUES (?, ?, ?)',
                (email, password, full_name)
            )
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))  # Omdiriger til innloggingssiden
        except Exception as error:
            print (error)
        finally:
            conn.close()
    
    # Hvis GET-forespørsel, vis registreringssiden
    return ('wrong password')

if __name__ == '__main__':
    app.run(debug=True)