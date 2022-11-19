import os 
from fastapi import FastAPI, Body, HTTPException, status 
from fastapi.responses import Response, JSONResponse 
from fastapi.encoders import jsonable_encoder 
from pydantic import BaseModel, Field, EmailStr 
from bson import ObjectId 
from typing import Optional, List 
import motor.motor_asyncio

app = FastAPI() 
#client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
MONGODB_URL ='mongodb+srv://arbeyrios:eljers0n!!@cluster0.j1a4mkv.mongodb.net/test'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL) 
db = client.automoviles

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
    def __modify_schema__(cls, field_schema):        
        field_schema.update(type="string")

class AutoModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Marca: str = Field(...)
    Color: str = Field(...)
    Precio: str = Field(...)
    Modelo: str = Field(...)
    Cilindraje: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                 "Marca": "Chevrolet",                
                 "Color": "Negro",                
                 "Precio": "45.000.000",                
                 "Modelo": "2010",
                 "Cilindraje": "3400cc"
            }
        }

class UpdateAutoModel(BaseModel):
    Marca: Optional[str]
    Color: Optional[str]
    Precio: Optional[int]
    Modelo: Optional[str]
    Cilindraje: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Marca": "Chevrolet",
                "Color": "Negro",
                "Precio": "45.000.000",
                "Modelo": "2010",
                "Cilindraje":"3400cc"
            }
        }

@app.post("/", response_description="Add new auto",response_model=AutoModel)
async def create_auto(auto: AutoModel = Body(...)):
    auto = jsonable_encoder(auto)
    new_auto = await db["automoviles"].insert_one(auto)
    created_auto = await db["automoviles"].find_one({"_id":new_auto.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED,content=created_auto)

@app.get("/", response_description="List all autos", response_model=List[AutoModel])
async def list_autos():
    autos = await db["tripulantes"].find().to_list(1000)
    return autos

@app.get("/{id}", response_description="Get a single auto", response_model=AutoModel)     
async def show_auto(id: str):
    if (auto := await db["automoviles"].find_one({"_id": id})) is not None:
        return auto

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

@app.put("/{id}", response_description="Update a auto",response_model=AutoModel)
async def update_auto(id: str, auto: UpdateAutoModel = Body(...)):
    auto = {k: v for k, v in auto.dict().items() if v is not None}
    if len(auto) >= 1:
        update_result = await db["automoviles"].update_one({"_id": id}, {"$set": auto})
        if update_result.modified_count == 1:
            if (updated_auto := await db["automoviles"].find_one({"_id": id})) is not None:
                return updated_auto
                if (existing_auto := await db["automoviles"].find_one({"_id": id})) is not None:
                    return existing_auto
                raise HTTPException(status_code=404, detail=f"Auto {id} not found")

@app.delete("/{id}", response_description="Delete a Car")
async def delete_car(id: str):
    delete_result = await db["automoviles"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Car {id} not found")