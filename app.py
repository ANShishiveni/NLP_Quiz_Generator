import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)
# Create the app
app = Flask(__name__)

# Initialize Migrate after app is created
migrate = Migrate(app, db)
app.secret_key = os.environ.get("SESSION_SECRET", "quiz-generator-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Needed for url_for to generate with https

# Configure the database
database_url = os.environ.get("DATABASE_URL")
# Handle missing or malformed environment variable
if not database_url:
    logger.warning("DATABASE_URL environment variable is not set, using fallback")
    database_url = "sqlite:///quiz.db"
else:
    if database_url.startswith("postgresql"):
        try:
            import psycopg2
            conn = psycopg2.connect(database_url)
            conn.close()
        except Exception:
            logger.warning("Postgres connection failed during startup, falling back to SQLite")
            database_url = "sqlite:///quiz.db"

# Set the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the database extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Import models after db initialization
if not os.environ.get("SKIP_APP_INIT"):
    with app.app_context():
        import models
        try:
            db.create_all()
        except OperationalError:
            logger.warning("Database connection failed, falling back to SQLite")
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
            db.engine.dispose()
            db.create_all()
        try:
            if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
                with db.engine.begin() as conn:
                    rows = conn.exec_driver_sql("PRAGMA table_info(questions)").fetchall()
                    cols = [row[1] for row in rows]
                    missing = []
                    if "difficulty" not in cols:
                        missing.append("ALTER TABLE questions ADD COLUMN difficulty TEXT")
                    if "validated" not in cols:
                        missing.append("ALTER TABLE questions ADD COLUMN validated BOOLEAN DEFAULT 0")
                    if "validation_confidence" not in cols:
                        missing.append("ALTER TABLE questions ADD COLUMN validation_confidence REAL DEFAULT 0.0")
                    if "flagged" not in cols:
                        missing.append("ALTER TABLE questions ADD COLUMN flagged BOOLEAN DEFAULT 0")
                    if "support_text" not in cols:
                        missing.append("ALTER TABLE questions ADD COLUMN support_text TEXT")
                    if "reference_source" not in cols:
                        missing.append("ALTER TABLE questions ADD COLUMN reference_source TEXT")
                    for sql in missing:
                        conn.exec_driver_sql(sql)
                    if missing:
                        logger.info("Applied SQLite schema updates: %s", "; ".join(missing))
        except Exception:
            pass
        from auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

# Load the user loader callback function
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
