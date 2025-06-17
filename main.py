from fastapi import FastAPI
from routes import expenses  # import the router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(expenses.router)  # include the routes

@app.get("/")
def read_root():
    return {"message": "Welcome to the Split Expense App"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
