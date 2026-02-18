# from fastapi import Request, HTTPException, Depends
# from typing import List, Callable
# from app.middleware.auth import authenticate


# def require_roles(*allowed_roles: str) -> Callable:
#     """
#     FastAPI dependency to enforce role-based access using Okta groups.
#     Usage:
#         Depends(require_roles("admin"))
#         Depends(require_roles("admin", "supervisor"))
#     """

#     async def role_checker(request: Request, user=Depends(authenticate)):
#         if not user:
#             raise HTTPException(status_code=401, detail="Unauthorized")

#         user_role: List[str] = user.get("role", [])

#         # Check intersection between allowed roles and user groups
#         if not any(role in user_role for role in allowed_roles):
#             raise HTTPException(status_code=403, detail="Forbidden")

#         return user  # allow route to access user info

#     return role_checker

from fastapi import Request, HTTPException, Depends
from typing import Callable
from app.middleware.auth import authenticate


def require_roles(*allowed_roles: str) -> Callable:
    """
    FastAPI dependency to enforce role-based access
    using database-stored user role.
    """

    async def role_checker(request: Request, user=Depends(authenticate)):
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_role = user.get("role")

        print("USER ROLE:", user_role)
        print("ALLOWED:", allowed_roles)

        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return role_checker
