from typing import Optional

from pydantic import BaseModel


class BarcodeLocationResponse(BaseModel):

    floor_id: Optional[int] = None
    rack_id: Optional[int] = None
    shelf_id: Optional[int] = None
    row_id: Optional[int] = None


class BarcodeBookResponse(BaseModel):

    book_id: int

    product_id: str

    book_code: str

    isbn_number: str

    title: str

    author_name: str

    publisher_name: Optional[str] = None

    edition: Optional[str] = None

    language: Optional[str] = None

    subject_name: Optional[str] = None

    cover_image_url: Optional[str] = None


class BookBarcodeResponse(BaseModel):

    copy_id: int

    barcode: str

    accession_number: str

    copy_number: int

    book_status: str

    is_reference_only: bool

    acquisition_type: Optional[str] = None

    source_name: Optional[str] = None

    book: BarcodeBookResponse

    location: BarcodeLocationResponse

    class Config:
        from_attributes = True