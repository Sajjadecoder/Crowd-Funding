from api import db, bcrypt
from api.models.cf_models import Users, CampaignCategory, Campaigns, CampaignStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_campaign(
    creator_id, title, description, goal_amount, category=None, status=None
):
    try:
        campaign = Campaigns(
            creator_id=creator_id,
            title=title,
            description=description,
            category=(
                category
                if isinstance(category, CampaignCategory)
                else CampaignCategory(category)
            ),
            goal_amount=goal_amount,
            status=(
                status if isinstance(status, CampaignStatus) else CampaignStatus(status)
            ),
        )
        db.session.add(campaign)
        db.session.commit()
        return campaign.to_dict()
    except ValueError as e:
        db.session.rollback()
        raise ValueError(f"Invalid status or category {str(e)}")
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not create a new campaign: {str(e)}")


def delete_campaign(campaign_id):
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        return f"No campaign found with campaign id: {campaign_id}"

    try:
        db.session.delete(campaign)
        db.session.commit()
        return f"Campaign with campaign id: {campaign_id} was deleted successfully"
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(
            f"Could not delete Campaign with campaign id: {campaign_id}. Error: {str(e)}"
        )


def view_campaign_by_campaign_id(campaign_id):
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        return f"No campaign with campaign id: {campaign_id} was found."
    return campaign.to_dict()


def view_all_campaigns_by_creator(creator_id):
    campaigns = Campaigns.query.filter_by(creator_id=creator_id).all()
    return [campaign.to_dict() for campaign in campaigns]


def update_campaign(campaign_id, **kwargs):
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        return f"No campaign found with campaign id: {campaign_id}"

    allowed_fields = [
        "title",
        "description",
        "category",
        "goal_amount",
        "raised_amount",
        "status",
    ]
    for field, value in kwargs.items():
        if field in allowed_fields:
            if field == "category":
                try:
                    campaign.category = (
                        value
                        if isinstance(value, CampaignCategory)
                        else CampaignCategory(value)
                    )
                except Exception as e:
                    raise ValueError(f"Invalid Category {str(e)}")
            elif field == "status":
                try:
                    campaign.status = (
                        value
                        if isinstance(value, CampaignStatus)
                        else CampaignStatus(value)
                    )
                except Exception as e:
                    raise ValueError(f"Invalid Status {str(e)}")
            else:
                setattr(campaign, field, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(
            f"Could not update campaign with campaign id: {campaign_id}. Error: {str(e)}"
        )

    return campaign.to_dict()


def search_campaign_by_title(title):
    campaigns = Campaigns.query.filter(Campaigns.title.ilike(f"%{title}%")).all()
    if not campaigns:
        return f"No campaigns found matching title: {title}"
    return [campaign.to_dict() for campaign in campaigns]


def view_campaigns_by_category(category):
    try:
        if not isinstance(category, CampaignCategory):
            category = CampaignCategory(category)
    except Exception:
        return f"Invalid category: {category}"

    campaigns = Campaigns.query.filter_by(category=category).all()
    if not campaigns:
        return f"No campaigns found for category: {category.value}"

    return [campaign.to_dict() for campaign in campaigns]


def view_all_active_campaigns():
    campaigns = Campaigns.query.filter_by(status=CampaignStatus.ACTIVE).all()
    return [campaign.to_dict() for campaign in campaigns]


def view_all_campaigns():
    return [campaign.to_dict() for campaign in Campaigns.query.all()]


def view_all_completed_campaigns():
    campaigns = Campaigns.query.filter_by(status=CampaignStatus.COMPLETED).all()
    return [campaign.to_dict() for campaign in campaigns]
