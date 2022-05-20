from company.urls import bp as company_bp
from user.urls import bp as user_bp
from auth.urls import bp as auth_bp
from location.urls import bp as location_bp


def register_blueprints(app):
    app.register_blueprint(company_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(location_bp)
