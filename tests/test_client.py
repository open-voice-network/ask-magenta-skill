from magenta.voice.client import ApiClient


def test_login():
    response = ApiClient()._test_login()
    assert response.token.startswith("eyJhbGciOiJIUzI1NiJ9")


def test_invoke_weather():
    with ApiClient() as client:
        client.connect()
        response = client.invoke_text("Wie ist das Wetter in Bonn?")
        assert response.text[:35] in (
            "Hier kommt die Vorhersage für heute",
            "In der nächsten Stunde bleibt es in",
            "Hier kommt das aktuelle Wetter: In ",
        )
