from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()
"""
TODO: Issue #14 
This API is a placeholder for local testing before ML Inference Service is ready

To run: 
    - $ python3 app.py
"""

class PageContent(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.post("/summary")
async def summarize(content: PageContent):
    response = PageContent(text=(content.text + ' ' + content.text))
    print(response)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
