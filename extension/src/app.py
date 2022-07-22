from fastapi import FastAPI
from pydantic.types import List
import sqlalchemy as db
import sqlalchemy.sql as sql
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class PageContent(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.post("/summary")
async def summarize(content: PageContent):
    return PageContent(text=(content.text + ' ' + content.text))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
