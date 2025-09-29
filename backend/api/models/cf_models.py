from api import db, app, bcrypt
from datetime import datetime
from sqlalchemy import DateTime, Enum
import enum
from decimal import Decimal

class Users (db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False)
    email = db.Column(db.String(length = 255), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 255), nullable = False)
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)

    def setPasswordHash(self, plaintextPassword):
        self.password_hash = bcrypt.generate_password_hash(plaintextPassword).decode('utf-8')

    def checkHashedPassword(self, plaintextPassword):
        return bcrypt.check_password_hash(self.password_hash, plaintextPassword)
    
class CampaignCategory(enum.Enum):
    TECHNOLOGY = 'Technology'
    COMMUNITY = 'Community'
    ARTS = 'Arts'
    HEALTH = 'Health'
    BUSINESS = 'Business'

class Campaigns(db.Model):
    __tablename__ = 'campaigns'
    campaign_id = db.Column(db.Integer(), primary_key = True)
    creater_id = db.Column(db.Integer(), db.ForeignKey(Users.user_id), nullable = False)
    title = db.Column(db.String(length = 80), nullable = False)
    short_description = db.Column(db.String(length = 255))
    long_description = db.Column(db.Text())
    category = db.Column(Enum(CampaignCategory), nullable = False)
    goal_amount = db.Column(db.Numeric(8, 2), nullable = False)   
    raised_amount = db.Column(db.Numeric(8, 2), default = Decimal("0.00"), nullable=False)
    image_url = db.Column(db.String(2083))
    start_date = db.Column(DateTime, default = datetime.utcnow, nullable=False)
    end_date = db.Column(DateTime, nullable = False)

class Donations(db.Model):
    __tablename__ = 'donations'
    donation_id = db.Column(db.Integer(), primary_key = True)
    campaign_id = db.Column(db.Integer(), db.ForeignKey(Campaigns.campaign_id), nullable = False)
    donor_id = db.Column(db.Integer(), db.ForeignKey(Users.user_id), nullable = False)
    amount = db.Column(db.Numeric(8, 2), nullable = False)
    donation_date = db.Column(DateTime, nullable = False)

class CampaignPaymentStatus(enum.Enum):
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'
    REFUNDED = 'refunded' 

class Payments(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer(), primary_key = True)
    donation_id = db.Column(db.Integer(), db.ForeignKey(Donations.donation_id), nullable = False)
    payment_method = db.Column(db.String(length = 50), nullable = False)    #method enum? Validation...
    payment_status = db.Column(Enum(CampaignPaymentStatus), nullable = False)   
    transaction_date = db.Column(DateTime, default = datetime.utcnow, nullable=False)

class Updates(db.Model):
    __tablename__ = 'updates'
    update_id = db.Column(db.Integer(), primary_key = True)
    campaign_id = db.Column(db.Integer(), db.ForeignKey(Campaigns.campaign_id), nullable = False)
    title = db.Column(db.String(length = 80), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    created_at = db.Column(DateTime, default = datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()