from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for donations
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    whatsapp_number = db.Column(db.String(10), nullable=True)
    use_as_mobile = db.Column(db.Boolean, default=False)
    address = db.Column(db.Text, nullable=False)
    landmark = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    approx_books = db.Column(db.Integer, nullable=False)
    carton_boxes = db.Column(db.Integer, nullable=True)
    total_weight = db.Column(db.Integer, nullable=False)
    categories = db.Column(db.String(255), nullable=True)
    terms_agreed = db.Column(db.Boolean, default=False)

# Route to render the form
@app.route("/")
def donation_form():
    return render_template("donation_form.html")

# Route to handle form submission
@app.route("/submit", methods=["POST"])
def submit_donation():
    data = request.form
    selected_categories = ", ".join(data.getlist("category"))

    new_donation = Donation(
        first_name=data["firstName"],
        last_name=data["lastName"],
        pincode=data["pincode"],
        whatsapp_number=data["whatsappNumber"],
        use_as_mobile="useAsMobileNumber" in data,
        address=data["address"],
        landmark=data["landmark"],
        state=data["state"],
        city=data["city"],
        approx_books=data["approxBooks"],
        carton_boxes=data.get("cartonBoxes", None),
        total_weight=data["totalWeight"],
        categories=selected_categories,
        terms_agreed="terms" in data
    )

    db.session.add(new_donation)
    db.session.commit()
    return redirect(url_for("donation_form"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)
