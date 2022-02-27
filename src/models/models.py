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
from utils.enums import GenderEnum, BloodGroupEnum

# fmt: off


class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(50), nullable=False, unique=True)

    users = relationship("User", back_populates="role")


class User(BaseModel):
    __tablename__ = "users"

    full_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(14), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    pharmacy = relationship("Pharmacy", uselist=False, back_populates="user")
    invoices = relationship("InvoiceOrder", back_populates="user")
    purchases = relationship("PurchaseOrder", back_populates="user")


class Pharmacy(BaseModel):
    __tablename__ = "pharmacies"

    name = Column(String(100), nullable=False)
    trade_license = Column(String(50), nullable=False, unique=True)
    area = Column(String(100), nullable=False)
    sub_district = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="pharmacy")
    invoice_orders = relationship("InvoiceOrder", back_populates="pharmacy")
    purchase_orders = relationship("PurchaseOrder", back_populates="pharmacy")
    grns = relationship("GRN", back_populates="pharmacy")
    stocks = relationship("Stock", back_populates="pharmacy")
    trades = relationship("Trade", back_populates="pharmacy")
    trade_histories = relationship("TradeHistory", back_populates="pharmacy")


class Customer(BaseModel):
    __tablename__ = "customers"

    full_name = Column(String(100), nullable=False)
    phone = Column(String(14), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=True, unique=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    bloodgroup = Column(Enum(BloodGroupEnum), nullable=True)
    birthdate = Column(Date, nullable=True)
    location = Column(String(225), nullable=True)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    invoices = relationship("InvoiceOrder", back_populates="customer")


class Manufacturer(BaseModel):
    __tablename__ = "manufacturers"  # shared

    name = Column(String(255), nullable=False)

    medicine = relationship("Medicine", back_populates="manufacturer")
    trade = relationship("Trade", uselist=False, back_populates="manufacturer")
    trade_histories = relationship("TradeHistory", back_populates="manufacturer")
    purchase_orders = relationship("PurchaseOrder", back_populates="manufacturer")
    grns = relationship("GRN", back_populates="manufacturer")


class Trade(BaseModel):
    __tablename__ = "trades"

    closing_balance = Column(Float, nullable=True, default=0)
    outstanding_amount = Column(Float, nullable=True, default=0)
    overdue_amount = Column(Float, nullable=True, default=0)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="CASCADE"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    manufacturer = relationship("Manufacturer", back_populates="trade")
    pharmacy = relationship("Pharmacy", back_populates="trades")


class TradeHistory(BaseModel):
    __tablename__ = "trade_histories"

    purchased_amount = Column(Float, nullable=True, default=0)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="CASCADE"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    manufacturer = relationship("Manufacturer", back_populates="trade_histories")
    pharmacy = relationship("Pharmacy", back_populates="trade_histories")


class Medicine(BaseModel):
    __tablename__ = "medicines"  # shared

    brand_name = Column(String(255), nullable=False, index=True)
    generic_name = Column(String(255), nullable=True, index=True)
    dosage_form = Column(String(255), nullable=True)
    strength = Column(String(255), nullable=True)
    unit_price = Column(Float, nullable=True)
    depo_price = Column(Float, nullable=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="CASCADE"))

    manufacturer = relationship("Manufacturer", uselist=False, back_populates="medicine")
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
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    medicine = relationship("Medicine", back_populates="stock")
    pharmacy = relationship("Pharmacy", back_populates="stocks")


class InvoiceOrder(BaseModel):
    __tablename__ = "invoice_orders"

    sub_total = Column(Float, nullable=False)
    total_mrp = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    due_amount = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    discount = Column(Integer, nullable=True, default=0)
    vat = Column(Integer, nullable=True, default=0)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    invoice_lines = relationship("InvoiceOrderLine", back_populates="invoice")
    user = relationship("User", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")
    pharmacy = relationship("Pharmacy", back_populates="invoice_orders")


class InvoiceOrderLine(BaseModel):
    __tablename__ = "invoice_order_lines"

    quantity = Column(Integer, nullable=False)
    mrp = Column(Float, nullable=False)
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
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="SET NULL"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    purchase_lines = relationship("PurchaseOrderLine", back_populates="purchase")
    user = relationship("User", back_populates="purchases")
    grns = relationship("GRN", back_populates="purchase_order")
    manufacturer = relationship("Manufacturer", back_populates="purchase_orders")
    pharmacy = relationship("Pharmacy", back_populates="purchase_orders")


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
    purchase_id = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"))
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete="SET NULL"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"))

    purchase_order = relationship("PurchaseOrder", back_populates="grns")
    medicine = relationship("Medicine", back_populates="grns")
    manufacturer = relationship("Manufacturer", back_populates="grns")
    pharmacy = relationship("Pharmacy", back_populates="grns")
