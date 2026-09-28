from pydantic import BaseModel, Field


class NeedsRequest(BaseModel):
    region: str = Field(min_length=1)


class YearMetrics(BaseModel):
    total: int
    replacement: int
    additional: int
