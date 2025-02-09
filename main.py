import uvicorn
from typing import Union
from fastapi import Depends, FastAPI, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
from dotenv import load_dotenv
load_dotenv()

# load environment variables
if "PORT" not in os.environ.keys():
    port = 8000
else:
    port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI(
    title="fastapi-template",
    description="Template repo for FastAPI.",
    version="0.0.1",
    license_info={
        "name": "AGPL-3.0 license",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)
key_query_scheme = APIKeyHeader(name="key")


def some_function():
    """some function that does something."""


def required_headers(
        username: str = Header(),
        password: str = Header()):
    """Headers required to use the API."""
    return username, password


@app.get("/", include_in_schema=False)
async def docs_redirect():
    """Redirect base URL to docs."""
    return RedirectResponse(url='/docs')


class MyPayload(BaseModel):
    #integer_field: int
    are_you_happy: bool
    text_field: str


@app.post("/post-something")
async def post_something(payload: MyPayload, dependencies=Depends(required_headers)):
    """POST Something. This method is meant for you to send the data of the registration in this format, so that it will be stored in the database. """
    
    # do something with input_data
    #new_string = payload.text_field + " Wessel is here " + str(payload.integer_field)
    
    if payload.text_field == 'hello':
        output = 'hello to you as well'
    else:
        output = 'bye bye'

    return JSONResponse(status_code=200, content={"message": "Success", "output": output})


@app.get("/get-something")
async def get_something(id: int, api_key: str = Depends(key_query_scheme)):
    """GET Something."""
    
    # check API key
    if api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(status_code=200, content={"message": f"this is the data of registration {id}"})

@app.get("/what-will-we-eat-today")
async def get_something(happiness: int):
    """GET Your Awesome Food Of Today. Choose a number of 1 to 5."""
    
    if happiness > 5 or happiness < 1:
        raise HTTPException(status_code=422, detail="The number is too big or too small")
    # check API key
    # if api_key != os.environ["API_KEY"]:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    if happiness == 1:
        output = 'chocolate'
    elif happiness == 2:
        output = 'pizza'
    elif happiness == 3:
        output = 'couscous'
    elif happiness == 4:
        output = 'salad'
    else:
        output = 'ice cream!!!!'
    
    return JSONResponse(status_code=200, content={"message": f"The best food for you is: {output}"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)