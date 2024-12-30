from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import uvicorn

from items_view import router as items_router
from users.views import router as users_router

app = FastAPI()
app.include_router(items_router, tags=["Items"])
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello World",
    }


@app.post("/calc/add/")
def add(a: int, b: int):
    return {"result": a + b}


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
