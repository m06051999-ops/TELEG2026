from telethon import TelegramClient
from telethon.sessions import SQLiteSession
import os

os.makedirs("sessions", exist_ok=True")

_client = None
_phone_code_hash = None


def create_client(api_id: str, api_hash: str):
    """
    Создает клиента один раз.
    """

    global _client

    if _client is None:

        _client = TelegramClient(
            SQLiteSession("sessions/main_session"),
            int(api_id),
            api_hash
        )

    return _client


def get_client():
    """
    Возвращает уже созданный клиент.
    """

    return _client


async def connect():

    client = get_client()

    if client is None:
        raise RuntimeError("Клиент еще не создан.")

    if not client.is_connected():
        await client.connect()

    return client


async def disconnect():

    client = get_client()

    if client and client.is_connected():
        await client.disconnect()


async def send_code(phone):

    global _phone_code_hash

    client = await connect()

    result = await client.send_code_request(phone)

    _phone_code_hash = result.phone_code_hash


async def sign_in(phone, code, password=""):

    client = await connect()

    from telethon.errors import SessionPasswordNeededError

    try:

        await client.sign_in(
            phone=phone,
            code=code,
            phone_code_hash=_phone_code_hash
        )

    except SessionPasswordNeededError:

        await client.sign_in(password=password)

    return await client.is_user_authorized()


async def check_authorized(api_id, api_hash):

    create_client(api_id, api_hash)

    client = await connect()

    return await client.is_user_authorized()