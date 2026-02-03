from pydantic import BaseModel, Field

class GeoPoint(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class RadiusSearch(BaseModel):
    center: GeoPoint
    radius_km: float = Field(..., gt=0)

class RectangleSearch(BaseModel):
    north_east: GeoPoint  # Северо-восточный угол
    south_west: GeoPoint  # Юго-западный угол