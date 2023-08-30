from typing import Union

from pydantic import BaseModel, Field


class HospitalCoordinatesSchema(BaseModel):
    latitude: float = Field(alias='lat')
    longitude: float = Field(alias='lng')


class HospitalIdAndCoordinatesSchema(BaseModel):
    hospital_id: Union[str, int] = Field(alias='id')
    latlon: HospitalCoordinatesSchema = Field(alias='latLang')


class HospitalIdAndCoordinatesResponseSchema(BaseModel):
    markers: list[HospitalIdAndCoordinatesSchema]
