from datetime import datetime

from pydantic import BaseModel

# =====================================

# CREATE STOCK REQUEST

# =====================================

class BookStockRequestCreate(BaseModel):
 product_id: str

book_id: int

requested_quantity: int

requested_by: int

remarks: str | None = None


# =====================================

# APPROVE STOCK REQUEST

# =====================================

class BookStockRequestApprove(BaseModel):


 approved_quantity: int

 approved_by: int

 remarks: str | None = None


# =====================================

# REJECT STOCK REQUEST

# =====================================

class BookStockRequestReject(BaseModel):
    approved_by: int

    rejection_reason: str


class BookStockRequestComplete(BaseModel):


 approved_by: int

 remarks: str | None = None


# =====================================

# RESPONSE SCHEMA

# =====================================

class BookStockRequestResponse(BaseModel):
    id: int

    product_id: str

    book_id: int

    requested_quantity: int

    approved_quantity: int | None

    request_status: str

    requested_by: int

    approved_by: int | None

    remarks: str | None

    rejection_reason: str | None

    created_at: datetime

    updated_at: datetime

class Config:

    from_attributes = True

