import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator


class LoginUserRequest(BaseModel):

    userId: Optional[str]

    # External access token. If not set, the login will be treated as an anonymous login
    externalToken: Optional[str] = None

    @validator("userId", always=True, allow_reuse=True)
    def generate_random(cls, v):
        # Generate a random user ID to log in anonymously
        return v or str(uuid.uuid4())


class AccessToken(BaseModel):

    token: str


class STTRequest(BaseModel):

    text: str


class STTResult(BaseModel):

    text: Optional[str] = None
    confidence: Optional[float] = 0.0


class STTResults(BaseModel):

    data: List[STTResult]


class InvokeIntent(BaseModel):

    intent: str
    entities: Dict[str, List[str]] = {}


class InvokeData(BaseModel):

    skillId: Optional[str]
    intent: str
    parameters: Dict[str, List[str]] = {}


class ExecuteAfter(BaseModel):
    class ReferenceType(str, Enum):
        SPEECH_END = "SPEECH_END"
        THIS_RESPONSE = "THIS_RESPONSE"

    reference: ReferenceType = ReferenceType.SPEECH_END
    offset: Optional[str] = None


class ExecutionTime(BaseModel):

    executeAfter: Optional[ExecuteAfter] = None
    executeAt: Optional[str] = None


class DelayedClientTask(BaseModel):

    invokeData: InvokeData
    executionTime: ExecutionTime


class SkillResult(BaseModel):

    id: str
    resultType: str
    data: Dict[str, Any] = {}
    delayedClientTask: Optional[DelayedClientTask]
    local: bool = False


class Session(BaseModel):

    id: str
    finished: bool
    ttl: int


class InvokeResult(BaseModel):

    text: str
    stt: Optional[STTResult]
    sttCandidates: Optional[STTResults]
    intent: Optional[InvokeIntent]
    skill: Optional[SkillResult]
    conversationId: str
    cardId: Optional[str]
    session: Session
    traceId: Optional[str] = Field(alias="@smarthub.traceId")
    status: Optional[str]
