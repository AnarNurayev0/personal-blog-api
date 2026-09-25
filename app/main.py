from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status
from .routers import public, admin


app = FastAPI()

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


# ---ROOT URL---

@app.get("/",status_code=status.HTTP_200_OK)
async def root():

    return {"message": "this is the root 'personal-blog-api' "}

