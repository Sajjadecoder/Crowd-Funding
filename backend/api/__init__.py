from flask import Flask
from flask_restx import Api, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
api = Api (
    app,
    version = '1.0',
    title = "Crowdfunding platform",
    description = "Api for crowdfunding platform"
)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:14Nov%402005@localhost:5432/crowdfunding_db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

users_ns = Namespace('Users', description='Data about the users')
campaigns_ns = Namespace('Campaigns', description="Data about the campaigns")
donations_ns = Namespace('Donations', description='Data about the donations')
payments_ns = Namespace('Payments', description='Data about the payments')
updates_ns = Namespace('Updates', description="Data about the updates")

api.add_namespace(users_ns, '/users')
api.add_namespace(campaigns_ns, '/campaigns')
api.add_namespace(donations_ns, '/donations')
api.add_namespace(payments_ns, '/payments')
api.add_namespace(updates_ns, '/updates')


import api.models.cf_models
