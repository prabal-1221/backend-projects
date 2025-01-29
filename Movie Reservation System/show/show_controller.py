from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional
import sys
sys.path.append("..")
from database import init_db
from sqlalchemy.orm import Session
from .show_model import Show, Seat
from .show_vo import ShowRequest, SeatRequest
sys.path.append("..")
from movie.movie_model import Movie
sys.path.append("..")
from user.user_model import Ticket
sys.path.append("..")
from user.user_controller import get_current_user

show_route = APIRouter(prefix="/shows")

db_dependency = Annotated[Session, Depends(init_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@show_route.get("/")
def get_all_shows(db: db_dependency, movie_id: Optional[int] = None):
    query = db.query(Show)

    if movie_id:
        query = query.filter(Show.movie_id == movie_id)

    shows = query.all()

    if not shows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no show found.")
    
    return shows

@show_route.post("/{movie_id}")
def add_show(movie_id: int, show_data: ShowRequest, db: db_dependency):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    new_show = Show(
        movie_id = movie_id,
        show_time = show_data.show_time
    )

    db.add(new_show)
    db.flush()
    db.refresh(new_show)

    seat_objects = [Seat(show_id = new_show.show_id, seat_number = i) for i in range(1,101)]
    db.bulk_save_objects(seat_objects)

    db.commit()

    return new_show

@show_route.get("/{show_id}/seats")
def get_available_seats(show_id: int, db: db_dependency):
    show = db.query(Show).filter(Show.show_id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found.")
    
    available_seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.is_booked == False).all()

    if not available_seats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No seat available.")
    
    return [{"seat_number": seat.seat_number, "price": seat.price} for seat in available_seats]

@show_route.post("/{show_id}/seats")
def books_seats(show_id: int, seats: SeatRequest, db: db_dependency, user: user_dependency):
    show = db.query(Show).filter(Show.show_id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found.")

    seat_objects = db.query(Seat).filter(Seat.show_id == show_id, Seat.seat_number.in_(seats)).all()

    unavailable_seats = []
    for seat in seat_objects:
        if seat.is_booked:
            unavailable_seats.append(seat.seat_number)

    if unavailable_seats:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Seats {unavailable_seats} are not available.")
    
    tickets_to_add = []
    for seat in seat_objects:
        seat.is_booked = True
        ticket = Ticket(
            user_id=user["user_id"],
            show_id=show_id,
            seat_id=seat.seat_id
        )
        tickets_to_add.append(ticket)

    db.bulk_save_objects(tickets_to_add)

    db.commit()
    
    return {"detail": f"Seats {', '.join(map(str, seats))} booked successfully."}
    