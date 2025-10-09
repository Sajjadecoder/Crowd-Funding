from api import db, app, bcrypt
from datetime import datetime
from sqlalchemy import Enum
import enum
from decimal import Decimal

class UserRole(enum.Enum):
    DONOR = "donor"
    CREATOR = "creator"
    ADMIN = "admin"


class CampaignCategory(enum.Enum):
    TECHNOLOGY = "Technology"
    COMMUNITY = "Community"
    ARTS = "Arts"
    HEALTH = "Health"
    BUSINESS = "Business"


class CampaignStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class CampaignPaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REFUNDED = "refunded"


class ReviewStatus(enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.DONOR)
    profile_image = db.Column(db.String(255), nullable=True)

    def setPasswordHash(self, plaintextPassword):
        self.password_hash = bcrypt.generate_password_hash(plaintextPassword).decode("utf-8")

    def checkHashedPassword(self, plaintextPassword):
        return bcrypt.check_password_hash(self.password_hash, plaintextPassword)
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }
    
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")


class Campaigns(db.Model):
    __tablename__ = "campaigns"

    campaign_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey(Users.user_id), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    short_description = db.Column(db.String(255))
    long_description = db.Column(db.Text)
    category = db.Column(db.Enum(CampaignCategory), nullable=False)
    goal_amount = db.Column(db.Numeric(8, 2), nullable=False)
    raised_amount = db.Column(db.Numeric(8, 2), default=Decimal("0.00"), nullable=False)
    image_url = db.Column(db.String(2083))
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(CampaignStatus), default=CampaignStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Donations(db.Model):
    __tablename__ = "donations"

    donation_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaigns.campaign_id), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey(Users.user_id), nullable=False)
    amount = db.Column(db.Numeric(8, 2), nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Enum(CampaignPaymentStatus), default=CampaignPaymentStatus.PENDING)


class Payments(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey(Donations.donation_id), nullable=False)
    amount = db.Column(db.Numeric(8, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.Enum(CampaignPaymentStatus), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class CampaignUpdates(db.Model):
    __tablename__ = "campaign_updates"

    update_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaigns.campaign_id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.user_id))
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class AdminReviews(db.Model):
    __tablename__ = "admin_reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaigns.campaign_id), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(Users.user_id))
    decision = db.Column(db.Enum(ReviewStatus))
    reason = db.Column(db.String(100), nullable=True)
    reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)


class Comments(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaigns.campaign_id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.user_id), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)


class Follows(db.Model):
    __tablename__ = "follows"

    follow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.user_id), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaigns.campaign_id), nullable=False)
    followed_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()
