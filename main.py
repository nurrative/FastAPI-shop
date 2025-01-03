from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from core.models import Base, db_helper
from items_view import router as items_router
from users.views import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Load the ML model
    # ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield


app = FastAPI(lifespan=lifespan)
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
