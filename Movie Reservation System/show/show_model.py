from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import sys
sys.path.append("..")
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Show(Base):
    __tablename__ = "shows"

    show_id = Column(Integer, primary_key=True, index=False)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), nullable=False)
    show_time = Column(DateTime, nullable=False)
    total_seats = Column(Integer, default=100)

    seats = relationship("Seat", back_populates="show")
    tickets = relationship("Ticket", back_populates="show")


class Seat(Base):
    __tablename__ = "seats"

    seat_id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.show_id"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    is_booked = Column(Boolean, default=False)
    price = Column(Integer, nullable=False)

    show = relationship("Show", back_populates="seats")
    tickets = relationship("Ticket", back_populates="seat")
