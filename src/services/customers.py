from .base import BaseService
from src.dals import CustomerDAL
from src.models import Customer
from src.schemas import CustomerCreate, CustomerUpdate


class CustomerService(BaseService[CustomerDAL, CustomerCreate, CustomerUpdate]):
    pass


customer_service = CustomerService(CustomerDAL, Customer)
