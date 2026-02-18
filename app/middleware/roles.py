from fastapi import Request, HTTPException


# def require_roles(*allowed_roles: str):
#     def dependency(request: Request):
#         user = getattr(request.state, "user", None)
#         if not user:
#             raise HTTPException(status_code=401, detail="Unauthorized")

#         groups = user.get("groups", [])
#         if not any(role in groups for role in allowed_roles):
#             raise HTTPException(status_code=403, detail="Forbidden")

#     return dependency
def require_roles(*allowed_roles: str):
    def dependency(request: Request):
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        groups = user.get("groups", [])
        if not any(role in groups for role in allowed_roles):
            raise HTTPException(status_code=403, detail="Forbidden")

        return user  # useful in routes

    return dependency
