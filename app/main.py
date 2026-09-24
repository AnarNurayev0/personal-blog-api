from fastapi import FastAPI, status
from .routers import public, admin

app = FastAPI()

app.include_router(public.router)
app.include_router(admin.router)


# ---ROOT URL---

@app.get("/",status_code=status.HTTP_200_OK)
async def root():

    return {"message": "this is the root 'personal-blog-api' "}

