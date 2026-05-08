from fastapi import APIRouter, HTTPException
from services.weather_service import get_weather

router = APIRouter()


@router.get("/weather")
async def weather():
    data = await get_weather()
    if "error" in data:
        raise HTTPException(status_code=502, detail=data["error"])
    return data
