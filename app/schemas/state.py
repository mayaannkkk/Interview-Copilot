from typing_extensions import TypedDict
from typing import Optional

class InterviewState(TypedDict):
    query: str
    route: Optional[str]
    response: Optional[str]