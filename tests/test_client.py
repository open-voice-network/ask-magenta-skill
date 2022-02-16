import pytest
from magenta.voice.client import ApiClient


@pytest.mark.asyncio
async def test_login():
    response = await ApiClient()._test_login()
    assert response.token.startswith("eyJhbGciOiJIUzI1NiJ9")


@pytest.mark.asyncio
async def test_invoke_weather():
    async with ApiClient() as client:
        await client.connect()
        response = await client.invoke_text("Wie ist das Wetter in Bonn?")
        assert response.text.startswith("Hier kommt die Vorhersage für heute")
