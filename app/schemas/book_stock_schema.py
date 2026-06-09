from datetime import (
    datetime,
    date
)

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# CREATE STOCK
# =====================================

class BookStockCreate(BaseModel):

    school_id: int

    branch_id: int

    library_id: int

    product_id: str

    book_id: int

    supplier_name: str | None = None

    invoice_number: str | None = None

    purchase_date: date | None = None

    purchase_price: float | None = Field(
        default=None,
        ge=0
    )

    received_quantity: int = Field(
        gt=0
    )

    remarks: str | None = None


# =====================================
# UPDATE STOCK
# =====================================

class BookStockUpdate(BaseModel):

    supplier_name: str | None = None

    invoice_number: str | None = None

    purchase_date: date | None = None

    purchase_price: float | None = Field(
        default=None,
        ge=0
    )

    damaged_quantity: int | None = Field(
        default=None,
        ge=0
    )

    lost_quantity: int | None = Field(
        default=None,
        ge=0
    )

    remarks: str | None = None

    is_active: bool | None = None


# =====================================
# STOCK SUMMARY RESPONSE
# =====================================

class BookStockSummaryResponse(BaseModel):

    total_received_quantity: int

    total_available_quantity: int

    total_damaged_quantity: int

    total_lost_quantity: int


# =====================================
# RESPONSE
# =====================================

class BookStockResponse(BaseModel):

    id: int

    school_id: int

    branch_id: int

    library_id: int

    product_id: str

    book_id: int

    supplier_name: str | None

    invoice_number: str | None

    purchase_date: date | None

    purchase_price: float | None

    received_quantity: int

    available_quantity: int

    damaged_quantity: int

    lost_quantity: int

    remarks: str | None

    is_active: bool

    created_by: int | None

    updated_by: int | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True