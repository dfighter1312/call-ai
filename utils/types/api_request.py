from pydantic import BaseModel


class APIRequest(BaseModel):

    path: str = '/'
    """API path"""

    user_id: int
    """User ID"""

    scenario_id: int
    """Scenario ID"""

    language: str = "en-US"
    """Language code"""
