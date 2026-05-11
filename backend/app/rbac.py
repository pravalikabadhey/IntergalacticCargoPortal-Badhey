from fastapi import Depends, HTTPException, status

from .auth import get_current_user
from .models import User

CLEARANCE_INADEQUATE = "Clearance level inadequate."


def require_role(role: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=CLEARANCE_INADEQUATE,
            )
        return user

    return checker
