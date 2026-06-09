from datetime import (
    datetime,
    date
)

from typing import (
    Optional,
    Literal
)

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# CREATE BOOK COPY
# =====================================

class BookCopyCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int

    book_id: int

    floor_id: Optional[int] = None
    rack_id: Optional[int] = None
    shelf_id: Optional[int] = None
    row_id: Optional[int] = None

    acquisition_type: str = Field(
        default="PURCHASE",
        max_length=100
    )

    acquisition_price: Optional[float] = Field(
        default=None,
        ge=0
    )

    acquisition_date: Optional[date] = None

    source_name: Optional[str] = Field(
        default=None,
        max_length=255
    )

    is_reference_only: bool = False

    remarks: Optional[str] = None

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]


# =====================================
# UPDATE BOOK COPY
# =====================================

class BookCopyUpdate(BaseModel):

    floor_id: Optional[int] = None
    rack_id: Optional[int] = None
    shelf_id: Optional[int] = None
    row_id: Optional[int] = None

    book_status: Optional[str] = Field(
        default=None,
        max_length=50
    )

    acquisition_type: Optional[str] = Field(
        default=None,
        max_length=100
    )

    acquisition_price: Optional[float] = Field(
        default=None,
        ge=0
    )

    acquisition_date: Optional[date] = None

    source_name: Optional[str] = Field(
        default=None,
        max_length=255
    )

    is_reference_only: Optional[bool] = None

    remarks: Optional[str] = None

    is_active: Optional[bool] = None

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]
# =====================================
# ASSIGN LOCATION
# =====================================

class AssignBookCopyLocation(BaseModel):

    book_copy_ids: list[int]

    floor_id: int
    rack_id: int
    shelf_id: int
    row_id: int


# =====================================
# RESPONSE
# =====================================

class BookCopyResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    book_id: int

    floor_id: Optional[int]
    rack_id: Optional[int]
    shelf_id: Optional[int]
    row_id: Optional[int]

    barcode: str
    accession_number: str

    copy_number: int

    book_status: str

    acquisition_type: Optional[str]
    acquisition_price: Optional[float]
    acquisition_date: Optional[date]

    source_name: Optional[str]

    is_reference_only: bool

    remarks: Optional[str]

    is_active: bool

    created_by: Optional[int]
    updated_by: Optional[int]

    created_at: datetime
    updated_at: datetime
    # created_role: Literal[
    #     "ADMIN",
    #     "LIBRARIAN"
    # ]
    barcode_image_url: Optional[str]

    qr_code_url: Optional[str]

    class BarcodeBookDetailsResponse(BaseModel):
        barcode: str
        accession_number: str

        book_id: int
        copy_id: int

        title: str
        author_name: str
        isbn_number: str

        publisher_name: Optional[str]
        subject_name: Optional[str]
        language: Optional[str]

        copy_number: int
        book_status: str

        floor_name: Optional[str]
        rack_name: Optional[str]
        shelf_name: Optional[str]
        row_name: Optional[str]

        barcode_image_url: Optional[str]

        class Config:
            from_attributes = True

