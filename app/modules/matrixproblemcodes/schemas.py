from pydantic import BaseModel


class MatrixCreate(BaseModel):
    location_id: int
    problem_code_id: int


class MatrixRead(MatrixCreate):
    id: int

    class Config:
        from_attributes = True
