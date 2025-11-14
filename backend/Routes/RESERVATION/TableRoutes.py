from fastapi import APIRouter, status

from Models.RESERVATION.TableModel import Table
from Schemas.RESERVATION.TableSchemas import *
from Controllers.RESERVATION.TableControllers import TableControllers
from Utils.SlowApi.SlowApi import limiter


TableRouter = APIRouter()