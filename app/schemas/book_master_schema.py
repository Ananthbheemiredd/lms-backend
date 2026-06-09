# from datetime import datetime
# from typing import (
#     Optional,
#     Literal
# )
#
# from pydantic import (
#     BaseModel,
#     Field
# )
#
#
# # =====================================
# # CREATE BOOK
# # =====================================
#
# class BookMasterCreate(BaseModel):
#
#     school_id: int
#     branch_id: int
#     library_id: int
#     category_id: int
#
#     title: str = Field(
#         min_length=2,
#         max_length=255
#     )
#
#     sub_title: Optional[str] = Field(
#         default=None,
#         max_length=255
#     )
#
#     author_name: str = Field(
#         min_length=2,
#         max_length=255
#     )
#
#     publisher_name: Optional[str] = Field(
#         default=None,
#         max_length=255
#     )
#
#     isbn_number: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     edition: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     language: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     subject_name: Optional[str] = Field(
#         default=None,
#         max_length=255
#     )
#
#     book_type: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     total_copies: int = Field(
#         default=0,
#         ge=0
#     )
#
#     available_copies: int = Field(
#         default=0,
#         ge=0
#     )
#
#     minimum_threshold: int = Field(
#         default=2,
#         ge=0
#     )
#
#     lost_copies: int = Field(
#         default=0,
#         ge=0
#     )
#
#     damaged_copies: int = Field(
#         default=0,
#         ge=0
#     )
#
#     reserved_copies: int = Field(
#         default=0,
#         ge=0
#     )
#     product_id:str
#     keywords: Optional[str] = None
#
#     description: Optional[str] = None
#
#     creator_role: Literal[
#         "ADMIN",
#         "LIBRARIAN"
#     ]
#
#
# # =====================================
# # UPDATE BOOK
# # =====================================
#
# class BookMasterUpdate(BaseModel):
#
#     title: Optional[str] = Field(
#         default=None,
#         min_length=2,
#         max_length=255
#     )
#
#     sub_title: Optional[str] = Field(
#         default=None,
#         max_length=255
#     )
#
#     author_name: Optional[str] = Field(
#         default=None,
#         min_length=2,
#         max_length=255
#     )
#
#     publisher_name: Optional[str] = Field(
#         default=None,
#         max_length=255
#     )
#
#     isbn_number: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     edition: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     language: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     subject_name: Optional[str] = Field(
#         default=None,
#         max_length=255
#     )
#
#     book_type: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#
#     total_copies: Optional[int] = Field(
#         default=None,
#         ge=0
#     )
#
#     available_copies: Optional[int] = Field(
#         default=None,
#         ge=0
#     )
#
#     minimum_threshold: Optional[int] = Field(
#         default=None,
#         ge=0
#     )
#
#     lost_copies: Optional[int] = Field(
#         default=None,
#         ge=0
#     )
#
#     damaged_copies: Optional[int] = Field(
#         default=None,
#         ge=0
#     )
#
#     reserved_copies: Optional[int] = Field(
#         default=None,
#         ge=0
#     )
#
#     keywords: Optional[str] = None
#
#     description: Optional[str] = None
#
#     is_active: Optional[bool] = None
#
#
# # =====================================
# # RESPONSE
# # =====================================
#
# class BookMasterResponse(BaseModel):
#
#     id: int
#
#     school_id: int
#     branch_id: int
#     library_id: int
#     category_id: int
#
#     book_code: str
#
#     title: str
#     sub_title: Optional[str]
#
#     author_name: str
#     publisher_name: Optional[str]
#
#     isbn_number: Optional[str]
#
#     edition: Optional[str]
#     language: Optional[str]
#
#     subject_name: Optional[str]
#     book_type: Optional[str]
#
#     total_copies: int
#     available_copies: int
#
#     minimum_threshold: int
#
#     low_stock_alert: bool
#
#     lost_copies: int
#     damaged_copies: int
#     reserved_copies: int
#
#     keywords: Optional[str]
#
#     description: Optional[str]
#
#     creator_role: str
#
#     is_active: bool
#
#
#     created_at: datetime
#     updated_at: datetime
#
#     class Config:
#         from_attributes = True