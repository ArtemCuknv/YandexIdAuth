from fastapi import Request, FastAPI
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from yandexid import AsyncYandexOAuth, YandexID
import uvicorn

yandex_oauth = AsyncYandexOAuth(
    client_id="",
    client_secret="",
    redirect_uri='http://127.0.0.1:8000/oauth'
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('start')
    "Тут можно инициализировать пулл соеденения с дб"
    yield
    print('end')
    "А тут закрывать"

app = FastAPI()

secret_key = "CHANGE_ME_TO_RANDOM_LONG_SECRET" #ОБЯЗАТЕЛЬНО ПОМЕНЯТЬ!!!
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
        yandex_user = YandexID(access_token)
        user_info = yandex_user.get_user_info_json()

        return {
            "status": "Success",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_info.id,
            "user_info": user_info
        }
    except Exception as e:
        return {"status": "Auth failed", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) # reload можно убрать