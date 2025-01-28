from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            pincode TEXT NOT NULL,
            address TEXT NOT NULL,
            landmark TEXT NOT NULL,
            city TEXT NOT NULL,
            approx_books INTEGER NOT NULL,
            carton_boxes INTEGER,
            discount TEXT,
            categories TEXT,
            terms_accepted INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route to render the form
@app.route('/')
def index():
    return render_template('donation_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Fetch form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        mobile = request.form['mobile']
        pincode = request.form['pincode']
        address = request.form['address']
        landmark = request.form['landmark']
        city = request.form['city']
        approx_books = request.form['approxBooks']
        carton_boxes = request.form.get('cartonBoxes', 0)  # Optional field
        discount = request.form.get('discount', None)      # Optional field
        categories = ', '.join(request.form.getlist('category'))  # Combine selected categories
        terms_accepted = 1 if 'terms' in request.form else 0  # Checkbox validation

        # Save data to the database
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO donations (
                first_name, last_name, email, mobile, pincode, address, landmark, 
                city, approx_books, carton_boxes, discount, categories, terms_accepted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, mobile, pincode, address, landmark, city,
              approx_books, carton_boxes, discount, categories, terms_accepted))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    # Initialize the database before starting the app
    init_db()
    app.run(debug=True)
