# Yandex ID async oauth

Асинхронное решения для регистрации через Яндекс Паспорт.
Это пример использования через FastAPI

## Запуск:

Перед работай укажите client_id, client_secret и redirect_url:
```py
yandex_oauth = AsyncYandexOAuth(
    client_id="",
    client_secret="",
    redirect_uri='http://127.0.0.1:8000/oauth' #Тут указан redirect_url который используется в коде
)
```

## Используемые библиотеки

yandexid - https://github.com/LulzLoL231/YandexID
fastapi - https://fastapi.tiangolo.com/ru/tutorial/

## HELP
TON - `UQAwz0_VswIBOfT3UpooQ6AF5gUI-Nyjdmahc6rNu0Fx3Mi-`
