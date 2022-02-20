from fastapi import APIRouter

from .endpoints import (
    customers,
    invoices,
    login,
    manufacturers,
    medicines,
    purchases,
    stocks,
    users,
    grns,
    roles,
)

api_router = APIRouter()

# fmt: off

api_router.include_router(login.router, tags=["login"])
api_router.include_router(manufacturers.router, prefix="/manufacturers", tags=["manufacturers"]) # noqa E501
api_router.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
api_router.include_router(grns.router, prefix="/grns", tags=["grns"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
