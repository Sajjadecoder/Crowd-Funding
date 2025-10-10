from sqlalchemy import func
from api import db
from api.models import Comments, Users, Campaigns


def get_total_comments():
    return db.session.query(func.count(Comments.comment_id)).scalar()


def get_total_comments_by_user(user_id):
    return (
        db.session.query(func.count(Comments.comment_id))
        .filter_by(user_id=user_id)
        .scalar()
    )


def get_total_comments_by_campaign(campaign_id):
    return (
        db.session.query(func.count(Comments.comment_id))
        .filter_by(campaign_id=campaign_id)
        .scalar()
    )


def get_top_commenters(limit=5):
    results = (
        db.session.query(
            Users.username, func.count(Comments.comment_id).label("comment_count")
        )
        .join(Comments, Users.user_id == Comments.user_id)
        .group_by(Users.username)
        .order_by(func.count(Comments.comment_id).desc())
        .limit(limit)
        .all()
    )

    return [{"username": r.username, "comment_count": r.comment_count} for r in results]


def get_top_commented_campaigns(limit=5):
    results = (
        db.session.query(
            Campaigns.title, func.count(Comments.comment_id).label("comment_count")
        )
        .join(Comments, Campaigns.campaign_id == Comments.campaign_id)
        .group_by(Campaigns.title)
        .order_by(func.count(Comments.comment_id).desc())
        .limit(limit)
        .all()
    )

    return [{"title": r.title, "comment_count": r.comment_count} for r in results]


def get_average_likes_per_comment():
    avg_likes = db.session.query(func.avg(Comments.likes)).scalar()
    return round(avg_likes or 0, 2)
