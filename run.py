from app import app
from api.routes import api_bp
from database.db import db
from flask_migrate import Migrate

migrate = Migrate(app, db)

db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0')