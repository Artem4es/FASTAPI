from pydantic import BaseModel


class RespUrlModel(BaseModel):
    download_link: str
