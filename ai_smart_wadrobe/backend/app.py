import os
from flask import Flask, render_template, request, redirect, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration for Render
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wardrobe.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Service URLs for Render
app.config['WEATHER_API_KEY'] = os.environ.get('WEATHER_API_KEY', '')
app.config['ML_API_URL'] = os.environ.get('ML_API_URL', 'http://localhost:8001')
app.config['CV_API_URL'] = os.environ.get('CV_API_URL', 'http://localhost:8002')

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    api_key=os.environ.get('CLOUDINARY_API_KEY', ''),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', '')
)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models (same as before, but optimized for PostgreSQL)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cloth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cloth_type = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50))
    season = db.Column(db.String(20))
    fabric = db.Column(db.String(50))
    image_url = db.Column(db.String(500))  # Cloudinary URL
    is_clean = db.Column(db.Boolean, default=True)
    wear_count = db.Column(db.Integer, default=0)
    last_worn = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes and helper functions (same as before but with Cloudinary upload)

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'smart-wardrobe-backend',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/test')
def api_test():
    """Test endpoint to verify services are working"""
    try:
        # Test database
        user_count = User.query.count()
        
        # Test ML service
        ml_response = requests.get(f"{app.config['ML_API_URL']}/health", timeout=5)
        
        # Test CV service
        cv_response = requests.get(f"{app.config['CV_API_URL']}/health", timeout=5)
        
        return jsonify({
            'database': f'connected (users: {user_count})',
            'ml_service': ml_response.status_code if ml_response else 'unavailable',
            'cv_service': cv_response.status_code if cv_response else 'unavailable',
            'status': 'all systems operational'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Create demo user if not exists
    if not User.query.filter_by(username='demo').first():
        demo_user = User(
            username='demo',
            email='demo@smartwardrobe.com',
            password_hash=bcrypt.generate_password_hash('demo123').decode('utf-8')
        )
        db.session.add(demo_user)
        db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)