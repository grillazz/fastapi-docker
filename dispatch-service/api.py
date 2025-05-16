from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .model import Taxi, Trip, TripStatus
from .schema import TripRequest
from .database import get_db

router = APIRouter()


@router.post("/trips", status_code=201)
async def create_trip(
        request: Request,
        trip_request: TripRequest,
        db: AsyncSession = Depends(get_db)
):
    closest_taxi = await Taxi.find_closest_and_lock_it(
        db,
        trip_request.start_x,
        trip_request.start_y
    )
    if not closest_taxi:
        raise HTTPException(status_code=404, detail="No available taxis found")

    new_trip = Trip(
        id=hash(trip_request.user_id+str(trip_request.start_x)+str(trip_request.start_y)+closest_taxi.taxi_id),
        user_id=trip_request.user_id,
        taxi_id=closest_taxi.taxi_id,
        start_x=trip_request.start_x,
        start_y=trip_request.start_y,
        end_x=trip_request.end_x,
        end_y=trip_request.end_y,
        status=TripStatus.ASSIGNED.value
    )

    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)

    try:
        container = request.app.docker_cli.containers.get(closest_taxi.taxi_id)
        container.restart()
        return {
            "trip_id": new_trip.id,
            "taxi_id": closest_taxi.taxi_id,
            "status": new_trip.status,
            "container_id": container.id,
        }

    except Exception as e:
        closest_taxi.status = "available"
        await db.delete(new_trip)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to start taxi: {str(e)}")