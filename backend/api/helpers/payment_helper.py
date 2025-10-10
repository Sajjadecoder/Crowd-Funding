from api import db
from api.models.cf_models import Payments, CampaignPaymentStatus
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def create_payment(donation_id, amount, payment_method, payment_status):
    if not amount or amount <= 0:
        raise ValueError("Amount must be greater than 0.")

    if not payment_method:
        raise ValueError("Payment method cannot be empty.")

    try:
        payment_status = (
            payment_status
            if isinstance(payment_status, CampaignPaymentStatus)
            else CampaignPaymentStatus(payment_status)
        )
    except ValueError:
        raise ValueError(
            f"Invalid payment status. Must be one of: {[s.value for s in CampaignPaymentStatus]}"
        )

    payment = Payments(
        donation_id=donation_id,
        amount=amount,
        payment_method=payment_method,
        payment_status=payment_status,
    )

    db.session.add(payment)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise RuntimeError("Payment creation failed due to database integrity error.")
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not create payment: {str(e)}")

    return payment.to_dict()


def view_payment_by_payment_id(payment_id):
    payment = Payments.query.get(payment_id)
    if not payment:
        raise ValueError(f"Could not find payment with payment id: {payment_id}")
    return payment.to_dict()


def view_all_payments():
    payments = Payments.query.all()
    if not payments:
        raise ValueError("No payments found.")
    return [p.to_dict() for p in payments]


def view_all_payments_by_donation(donation_id):
    payments = Payments.query.filter_by(donation_id=donation_id).all()
    if not payments:
        raise ValueError(f"No payments found for donation id: {donation_id}")
    return [p.to_dict() for p in payments]


def update_payment_status(payment_id, new_status):
    payment = Payments.query.get(payment_id)
    if not payment:
        raise ValueError(f"Payment with payment id {payment_id} not found.")

    try:
        new_status = (
            new_status
            if isinstance(new_status, CampaignPaymentStatus)
            else CampaignPaymentStatus(new_status)
        )
    except ValueError:
        raise ValueError(
            f"Invalid payment status. Must be one of: {[s.value for s in CampaignPaymentStatus]}"
        )

    payment.payment_status = new_status
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not update payment status: {str(e)}")

    return payment.to_dict()


def update_payment_method(payment_id, new_method):
    payment = Payments.query.get(payment_id)
    if not payment:
        raise ValueError(f"Payment with payment id {payment_id} not found.")

    if not new_method:
        raise ValueError("Payment method cannot be empty.")

    payment.payment_method = new_method
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not update payment method: {str(e)}")

    return payment.to_dict()


def delete_payment(payment_id):
    payment = Payments.query.get(payment_id)
    if not payment:
        raise ValueError(f"Payment with payment id {payment_id} not found.")

    try:
        db.session.delete(payment)
        db.session.commit()
        return {"message": f"Payment with id {payment_id} deleted successfully."}
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not delete payment: {str(e)}")


def get_total_payments():
    total = db.session.query(db.func.count(Payments.payment_id)).scalar()
    return {"total_payments": total or 0}


def get_total_payment_amount():
    total = db.session.query(db.func.sum(Payments.amount)).scalar()
    return {"total_amount": float(total or 0)}


def filter_payments_by_status(status):
    try:
        status_enum = (
            status
            if isinstance(status, CampaignPaymentStatus)
            else CampaignPaymentStatus(status)
        )
    except ValueError:
        raise ValueError(
            f"Invalid payment status. Must be one of: {[s.value for s in CampaignPaymentStatus]}"
        )

    payments = Payments.query.filter_by(payment_status=status_enum).all()
    if not payments:
        raise ValueError(f"No payments found with status: {status_enum.value}")

    return [p.to_dict() for p in payments]


def filter_payments_by_method(method):
    payments = Payments.query.filter(
        db.func.lower(Payments.payment_method) == method.lower()
    ).all()
    if not payments:
        raise ValueError(f"No payments found using method: {method}")
    return [p.to_dict() for p in payments]