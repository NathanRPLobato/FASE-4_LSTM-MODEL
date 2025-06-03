from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    Swagger(app)
    
    from app.routes.predict import predict_bp
    app.register_blueprint(predict_bp)
    
    return app
