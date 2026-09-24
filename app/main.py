from fastapi import FastAPI, status

app = FastAPI()


# ---ROOT URL---

@app.get("/",status_code=status.HTTP_200_OK)
async def root():

    return {"message": "this is the root"}

