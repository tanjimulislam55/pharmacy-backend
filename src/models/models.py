from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import (
    Column,
    Float,
    Integer,
    PickleType,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Enum,
)

from .base import BaseModel
from src.utils.enums import GenderEnum, BloodGroupEnum

# fmt: off


class Role(BaseModel):
    __tablename__ = "roles"
    name = Column(String(50), nullable=False, unique=True)


class User(BaseModel):
    __tablename__ = "users"
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(14), nullable=False, unique=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    address = relationship("Address", uselist=False, back_populates="user")
    invoices = relationship("InvoiceOrder", back_populates="user")
    purchases = relationship("PurchaseOrder", back_populates="user")


class Customer(BaseModel):
    __tablename__ = "customers"

    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    phone = Column(String(14), nullable=False, unique=True, index=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    bloodgroup = Column(Enum(BloodGroupEnum), nullable=True)
    birthdate = Column(Date, nullable=True)

    address = relationship("Address", uselist=False, back_populates="customer")
    invoices = relationship("InvoiceOrder", back_populates="customer")


class Address(BaseModel):
    __tablename__ = "addresses"

    flat = Column(String(10), nullable=True)
    house = Column(String(10), nullable=True)
    road = Column(String(10), nullable=True)
    block = Column(String(10), nullable=True)
    area = Column(String(30), nullable=True)
    city = Column(String(20), nullable=True)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(30), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    user = relationship("User", back_populates="address")
    customer = relationship("Customer", back_populates="address")


class Manufacturer(BaseModel):
    __tablename__ = "manufacturers"

    name = Column(String(255), nullable=False)
    total_brands = Column(Integer, nullable=True)
    total_generics = Column(Integer, nullable=True)
    headquarter = Column(String(500), nullable=True)
    contact_list = Column(MutableList.as_mutable(PickleType), nullable=True, default=[])
    established_in = Column(String(10), nullable=True)
    market_share = Column(String(10), nullable=True)
    growth = Column(String(10), nullable=True)

    medicine = relationship("Medicine", back_populates="manufacturer")


class Medicine(BaseModel):
    __tablename__ = "medicines"

    brand_name = Column(String(255), nullable=False, index=True)
    generic_name = Column(String(255), nullable=True, index=True)
    dosage_form = Column(String(255), nullable=True)
    strength = Column(String(255), nullable=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))

    manufacturer = relationship("Manufacturer", uselist=False, back_populates="medicine") # noqa E501
    stock = relationship("Stock", back_populates="medicine")
    invoice_lines = relationship("InvoiceOrderLine", back_populates="medicine")
    purchase_lines = relationship("PurchaseOrderLine", back_populates="medicine")


class Stock(BaseModel):
    __tablename__ = "stocks"

    in_stock = Column(Integer, nullable=True, default=0)
    last_transacted_date = Column(DateTime, nullable=True)
    last_transacted_quantity = Column(Integer, nullable=True, default=0)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))

    medicine = relationship("Medicine", back_populates="stock")


class InvoiceOrder(BaseModel):
    __tablename__ = "invoice_orders"

    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    due_amount = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    discount = Column(Integer, nullable=True, default=0)
    vat = Column(Integer, nullable=True, default=0)
    profit_on_transaction = Column(Float, default=0)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")


class InvoiceOrderLine(BaseModel):
    __tablename__ = "invoice_order_lines"

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoice_orders.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))

    medicine = relationship("Medicine", back_populates="invoice_lines")


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    due_amount = Column(Float, nullable=False)
    note = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="purchases")


class PurchaseOrderLine(BaseModel):
    __tablename__ = "purchase_order_lines"

    quantity = Column(Integer, nullable=False)
    buying_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    expiry_date = Column(Date, nullable=True)
    purchase_id = Column(Integer, ForeignKey("purchase_orders.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))

    medicine = relationship("Medicine", back_populates="purchase_lines")
