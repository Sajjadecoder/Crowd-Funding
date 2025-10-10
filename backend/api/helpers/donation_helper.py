from api import db, bcrypt
from api.models.cf_models import Donations, DonationStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_donation(user_id, campaign_id, amount, status=""):
    if not amount:
        raise ValueError("Amount cannot be empty/0")

    try:
        status_enum = (
            status if isinstance(status, DonationStatus) else DonationStatus(status)
        )
    except ValueError:
        raise ValueError(f"Invalid donation status: {status}")

    donation = Donations(
        user_id=user_id, campaign_id=campaign_id, amount=amount, status=status_enum
    )

    db.session.add(donation)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not create donation: {str(e)}")

    return donation.to_dict()


def view_donation_by_donation_id(donation_id):
    donation = Donations.query.get(donation_id)
    if not donation:
        raise ValueError(f"Could not find donation with donation id: {donation_id}")

    return donation.to_dict()


def view_all_donations_by_user(user_id):
    donations = Donations.query.filter_by(user_id=user_id).all()
    if not donations:
        raise ValueError(f"No donation found by user id: {user_id}")

    return [donation.to_dict() for donation in donations]


def view_all_donations_by_campaign(campaign_id):
    donations = Donations.query.filter_by(campaign_id=campaign_id).all()
    if not donations:
        raise ValueError(f"No donation found by campaign id: {campaign_id}")

    return [donation.to_dict() for donation in donations]


def updateDonationStatus(donation_id, status):
    donation = Donations.query.get(donation_id)

    if not donation:
        raise ValueError(f"Could not find donation with donation id: {donation_id}")

    try:
        donation.status = (
            status if isinstance(status, DonationStatus) else DonationStatus(status)
        )
    except ValueError:
        raise ValueError(f"Invalid donation status: {status}")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not update donation status. Error: {str(e)}")

    return donation.to_dict()


def cancel_donation(donation_id):
    donation = Donations.query.get(donation_id)

    if not donation:
        raise ValueError("Donation not found")

    donation.status = DonationStatus.CANCELLED

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not cancel the donation. Error: {str(e)}")
