from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class MongoBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class User(MongoBaseModel):
    username: str
    email: EmailStr
    password: str
    is_provider: bool = False
    location: Optional[dict] = None # GeoJSON Point: { type: "Point", coordinates: [lon, lat] }
    address: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    is_admin: bool = False

class Service(MongoBaseModel):
    provider_email: str
    title: str
    description: str
    category: str
    price: float
    location: Optional[dict] = None # GeoJSON Point: { type: "Point", coordinates: [lon, lat] }
    address: Optional[str] = None
    provider_phone: Optional[str] = None
    provider_image: Optional[str] = None
    skills: List[str] = []
    certificate: Optional[str] = None
    id: Optional[str] = Field(None, alias="_id")

class GeoLocation(BaseModel):
    latitude: float
    longitude: float
