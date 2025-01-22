from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentmart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Initialize the database
db = SQLAlchemy(app)

# Define the ProductRequest model
class ProductRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ProductRequest {self.first_name} {self.last_name}>'

# Route to initialize the database
@app.route('/init_db')
def init_db():
    db.create_all()  # This will create the tables if they don't exist
    return "Database initialized!"

# Home route
@app.route('/')
def home():
    return render_template('product_form.html')

# Route to handle form submission
@app.route('/submit_request', methods=['POST'])
def submit_request():
    # Get form data
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    product_type = request.form.get('product-type')
    product_name = request.form.get('product-name')
    description = request.form.get('description')

    # Validate required fields
    if not first_name or not last_name or not email:
        flash("First name, last name, and email are required.", "error")
        return redirect(url_for('home'))

    # Create a new ProductRequest record
    new_request = ProductRequest(
        first_name=first_name,
        last_name=last_name,
        email=email,
        product_type=product_type,
        product_name=product_name,
        description=description
    )

    # Add the new request to the session and commit to the database
    db.session.add(new_request)
    db.session.commit()

    flash("Your request has been submitted successfully!", "success")
    return redirect(url_for('home'))  # Redirect back to home after submission

if __name__ == '__main__':
    app.run(debug=True)