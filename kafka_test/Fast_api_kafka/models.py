from pydantic import BaseModel

class EmployeesInput(BaseModel):
    id: int
    title: str
    name: str
    experience: str
    
class EmployeesResponse(BaseModel):
    id: int
    title: str
    name: str
    experience: str
