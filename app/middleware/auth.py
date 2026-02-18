# from fastapi import Request, HTTPException, Depends
# from fastapi.security import HTTPBearer
# from okta_jwt_verifier import AccessTokenVerifier
# from app.config.settings import settings

# # Initialize Security and Verifier
# security = HTTPBearer()

# verifier = AccessTokenVerifier(
#     issuer=settings.OKTA_ISSUER,
#     audience=settings.OKTA_AUDIENCE,
# )

# async def authenticate(request: Request, credentials=Depends(security)):
#     """
#     Dependency to verify Okta JWT tokens and inject user claims into the request state.
#     """
#     token = credentials.credentials

#     try:
#         # Verify the token asynchronously
#         claims = await verifier.verify(token)
#     except Exception:
#         raise HTTPException(
#             status_code=401, 
#             detail="Invalid or expired Okta token"
#         )

#     # Attach user data to request state for use in route handlers
#     request.state.user = {
#         "email": claims.get("sub"),
#         "name": claims.get("name"),
#         "groups": claims.get("groups", []),
#     }

#     return request.state.user

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from okta_jwt_verifier import AccessTokenVerifier
from sqlalchemy.orm import Session
import logging

from app.config.settings import settings
from app.config.db import SessionLocal
from app.modules.users.service import get_user_by_email
from app.modules.users.models import User

logger = logging.getLogger(__name__)

security = HTTPBearer()

verifier = AccessTokenVerifier(
    issuer=settings.OKTA_ISSUER,
    audience=settings.OKTA_AUDIENCE,
)


async def authenticate(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Verify Okta JWT access token,
    auto-provision user if not exists,
    and attach user info to request.state.
    """
    token = credentials.credentials

    # try:
    #     claims = await verifier.verify(token)

    # except Exception as e:
    #     logger.warning(f"JWT verification failed: {e}")
    #     raise HTTPException(status_code=401, detail="Invalid or expired Okta token")

    # # ==============================
    # # AUTO-PROVISION USER
    # # ==============================
    # db: Session = SessionLocal()

    # try:
    #     email = claims.get("sub")
    #     full_name = claims.get("name")

    #     user = get_user_by_email(db, email)

    #     if not user:
    #         user = User(
    #             email=email,
    #             full_name=full_name,
    #             role="technician",  # default role
    #         )
    #         db.add(user)
    #         db.commit()
    #         db.refresh(user)

    # finally:
    #     db.close()

    # # ==============================
    # # Attach to request.state
    # # ==============================
    # request.state.user = {
    #     "id": user.id,
    #     "email": user.email,
    #     "name": user.full_name,
    #     "role": user.role,
    #     "groups": claims.get("groups", []),
    # }

    # return request.state.user
# from fastapi import Request, HTTPException, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt
# import requests

# from app.config.settings import settings

# security = HTTPBearer()

# # Fetch Okta public keys (JWKS)
# JWKS_URL = f"{settings.OKTA_ISSUER}/v1/keys"
# jwks = requests.get(JWKS_URL).json()


# async def authenticate(
#     request: Request,
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ):
#     """
#     Verify JWT access token using Okta JWKS
#     """

#     token = credentials.credentials

#     try:
#         # Get token header
#         header = jwt.get_unverified_header(token)

#         # Match key by kid
#         key = next(
#             k for k in jwks["keys"] if k["kid"] == header["kid"]
#         )

#         # Decode and verify token
#         claims = jwt.decode(
#             token,
#             key,
#             algorithms=["RS256"],
#             audience=settings.OKTA_AUDIENCE,
#             issuer=settings.OKTA_ISSUER,
#         )

#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Token invalid: {str(e)}")

#     # Attach user info to request
#     request.state.user = {
#         "email": claims.get("sub"),
#         "name": claims.get("name"),
#         "groups": claims.get("scp", []),
#     }
#     print("AUTH USER:", request.state.user)

#     return request.state.user
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests

from app.config.settings import settings
from app.config.db import SessionLocal
from app.modules.users.service import get_user_by_email
from app.modules.users.models import User

security = HTTPBearer()

JWKS_URL = f"{settings.OKTA_ISSUER}/v1/keys"
jwks = requests.get(JWKS_URL).json()


async def authenticate(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        header = jwt.get_unverified_header(token)

        key = next(
            k for k in jwks["keys"] if k["kid"] == header["kid"]
        )

        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.OKTA_AUDIENCE,
            issuer=settings.OKTA_ISSUER,
        )

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token invalid: {str(e)}")

    db = SessionLocal()

    try:
        email = claims.get("sub")
        user = get_user_by_email(db, email)

        if not user:
            # auto-provision
            user = User(
                email=email,
                full_name=claims.get("email"),
                role="technician",  # default role
            )
            db.add(user)
            db.commit()
            db.refresh(user)

    finally:
        db.close()

    request.state.user = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }

    print("AUTH USER:", request.state.user)

    return request.state.user
