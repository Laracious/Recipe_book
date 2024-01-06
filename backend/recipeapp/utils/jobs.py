from datetime import datetime
from recipeapp import db, scheduler
from recipeapp.models.jwt_blocklist import TokenBlocklist


# Schedule a job to delete expired tokens every day
@scheduler.task("cron", id="delete_expired_tokens", day_of_week="*", hour=0, minute=0)  # nopep8
def delete_expired_tokens():
    """
    Scheduled job to delete expired tokens from the blocklist.

    This function queries the TokenBlocklist table and deletes entries where
    the `expires_at` timestamp is earlier than the current time. The job runs
    every day at midnight.
    """
    expired_tokens = TokenBlocklist.query.filter(
        TokenBlocklist.expires_at < datetime.utcnow()).all()
    for token in expired_tokens:
        db.session.delete(token)
    db.session.commit()