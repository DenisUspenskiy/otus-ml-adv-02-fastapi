from pydantic import BaseModel

class HartDiseaseModelResponse(BaseModel):
    prediction: int