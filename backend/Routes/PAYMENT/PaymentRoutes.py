from fastapi import APIRouter, Depends, HTTPException
from typing import Any

from Controllers.PAYMENT.PaymentControllers import create_payment
from Schemas.PAYMENT.PaymentSchemas import PaymentCreate, PaymentRead

PaymentRouter = APIRouter(prefix="/payments", tags=["payments"])