from typing import Optional
import httpx

from . import LoginUserRequest, AccessToken, STTRequest, InvokeResult
from .config import settings


class ApiException(Exception):
    """Signals technical API error"""


class ApiClient(httpx.Client):
    """
    API client
    """

    _token: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = settings.base_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "ApiKey": settings.api_key,
        }

    def _test_login(self) -> AccessToken:
        user = LoginUserRequest()
        url = settings.user_api.format(testing=True, testing_secret=settings.testing_secret)
        result = self.post(url, content=user.json())
        return AccessToken.parse_obj(result.json())

    def connect(self) -> "ApiClient":
        self._token = self._test_login().token
        self.headers["Authorization"] = f"Bearer {self._token}"
        return self

    def disconnect(self) -> "ApiClient":
        self._token = None
        return self

    def is_connected(self) -> bool:
        return self._token is not None

    def invoke_text(
        self, text: str, intent: bool = True, skill: bool = True, session_id: str = None
    ) -> InvokeResult:
        if not self.is_connected():
            raise ApiException("Not connected")

        request = STTRequest(text=text)
        url = settings.invoke_text.format(intent=intent, skill=skill, sessionId=session_id)
        result = self.post(url, content=request.json())
        return InvokeResult.parse_obj(result.json())
