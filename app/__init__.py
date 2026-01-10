import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, render_template
from config import Config

db = None
bucket = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    global db, bucket

    if not firebase_admin._apps:
        cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS_PATH'])
        firebase_admin.initialize_app(cred, {
            'storageBucket': app.config['FIREBASE_CONFIG']['storageBucket']
        })

    db = firestore.client()
    bucket = storage.bucket()

    from app.blueprints import match, explain, audit
    app.register_blueprint(match.bp)
    app.register_blueprint(explain.bp)
    app.register_blueprint(audit.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
