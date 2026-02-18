# import secrets
# import urllib.parse
# import httpx
# from jose import jwt

# from fastapi import FastAPI, Request, HTTPException
# from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from okta_jwt_verifier import AccessTokenVerifier

# from app.config.settings import settings

# # # NEW IMPORT
# # from app.modules.locations.router import router as locations_router
# from app.config.db import Base, engine 
# # from app.modules.locations import models as location_models
# # from app.modules.prioritycodes import models as priority_models
# # from app.modules.problemcodes import models as problem_models

# # =========================================================
# # IMPORT MODELS FOR TABLE CREATION
# # =========================================================
# from app.modules.locations import models as location_models
# from app.modules.prioritycodes import models as priority_models
# from app.modules.problemcodes import models as problem_models
# from app.modules.matrixproblemcodes import models as matrix_problem_models

# app = FastAPI(title="CMMS Backend")

# # Create tables 
# location_models.Base.metadata.create_all(bind=engine)
# priority_models.Base.metadata.create_all(bind=engine)
# problem_models.Base.metadata.create_all(bind=engine)
# matrix_problem_models.Base.metadata.create_all(bind=engine)


# # Serve frontend
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ISSUER = settings.OKTA_ISSUER
# AUDIENCE = settings.OKTA_AUDIENCE


# # =========================================================
# # ROOT → SERVE FRONTEND
# # =========================================================
# @app.get("/")
# async def root():
#     return FileResponse("app/static/index.html")


# # =========================================================
# # LOGIN → REDIRECT TO OKTA
# # =========================================================
# @app.get("/login")
# async def login():
#     state = secrets.token_urlsafe(16)

#     params = {
#         "client_id": settings.OKTA_CLIENT_ID,
#         "response_type": "code",
#         "scope": "openid profile email",
#         "redirect_uri": settings.OKTA_REDIRECT_URI,
#         "state": state,
#     }

#     url = f"{ISSUER}/v1/authorize?{urllib.parse.urlencode(params)}"
#     return RedirectResponse(url)


# # =========================================================
# # CALLBACK → EXCHANGE CODE FOR TOKEN
# # =========================================================
# @app.get("/callback")
# async def callback(code: str):
#     token_url = f"{ISSUER}/v1/token"

#     data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": settings.OKTA_REDIRECT_URI,
#         "client_id": settings.OKTA_CLIENT_ID,
#         "client_secret": settings.OKTA_CLIENT_SECRET,
#     }

#     async with httpx.AsyncClient() as client:
#         resp = await client.post(token_url, data=data)
#         resp.raise_for_status()
#         tokens = resp.json()

#     access_token = tokens["access_token"]

#     response = RedirectResponse("/")

#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         samesite="lax",
#         secure=False,  # True only in HTTPS production
#     )

#     return response


# # =========================================================
# # VERIFY USER
# # =========================================================
# # @app.get("/me")
# # async def me(request: Request):
# #     token = request.cookies.get("access_token")

# #     if not token:
# #         raise HTTPException(status_code=401, detail="Not authenticated")

# #     verifier = AccessTokenVerifier(issuer=ISSUER, audience=AUDIENCE)

# #     try:
# #         claims = await verifier.verify(token)
# #     except Exception:
# #         raise HTTPException(status_code=401, detail="Invalid token")

# #     return JSONResponse(claims)



# @app.get("/me")
# async def me(request: Request):
#     token = request.cookies.get("access_token")

#     if not token:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     try:
#         # Decode WITHOUT verifying signature first (to inspect claims)
#         unverified = jwt.get_unverified_claims(token)
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     return unverified



# # =========================================================
# # SIMPLE TEST PAGE
# # =========================================================
# @app.get("/app")
# async def app_home():
#     return {"message": "You are logged in to CMMS backend"}

# # =========================================================
# # ADD ROUTERS
# # =========================================================
# from app.modules.locations.router import router as locations_router
# from app.modules.prioritycodes.router import router as prioritycodes_router
# from app.modules.problemcodes.router import router as problemcodes_router
# from app.modules.matrixproblemcodes.router import router as matrix_problem_codes_router


# app.include_router(locations_router)
# app.include_router(prioritycodes_router)
# app.include_router(problemcodes_router)
# app.include_router(matrix_problem_codes_router)

# # /* NEW */
# from fastapi import FastAPI
# from app.services.scheduler import start_scheduler

# app = FastAPI(title="CMMS API")

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

from app.config.db import Base, engine
from app.config.settings import settings
from app.services.scheduler import start_scheduler

# Import routers
from app.modules.assets.router import router as assets_router
from app.modules.locations.router import router as locations_router
from app.modules.workorders.router import router as workorders_router
from app.modules.pm.router import router as pm_router
from app.modules.prioritycodes.router import router as priority_router
from app.modules.problemcodes.router import router as problem_router
from app.modules.matrixproblemcodes.router import router as matrix_router
from app.modules.users.router import router as users_router


# -------------------------------------------------
# Create FastAPI app
# -------------------------------------------------
app = FastAPI(
    title="CMMS API",
    version="1.0.0"
)


# -------------------------------------------------
# CORS
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Include Routers
# -------------------------------------------------
app.include_router(assets_router)
app.include_router(locations_router)
app.include_router(workorders_router)
app.include_router(pm_router)
app.include_router(priority_router)
app.include_router(problem_router)
app.include_router(matrix_router)
app.include_router(users_router)


# -------------------------------------------------
# Static Files
# -------------------------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("app/static/index.html")


# -------------------------------------------------
# OAuth Callback (Backend-handled)
# -------------------------------------------------
@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return {"error": "Authorization code missing"}

    token_url = f"{settings.OKTA_ISSUER}/v1/token"

    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.OKTA_REDIRECT_URI,
            "client_id": settings.OKTA_CLIENT_ID,
            "client_secret": settings.OKTA_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        return {"error": "Failed to retrieve access token", "details": token_data}

    return RedirectResponse(
        url=f"/static/dashboard.html?token={access_token}"
    )


# -------------------------------------------------
# Startup Event
# -------------------------------------------------
@app.on_event("startup")
def startup_event():
    # Create tables (dev only)
    Base.metadata.create_all(bind=engine)

    # Start scheduler
    start_scheduler()


# -------------------------------------------------
# Health Check
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

