from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            pincode TEXT NOT NULL,
            whatsapp_number TEXT,
            address TEXT NOT NULL,
            landmark TEXT NOT NULL,
            state TEXT NOT NULL,
            city TEXT NOT NULL,
            approx_books INTEGER NOT NULL,
            carton_boxes INTEGER,
            total_weight INTEGER NOT NULL,
            categories TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    # Embed your HTML form directly for simplicity
    return render_template_string(open('form.html').read())

@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect data from the form
    data = {
        "first_name": request.form.get('firstName'),
        "last_name": request.form.get('lastName'),
        "pincode": request.form.get('pincode'),
        "whatsapp_number": request.form.get('whatsappNumber'),
        "address": request.form.get('address'),
        "landmark": request.form.get('landmark'),
        "state": request.form.get('state'),
        "city": request.form.get('city'),
        "approx_books": request.form.get('approxBooks'),
        "carton_boxes": request.form.get('cartonBoxes'),
        "total_weight": request.form.get('totalWeight'),
        "categories": ','.join(request.form.getlist('category'))
    }

    # Insert data into SQLite
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donations (
            first_name, last_name, pincode, whatsapp_number, address, 
            landmark, state, city, approx_books, carton_boxes, total_weight, categories
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["first_name"], data["last_name"], data["pincode"], data["whatsapp_number"],
        data["address"], data["landmark"], data["state"], data["city"],
        data["approx_books"], data["carton_boxes"], data["total_weight"], data["categories"]
    ))
    conn.commit()
    conn.close()

    return "Form submitted successfully!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
