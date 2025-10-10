from api import db
from api.models.cf_models import Follows, Users, Campaigns
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def follow_campaign(user_id, campaign_id):
    existing_follow = Follows.query.filter_by(user_id=user_id, campaign_id=campaign_id).first()
    if existing_follow:
        raise ValueError("User already follows this campaign.")

    follow = Follows(user_id=user_id, campaign_id=campaign_id)

    db.session.add(follow)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise RuntimeError("Could not follow campaign due to database integrity error.")
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not follow campaign: {str(e)}")

    return follow.to_dict()


def unfollow_campaign(user_id, campaign_id):
    follow = Follows.query.filter_by(user_id=user_id, campaign_id=campaign_id).first()
    if not follow:
        raise ValueError("User is not following this campaign.")

    try:
        db.session.delete(follow)
        db.session.commit()
        return {"message": f"User {user_id} unfollowed campaign {campaign_id} successfully."}
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not unfollow campaign: {str(e)}")


def view_follow_by_id(follow_id):
    follow = Follows.query.get(follow_id)
    if not follow:
        raise ValueError(f"No follow record found with follow id: {follow_id}")
    return follow.to_dict()


def view_all_follows():
    follows = Follows.query.all()
    if not follows:
        raise ValueError("No follow records found.")
    return [f.to_dict() for f in follows]


def view_all_followed_campaigns_by_user(user_id):
    follows = Follows.query.filter_by(user_id=user_id).all()
    if not follows:
        raise ValueError(f"No campaigns followed by user id: {user_id}")
    return [f.to_dict() for f in follows]


def view_all_followers_by_campaign(campaign_id):
    follows = Follows.query.filter_by(campaign_id=campaign_id).all()
    if not follows:
        raise ValueError(f"No followers found for campaign id: {campaign_id}")
    return [f.to_dict() for f in follows]


def is_user_following(user_id, campaign_id):
    follow = Follows.query.filter_by(user_id=user_id, campaign_id=campaign_id).first()
    return {"is_following": bool(follow)}


def count_followers(campaign_id):
    count = db.session.query(db.func.count(Follows.follow_id)).filter_by(campaign_id=campaign_id).scalar()
    return {"campaign_id": campaign_id, "follower_count": count or 0}


def count_followed_campaigns(user_id):
    count = db.session.query(db.func.count(Follows.follow_id)).filter_by(user_id=user_id).scalar()
    return {"user_id": user_id, "followed_campaigns_count": count or 0}


def delete_follow(follow_id):
    follow = Follows.query.get(follow_id)
    if not follow:
        raise ValueError(f"No follow record found with id: {follow_id}")

    try:
        db.session.delete(follow)
        db.session.commit()
        return {"message": f"Follow record {follow_id} deleted successfully."}
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not delete follow record: {str(e)}")