from flask import Flask
from flask_restx import Api, Namespace
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api (
    app,
    version = '1.0',
    title = "Crowdfunding platform",
    description = "Api for crowdfunding platform"
)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:14Nov%402005@localhost:5432/crowdfunding_db"

db = SQLAlchemy(app)



