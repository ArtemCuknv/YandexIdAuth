from fastapi import Request, FastAPI
from starlette import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from yandexid import AsyncYandexOAuth

yandex_oauth = AsyncYandexOAuth(
    client_id="",
    client_secret="",
    redirect_uri='http://127.0.0.1:8000/oauth'
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('start')
    yield
    print('end')

app = FastAPI()

secret_key = "CHANGE_ME_TO_RANDOM_LONG_SECRET"
app.add_middleware(SessionMiddleware, secret_key=secret_key)

@app.get("/")
async def index(request: Request):
    auth_url = yandex_oauth.get_authorization_url()

    return RedirectResponse(url= auth_url)


@app.get('/oauth')
async def auth(request: Request, code: str | None = None, error: str | None = None):
    if error:
        return {"error": error}
    if not code:
        return {"error": "No code provided"}

    try:
        token_response = await yandex_oauth.get_token_from_code(code)

        access_token = token_response.access_token
        refresh_token = token_response.refresh_token

        return {
            "status": "Success",
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except Exception as e:
        return {"status": "Auth failed", "detail": str(e)}