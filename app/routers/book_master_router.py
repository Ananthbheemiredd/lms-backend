# from typing import List
#
# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     status
# )
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.database.session import get_db
#
# from app.schemas.book_master_schema import (
#     BookMasterCreate,
#     BookMasterUpdate,
#     BookMasterResponse
# )
#
# from app.services.book_master_service import (
#     BookMasterService
# )
#
# router = APIRouter(
#     prefix="/books",
#     tags=["Book Master"]
# )
#
#
# # =====================================
# # CREATE BOOK
# # =====================================
#
# @router.post(
#     "",
#     response_model=BookMasterResponse,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_book(
#     payload: BookMasterCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#
#     try:
#
#         return await (
#             BookMasterService
#             .create_book(
#                 db=db,
#                 payload=payload,
#                 created_by=1
#                 # created_by=current_user.id
#             )
#         )
#
#     except ValueError as e:
#
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
#
#     except Exception as e:
#
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to create book: {str(e)}"
#         )
#
#
# # =====================================
# # GET ALL BOOKS
# # =====================================
#
# @router.get(
#     "",
#     response_model=List[BookMasterResponse]
# )
# async def get_books(
#     db: AsyncSession = Depends(get_db)
# ):
#
#     try:
#
#         return await (
#             BookMasterService
#             .get_all_books(db)
#         )
#
#     except Exception as e:
#
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to fetch books: {str(e)}"
#         )
#
#
# # =====================================
# # GET BOOK BY ID
# # =====================================
#
# @router.get(
#     "/{book_id}",
#     response_model=BookMasterResponse
# )
# async def get_book_by_id(
#     book_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#
#     book = await (
#         BookMasterService
#         .get_book_by_id(
#             db,
#             book_id
#         )
#     )
#
#     if not book:
#
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found"
#         )
#
#     return book
#
#
# # =====================================
# # UPDATE BOOK
# # =====================================
#
# @router.put(
#     "/{book_id}",
#     response_model=BookMasterResponse
# )
# async def update_book(
#     book_id: int,
#     payload: BookMasterUpdate,
#     db: AsyncSession = Depends(get_db)
# ):
#
#     book = await (
#         BookMasterService
#         .update_book(
#             db=db,
#             book_id=book_id,
#             payload=payload,
#             updated_by=1
#             # updated_by=current_user.id
#         )
#     )
#
#     if not book:
#
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found"
#         )
#
#     return book
#
#
# # =====================================
# # DELETE BOOK
# # =====================================
#
# @router.delete(
#     "/{book_id}"
# )
# async def delete_book(
#     book_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#
#     deleted = await (
#         BookMasterService
#         .delete_book(
#             db,
#             book_id
#         )
#     )
#
#     if not deleted:
#
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found"
#         )
#
#     return {
#         "message":
#             "Book deleted successfully"
#     }