from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .model import Taxi, Trip, TripStatus, TaxiStatus
from .schema import TripRequest
from .database import get_db
from sqlalchemy.exc import NoResultFound

router = APIRouter()


@router.post("/trips", status_code=201)
async def create_trip(
    request: Request, trip_request: TripRequest, db: AsyncSession = Depends(get_db)
):
    closest_taxi = await Taxi.find_closest_and_lock_it(
        db, trip_request.start_x, trip_request.start_y
    )
    if not closest_taxi:
        raise HTTPException(status_code=404, detail="No available taxis found")

    new_trip = Trip(
        user_id=trip_request.user_id,
        taxi_id=closest_taxi.taxi_id,
        start_x=trip_request.start_x,
        start_y=trip_request.start_y,
        end_x=trip_request.end_x,
        end_y=trip_request.end_y,
        status=TripStatus.ASSIGNED.value,
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
        }

    except Exception as e:
        closest_taxi.status = "available"
        await db.delete(new_trip)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to start taxi: {str(e)}")


@router.get("/trips/{taxi_id}", status_code=200)
async def get_trip(taxi_id: str, db: AsyncSession = Depends(get_db)):
    trip: Trip = await Trip.get_trip_by_taxi_id(db, taxi_id)
    if trip:
        return {
            "trip_id": trip.id,
            "user_id": trip.user_id,
            "taxi_id": trip.taxi_id,
            "start_x": trip.start_x,
            "start_y": trip.start_y,
            "end_x": trip.end_x,
            "end_y": trip.end_y,
            "status": trip.status,
        }
    return None


@router.patch("/trips/{trip_id}", status_code=200)
async def update_trip_status(
    trip_id: int, status: TripStatus, db: AsyncSession = Depends(get_db)
):
    try:
        trip = await db.get_one(Trip, trip_id)
        trip.status = status.value
        await db.flush()
        await db.refresh(trip)
        if trip.status == TripStatus.COMPLETED.value:
            taxi = await db.get_one(Taxi, trip.taxi_id)
            taxi.status = TaxiStatus.AVAILABLE.value
            taxi.x = trip.end_x
            taxi.y = trip.end_y
            await db.commit()
        return {"trip_id": trip.id, "status": trip.status}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Trip not found")
