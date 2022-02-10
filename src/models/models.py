from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Float,
    Integer,
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
    full_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(14), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)

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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=True) # noqa E501

    user = relationship("User", back_populates="address")
    customer = relationship("Customer", back_populates="address")


class Manufacturer(BaseModel):
    __tablename__ = "manufacturers"  # shared

    name = Column(String(255), nullable=False)

    medicine = relationship("Medicine", back_populates="manufacturer")
    trade = relationship("Trade", uselist=False, back_populates="manufacturer")
    trade_histories = relationship("TradeHistory", back_populates="manufacturer")


class Trade(BaseModel):
    __tablename__ = "trades"

    closing_balance = Column(Float, nullable=True, default=0)
    outstanding_amount = Column(Float, nullable=True, default=0)
    overdue_amount = Column(Float, nullable=True, default=0)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="CASCADE")) # noqa E501

    manufacturer = relationship("Manufacturer", back_populates="trade")


class TradeHistory(BaseModel):
    __tablename__ = "trade_histories"

    purchased_amount = Column(Float, nullable=True, default=0)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="CASCADE")) # noqa E501

    manufacturer = relationship("Manufacturer", back_populates="trade_histories")


class Medicine(BaseModel):
    __tablename__ = "medicines"  # shared

    brand_name = Column(String(255), nullable=False, index=True)
    generic_name = Column(String(255), nullable=True, index=True)
    dosage_form = Column(String(255), nullable=True)
    strength = Column(String(255), nullable=True)
    unit_price = Column(Float, nullable=True)
    depo_price = Column(Float, nullable=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="CASCADE")) # noqa E501

    manufacturer = relationship("Manufacturer", uselist=False, back_populates="medicine") # noqa E501
    stock = relationship("Stock", back_populates="medicine")
    invoice_lines = relationship("InvoiceOrderLine", back_populates="medicine")
    purchase_lines = relationship("PurchaseOrderLine", back_populates="medicine")
    grns = relationship("GRN", back_populates="medicine")


class Stock(BaseModel):
    __tablename__ = "stocks"

    in_stock = Column(Integer, nullable=True, default=0)
    critical_stock = Column(Integer, nullable=True, default=0)
    last_date_of_purchase = Column(DateTime, nullable=True)
    last_purchased_quantity = Column(Integer, nullable=True, default=0)
    gross_margin = Column(Float, nullable=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"))

    medicine = relationship("Medicine", back_populates="stock")


class InvoiceOrder(BaseModel):
    __tablename__ = "invoice_orders"

    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    due_amount = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    discount = Column(Integer, nullable=True, default=0)
    vat = Column(Integer, nullable=True, default=0)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True) # noqa E501
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    invoice_lines = relationship("InvoiceOrderLine", back_populates="invoice")
    user = relationship("User", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")


class InvoiceOrderLine(BaseModel):
    __tablename__ = "invoice_order_lines"

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Integer, nullable=True, default=0)
    cost = Column(Float, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoice_orders.id", ondelete="CASCADE"))
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="SET NULL"))

    invoice = relationship("InvoiceOrder", back_populates="invoice_lines")
    medicine = relationship("Medicine", back_populates="invoice_lines")


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    due_amount = Column(Float, nullable=False)
    note = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    purchase_lines = relationship("PurchaseOrderLine", back_populates="purchase")
    user = relationship("User", back_populates="purchases")
    grns = relationship("GRN", back_populates="purchase_order")


class PurchaseOrderLine(BaseModel):
    __tablename__ = "purchase_order_lines"

    quantity = Column(Integer, nullable=False)
    purchase_id = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"))
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="SET NULL"))

    purchase = relationship("PurchaseOrder", back_populates="purchase_lines")
    medicine = relationship("Medicine", back_populates="purchase_lines")


class GRN(BaseModel):
    __tablename__ = "grns"

    quantity = Column(Integer, nullable=False)
    depo_price = Column(Float, nullable=False)
    vat = Column(Integer, nullable=True, default=0)
    discount = Column(Integer, nullable=True, default=0)
    cost = Column(Float, nullable=False)
    expiry_date = Column(Date, nullable=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="SET NULL"))
    purchase_id = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE")) # noqa E501

    purchase_order = relationship("PurchaseOrder", back_populates="grns")
    medicine = relationship("Medicine", back_populates="grns")
