from fastapi import APIRouter, HTTPException, status, Request
from Controllers.RESERVATION.ReservationControllers import ReservationControllers
from Schemas.RESERVATION.ReservationSchemas import ReservationCreate, ReservationUpdate
from datetime import datetime

from Utils.SlowApi.SlowApi import limiter

ReservationRouter = APIRouter(prefix="/reservations", tags=["Reservations"])