from .base import BaseService
from dals import CustomerDAL
from models import Customer
from schemas import CustomerCreate, CustomerUpdate


class CustomerService(BaseService[CustomerDAL, CustomerCreate, CustomerUpdate]):
    pass


customer_service = CustomerService(CustomerDAL, Customer)
