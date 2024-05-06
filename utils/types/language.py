from typing import Union

from pydantic import BaseModel


class Language(BaseModel):
    """Containing language name (in English), ISO code (in ISO 639-1) and BCP code (in BCP 47)"""

    name: str

    iso_code: str

    bcp_code: str

    def __init__(self, language: str = "English"):
        # TODO: Implement other languages by retrieving from the database
        language = "English"
        if language == "English":
            language_name = "English"
            iso_code = "en"
            bcp_code = "en-US"

            super(Language, self).__init__(name=language_name, iso_code=iso_code, bcp_code=bcp_code)
        else:
            raise ValueError("Only English is supported")
