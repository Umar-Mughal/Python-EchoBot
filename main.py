from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, requests, jwt, time

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DISCORD_CLIENT_ID = "1053517227783098488"
DISCORD_CLIENT_SECRET = "_L43zKRHeGiJES2o1sJj0VYwb-jdXW_e"
DISCORD_REDIRECT_URI = "http://localhost:8080/callback" #"http://localhost:8080/callback"

SECRET = "697822579A70EAFB7A67B55E0E399D605EB2959841116E00F1D11DC47EA5CECA"

@app.get("/callback")
async def callback(request: Request, response: Response):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="authentification failed")

    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": "identify"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(token_url, data=data, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Error exchanging authorization code for access token")

    access_token = r.json()["access_token"]
    user_info_url = "https://discord.com/api/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}

    r = requests.get(user_info_url, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="authentification failed")

    userId = r.json()["id"]
    jwt_token = jwt.encode({"userId": userId, "exp": time.time() + 3600}, SECRET, algorithm="HS256")

    response.set_cookie("jwt_token", jwt_token)
    time.sleep(1)
    return {"message": "authentification succesful"}


@app.get("/load")
async def load(request: Request):
    try:
        payload = jwt.decode(request.cookies.get("jwt_token"), SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=400, detail="error")
    ##groups get from username
    groups = {
        "clients": [
            {
            "_id": "fa3f095e-b40d-42e3-8b03-54653bffd72d",
            "name": "TEST",
            "channelIds": [
                {
                "_id": "0e70aaad-756c-4300-bcdd-ba6f53033c0c",
                "webhook": "https://discord.com/api/webhooks/1059292460762812517/xkWz4GBn6Jk05HZFhHCGWEzC_20sgIJ4hmsnKVFoIi_83fwHdkT7W0fE",
                "marketplace": "US",
                "merchGroup": "US",
                "productType": "FOOTWEAR",
                "channelType": "LAUNCH",
                "status": "PENDING",
                "filter": {
                    "isLaunch": [
                        True,
                        False
                    ],
                    "isOOS": [
                        False
                    ],
                    "isPSTD": [
                        True,
                        False
                    ],
                    "unfiltered": True,
                    "skus": {
                    "positive": [],
                    "negative": []
                    },
                    "kws": {
                    "positive": [],
                    "negative": []
                    }
                }
                }
            ]
            },
            {
            "_id": "28c3f0a2-c0cf-455a-9e1d-798a393bf701",
            "name": "TEST2",
            "channelIds": [
                {
                "_id": "d6c0647e-4cee-4c29-899c-e514c794f7fa",
                "webhook": "https://discord.com/api/webhooks/1059292460762812517/xkWz4GBn6Jk05HZFhHCGWEzC_20sgIJ4hmsnKVFoIi_83fwHdkT7W0fE",
                "marketplace": "CA",
                "merchGroup": "XP",
                "productType": "FOOTWEAR",
                "channelType": "FRONTEND",
                "status": "RUNNING",
                "filter": {
                    "isLaunch": [
                    True,
                    False
                    ],
                    "isOOS": [
                    False
                    ],
                    "isPSTD": [
                    True,
                    False
                    ],
                    "unfiltered": False,
                    "skus": {
                    "positive": [],
                    "negative": []
                    },
                    "kws": {
                    "positive": [],
                    "negative": []
                    }
                }
                },
                {
                "_id": "ff380a36-1a21-4779-b53a-315a5accfc27",
                "webhook": "https://discord.com/api/webhooks/1059292460762812517/xkWz4GBn6Jk05HZFhHCGWEzC_20sgIJ4hmsnKVFoIi_83fwHdkT7W0fE",
                "marketplace": "CA",
                "merchGroup": "XP",
                "productType": "FOOTWEAR",
                "channelType": "FRONTEND",
                "status": "RUNNING",
                "filter": {
                    "isLaunch": [
                    True,
                    False
                    ],
                    "isOOS": [
                    False
                    ],
                    "isPSTD": [
                    True,
                    False
                    ],
                    "unfiltered": False,
                    "skus": {
                    "positive": [],
                    "negative": []
                    },
                    "kws": {
                    "positive": [],
                    "negative": []
                    }
                }
                }
            ]
            }
        ]
        }

    return {"clients": groups}

@app.post("/update")
async def update(request: Request):
    try:
        payload = jwt.decode(request.cookies.get("jwt_token"), SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=400, detail="error")

    try:
        body = await request.json()
    except:
        raise HTTPException(status_code=400, detail="invalid body")

    updated = False
    group = body.get("client")

    ## group update

    return {"updated": updated}

@app.post("/i/{redirectId}")
async def redirect(request: Request, redirectId: str):
    try:
        body = await request.json()
    except:
        raise HTTPException(status_code=400, detail="invalid body")

    redirect = {
        "_id": "lpfiqk",
        "channelId": "11b75bc0-bf81-45e7-be98-db7c1cefe682",
        "productId": "DQ8417-071_EU",
        "styleColor": "DQ8417-071",
        "merchGroup": "EU",
        "marketplace": "CZ",
        "channels": [
            "SNKRS",
            "NikeApp",
            "Nike.com",
            "Nike Store Experiences"
        ],
        "slug": "air-jordan-1-mid-se-shoes-NMMxDk",
        "redirectCount": {
            "total": 0,
            "webstore": 0,
            "nikeapp": 0,
            "snkrs": 0,
            "atc": 0,
            "goat": 0,
            "stockx": 0
        }
    }
    if redirect == None:
        raise HTTPException(status_code=404, detail="redirect not found")
    else:
        redirectType = body.get("type")
        match redirectType:
            case "nikeweb":
                data = "https://www.nike.com/launch/t/" + redirect["slug"] if "SNKRS" in redirect["channels"] and "Nike.com" not in redirect["channels"] else "https://www.nike.com/t/" + redirect["slug"] + "/" + redirect["styleColor"]
            case "nikeapp":
                data = "mynike://x-callback-url/product-details?style-color=" + redirect["styleColor"]
            case "snkrs":
                data = "snkrs://product/" + redirect["styleColor"]
            case "atc":
                data = redirect["productId"]
            case "stockx":
                data = "https://stockx.com/search?s=" + redirect["styleColor"]
            case "goat":
                data = "https://www.goat.com/search?query=" + redirect["styleColor"]
            case _:
                raise HTTPException(status_code=400, detail="invalid type")

        return {"message": data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)