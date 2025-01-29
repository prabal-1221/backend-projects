from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import sys
sys.path.append('..')
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
import sys
sys.path.append('..')
from show.show_model import Seat
from show.show_model import Show
from movie.movie_model import Movie

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    tickets = relationship("Ticket", back_populates="user")

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    show_id = Column(Integer, ForeignKey("shows.show_id"))
    seat_id = Column(Integer, ForeignKey("seats.seat_id"))
    booked_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="tickets")
    show = relationship("Show", back_populates="tickets")
    seat = relationship("Seat", back_populates="tickets")
