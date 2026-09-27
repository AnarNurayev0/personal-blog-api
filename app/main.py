# from fastapi.middleware.cors import CORSMiddleware
from .routers import public, admin, articles
from fastapi import FastAPI, status, Request
from .limiter import limiter

tags_metadata = [
    {
        "name": "Admin Articles",
        "description": "Admin endpoints for managing blog posts.",
    },
    {
        "name": "Admin Management",
        "description": "User administration, authentication, and role management.",
    },
    {
        "name": "System",
        "description": "Health checks and root API status.",
    },
    {
        "name": "Public Articles",
        "description": "Public endpoints for browsing and reading blog posts."
    }
]

app = FastAPI(
    title="Personal Blog API",
    description="Backend REST API for blog management",
    version="1.0.0",
    openapi_tags=tags_metadata
)

# === ROUTERS ===
app.include_router(articles.router)
app.include_router(public.router)
app.include_router(admin.router)


# === CORSMiddleware ===
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# --- ROOT URL ---
@app.get("/", status_code=status.HTTP_200_OK, tags=["System"])
@limiter.limit("20/minute")
async def root(request: Request):

    return {"message": "this is the root 'personal-blog-api' "}


# --- CHECK HEALTH ---
@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
@limiter.limit("20/minute")
async def health(request: Request):
    return {"status": "ok"}
