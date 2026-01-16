#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import db, app, User, Cloth
import bcrypt

def initialize_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo').first()
        
        if not demo_user:
            # Create demo user
            hashed_password = bcrypt.hashpw('demo123'.encode('utf-8'), bcrypt.gensalt())
            demo_user = User(
                username='demo',
                email='demo@smartwardrobe.com',
                password_hash=hashed_password.decode('utf-8')
            )
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Demo user created")
            
            # Add sample clothes for demo user
            sample_clothes = [
                {
                    'name': 'Blue Denim Jacket',
                    'cloth_type': 'jacket',
                    'color': 'blue',
                    'season': 'all',
                    'fabric': 'denim',
                    'wear_count': 5,
                    'is_clean': True
                },
                {
                    'name': 'White Cotton T-Shirt',
                    'cloth_type': 'tshirt',
                    'color': 'white',
                    'season': 'summer',
                    'fabric': 'cotton',
                    'wear_count': 12,
                    'is_clean': True
                },
                {
                    'name': 'Black Formal Pants',
                    'cloth_type': 'pants',
                    'color': 'black',
                    'season': 'all',
                    'fabric': 'polyester',
                    'wear_count': 8,
                    'is_clean': False
                },
                {
                    'name': 'Red Wool Sweater',
                    'cloth_type': 'sweater',
                    'color': 'red',
                    'season': 'winter',
                    'fabric': 'wool',
                    'wear_count': 3,
                    'is_clean': True
                },
                {
                    'name': 'Blue Denim Jeans',
                    'cloth_type': 'jeans',
                    'color': 'blue',
                    'season': 'all',
                    'fabric': 'denim',
                    'wear_count': 15,
                    'is_clean': True
                }
            ]
            
            for cloth_data in sample_clothes:
                cloth = Cloth(
                    user_id=demo_user.id,
                    **cloth_data
                )
                db.session.add(cloth)
            
            db.session.commit()
            print(f"✅ Added {len(sample_clothes)} sample clothes")
        
        # Count users and clothes
        user_count = User.query.count()
        cloth_count = Cloth.query.count()
        
        print(f"\n📊 Database Summary:")
        print(f"   Users: {user_count}")
        print(f"   Clothes: {cloth_count}")
        print(f"\n🔗 Demo Credentials:")
        print(f"   Username: demo")
        print(f"   Password: demo123")
        print("\n✅ Database initialization complete!")

if __name__ == '__main__':
    initialize_database()