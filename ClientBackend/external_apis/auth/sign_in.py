
import aiohttp

from external_apis.common import TIMEOUT


def create_payload(email, password):
    return {
        "operationName": "SignIn",
        "variables": {
            "email": email,
            "password": password,
        },
        "query":
        "mutation SignIn($email: String!, $password: String!) {\n  signIn(email: $email, password: $password) {\n    id\n    name\n    email\n    phoneNumber\n    accessToken\n    createdAt\n    __typename\n  }\n}",
    }


async def exec(email, password):
    url = "https://graphql-dash-wrapper.stellate.sh/graphql"

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.post(url, json=create_payload(email, password)) as response:
            return await response.json()
