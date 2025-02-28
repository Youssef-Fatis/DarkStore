import asyncio
from . import sign_in


def get_token(email, password):
    response_body = asyncio.run(sign_in.exec(email, password))
    return response_body["data"]["signIn"]["accessToken"]
