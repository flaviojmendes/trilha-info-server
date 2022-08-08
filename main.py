import json
import os
from urllib.request import urlopen
import uuid
from fastapi import FastAPI, HTTPException, Header, Request
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from model.roadmap_view_model import RoadmapViewModel

from model.user_view_model import UserViewModel
from service.roadmap_service import create_roadmap, get_roadmap, get_roadmaps
from service.user_service import create_user, get_user, update_user
app = FastAPI()
app_public = FastAPI(openapi_prefix='/public')
app_private = FastAPI(openapi_prefix='/api')

app.mount("/public", app_public)
app.mount("/api", app_private)

origins = ["*"]




AUTH0_DOMAIN = "trilha-info.us.auth0.com"
API_AUDIENCE = "TrilhaInfoApi"
ALGORITHMS = ["RS256"]


def decode_jwt(token: str):
    token = token.split(" ")[1]
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token_expired")
        except jwt.JWTClaimsError:
            raise HTTPException(status_code=404, detail="invalid_claims")

        except Exception:
            raise HTTPException(status_code=401, detail="invalid_header")
    if payload is not None:
        return payload
    raise HTTPException(status_code=401, detail="invalid_header")


@app_private.middleware("http")
async def verify_user_agent(request: Request, call_next):
    try:
        token = request.headers["Authorization"]
        payload = decode_jwt(token)
        response = await call_next(request)
        return response
    except:
        raise HTTPException(status_code=403, detail="Unauthorized")



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app_private.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app_public.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app_private.get("/user/{user_login}")
async def get_get_user(user_login: str, Authorization=Header(...)):
    if authenticated_user(Authorization, user_login):
        return get_user(user_login)

def authenticated_user(Authorization, user_login):
    token = decode_jwt(Authorization)
    nickname = token["https://trilha.info/nickname"]
    if nickname == user_login:
        return True

    raise HTTPException(status_code=403, detail="Unauthorized")


@app_private.post("/user")
async def post_create_user(user: UserViewModel, Authorization=Header(...)):
    if authenticated_user(Authorization, user.user_login):
        return create_user(user)


@app_private.put("/user")
async def put_update_user(user: UserViewModel, Authorization=Header(...)):
    if authenticated_user(Authorization, user.user_login):
        return update_user(user)



@app_private.post("/roadmap")
async def post_create_roadmap(roadmap: RoadmapViewModel, Authorization=Header(...)):
    if authenticated_user(Authorization, roadmap.owner):
        return create_roadmap(roadmap)

@app_private.get("/roadmap/{user_login}")
async def get_get_roadmaps(user_login: str, Authorization=Header(...)):
    if authenticated_user(Authorization, user_login):
        return get_roadmaps()


@app_public.get("/roadmap/{id}")
async def get_get_roadmap(id: str):
    return get_roadmap(id)


if __name__ == '__main__':
    if(os.environ["ENV"] == 'prod'):
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=8000,
                    reload=True,
                    ssl_keyfile=os.environ["PRIVATE_KEY"],
                    ssl_certfile=os.environ["CERT"]
                    )
    else:
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=8000,
                    reload=True
                    )