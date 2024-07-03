from fastapi import FastAPI
from llm_controller import router as llm_contoller_router

app = FastAPI(title="Radiologist Agent API", version="0.1.0" )

app.include_router(llm_contoller_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


#  uvicorn main:app --reload