from datetime import datetime
from app import db
from app.models.xp_log import XpLog
from app.models.user import User

def add_xp(user: User, xp: int, description: str = "", habit_id: int | None = None):
    """
    Add XP to a user and log it in xp_log.
    """
    if not user:
        raise ValueError("User must be provided to add XP.")

    # ✅ Update user's XP and level using the User model helper
    user.add_xp(xp)

    # ✅ Create XP log
    log_entry = XpLog(
        user_id=user.id,
        habit_id=habit_id,
        xp_amount=xp,
        timestamp=datetime.utcnow()
    )

    db.session.add(log_entry)
    db.session.commit()

