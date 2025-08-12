# Import app and extensions from extensions.py
from extensions import app, db

# Import models to create tables
from models import *

# Import and register routes
from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)