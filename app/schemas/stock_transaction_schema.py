from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# CREATE TRANSACTION
# =====================================

class StockTransactionCreate(BaseModel):

    product_id: str

    book_id: int

    transaction_type: str

    quantity: int = Field(
        gt=0
    )

    reference_id: int | None = None

    remarks: str | None = None

    created_by: int | None = None


# =====================================
# RESPONSE
# =====================================

class StockTransactionResponse(BaseModel):

    id: int

    product_id: str

    book_id: int

    transaction_type: str

    quantity: int

    reference_id: int | None

    remarks: str | None

    created_by: int | None

    created_at: datetime

    class Config:

        from_attributes = True


# =====================================
# SUMMARY RESPONSE
# =====================================

class StockTransactionSummaryResponse(
    BaseModel
):

    total_stock_in: int

    total_issued: int

    total_returned: int

    total_lost: int

    total_damaged: int