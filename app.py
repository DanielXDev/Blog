from flask import Flask
from flask_login import LoginManager
from models.base import db
from models.user import User
from config import Config
from flask_ckeditor import CKEditor, CKEditorField
import os


from routes.blog_routes import blog_bp
from routes.main_routes import main_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ckeditor = CKEditor()
    ckeditor.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug= True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    