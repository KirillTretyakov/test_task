import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status

from app.config import Settings, get_settings
from app.repository import get_needs
from app.schemas import NeedsRequest, YearMetrics

app = FastAPI(title="Regional Staffing Needs API", version="1.0.0")


async def verify_app_token(
    settings: Annotated[Settings, Depends(get_settings)],
    x_app_token: Annotated[str | None, Header()] = None,
) -> None:
    if x_app_token is None or not secrets.compare_digest(x_app_token, settings.app_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing application token",
        )


@app.post(
    "/api/v1/staffing/needs",
    response_model=dict[str, YearMetrics],
    dependencies=[Depends(verify_app_token)],
)
async def read_staffing_needs(request: NeedsRequest) -> dict[str, YearMetrics]:
    needs = get_needs(request.region)
    if needs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Данные по региону '{request.region}' не найдены в базе данных.",
        )
    return needs
