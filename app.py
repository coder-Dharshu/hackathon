# Import necessary modules from Flask and other libraries.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_cors import CORS

# Initialize the Flask application.
app = Flask(__name__)
CORS(app) # ENABLE CORS

# --- Database and Configuration Setup ---
# A simple configuration for SQLite, a file-based database.
# The database file will be created in the same directory as this script.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kalakriti.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the app.
db = SQLAlchemy(app)

# Initialize the Bcrypt object for password hashing.
bcrypt = Bcrypt(app)

# --- Database Model Definition ---
# This class defines the structure of the 'artists' table in our database.
# It inherits from db.Model provided by Flask-SQLAlchemy.
class Artist(db.Model):
    # 'id' is the primary key, a unique identifier for each artist.
    id = db.Column(db.Integer, primary_key=True)
    # 'email' must be unique to prevent multiple artists from using the same email.
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 'password' is stored as a hashed string for security.
    password_hash = db.Column(db.String(128), nullable=False)
    # NEW: role to distinguish between artist and customer.
    role = db.Column(db.String(20), default='customer', nullable=False)

    # A method to set the password, which hashes it using bcrypt.
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # A method to check a provided password against the stored hash.
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # A string representation of the object for debugging purposes.
    def __repr__(self):
        return f'<Artist {self.email}>'

# --- API Endpoints ---

@app.route('/register', methods=['POST'])
def register():
    """
    Handles artist registration.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # NEW: get the role, with 'customer' as the default.
    role = data.get('role', 'customer')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if Artist.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    try:
        new_artist = Artist(email=email, role=role)
        new_artist.set_password(password)
        db.session.add(new_artist)
        db.session.commit()
        return jsonify({"message": "Artist registered successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error during registration: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Handles artist login authentication.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    artist = Artist.query.filter_by(email=email).first()

    if not artist or not artist.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    # NEW: Return the user's role
    return jsonify({"message": "Login successful!", "artist_id": artist.id, "role": artist.role}), 200


# --- Endpoint to check the backend data ---
@app.route('/artists', methods=['GET'])
def get_artists():
    """
    Retrieves and returns all artist data from the database.
    Note: In a real application, you would secure this endpoint.
    """
    # Query all artists from the database.
    artists = Artist.query.all()
    
    # Convert the list of artist objects into a list of dictionaries.
    # We do not return the password hash for security reasons.
    artists_list = []
    for artist in artists:
        artists_list.append({
            'id': artist.id,
            'email': artist.email,
            'role': artist.role
        })
    
    # Return the list as a JSON response.
    return jsonify(artists_list), 200

# This block ensures the database tables are created when the script is run.
# It only runs if the script is the main program, not when imported as a module.
if __name__ == '__main__':
    # Create the database and tables within the application context.
    with app.app_context():
        db.create_all()
    
    # Run the Flask development server.
    app.run(debug=True, port=5000)
