from fastapi import FastAPI
from main import print_hi

app = FastAPI()


@app.get("/")
async def hello_world(name):
    return print_hi(name)