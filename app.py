from flask import Flask, redirect, render_template, request
import os
import psycopg2  # PostgreSQL-Adapter
import string
import random
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# PostgreSQL-Verbindung
def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    return conn

# Tabellen erstellen (nur beim ersten Start)
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


        
    short_url = request.host_url + short_code
    return render_template('index.html', short_url=short_url)
    


@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = get_db_connection()
    url = conn.execute('SELECT original_url FROM urls WHERE short_code = ?',
                       (short_code,)).fetchone()
    conn.close()
    
    if url:
        return redirect(url['original_url'])
    return render_template('404.html'), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)