from pydantic import BaseModel


class TripRequest(BaseModel):
    user_id: str
    start_x: int
    start_y: int
    end_x: int
    end_y: int
