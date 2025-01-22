from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

app1 = Flask(__name__)

# Configure the SQLite database URI
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mart.db'
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app1.config['SECRET_KEY'] = 'your_secret_key'  # Needed for flash messages and CSRF protection

# Initialize the database
db = SQLAlchemy(app1)

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

# Define the ProductRequest form
class ProductRequestForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    product_type = SelectField('Product Type', choices=['Type 1', 'Type 2', 'Type 3'], validators=[DataRequired()])
    product_name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')

# Route to initialize the database
@app1.route('/init_db')
def init_db():
    with app1.app_context():
        db.create_all()  # This will create the tables if they don't exist
    return "Database initialized!"

# Home route
@app1.route('/')
def home():
    form = ProductRequestForm()
    return render_template('product_form.html', form=form)

# Route to handle form submission
@app1.route('/submit_request', methods=['POST'])
def submit_request():
    form = ProductRequestForm()
    if form.validate_on_submit():
        # Create a new ProductRequest record
        new_request = ProductRequest(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            product_type=form.product_type.data,
            product_name=form.product_name.data,
            description=form.description.data
        )

        try:
            db.session.add(new_request)
            db.session.commit()
            flash("Your request has been submitted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
    else:
        flash("Please fill in all required fields.", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app1.run(debug=True, port=5002)