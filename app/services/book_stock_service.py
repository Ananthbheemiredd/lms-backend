from sqlalchemy import (
    select,
    func
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.book_model import Book
from app.models.book_stock_model import (
    BookStock
)

from app.schemas.book_stock_schema import (
    BookStockCreate,
    BookStockUpdate
)


class BookStockService:

    # =====================================
    # CREATE STOCK
    # =====================================

    @staticmethod
    async def create_stock(
        db: AsyncSession,
        payload: BookStockCreate,
        created_by: int = 1
    ):

        book = await db.get(
            Book,
            payload.book_id
        )

        if not book:
            raise ValueError(
                "Book not found"
            )

        stock = BookStock(

            school_id=payload.school_id,

            branch_id=payload.branch_id,

            library_id=payload.library_id,

            product_id=payload.product_id,

            book_id=payload.book_id,

            supplier_name=payload.supplier_name,

            invoice_number=payload.invoice_number,

            purchase_date=payload.purchase_date,

            purchase_price=payload.purchase_price,

            received_quantity=
                payload.received_quantity,

            available_quantity=
                payload.received_quantity,

            remarks=payload.remarks,

            created_by=created_by
        )

        db.add(stock)

        await db.commit()

        await db.refresh(stock)

        return stock

    # =====================================
    # GET ALL STOCKS
    # =====================================

    @staticmethod
    async def get_all_stocks(
        db: AsyncSession
    ):

        result = await db.execute(

            select(BookStock)

            .where(
                BookStock.is_active == True
            )

            .order_by(
                BookStock.id.desc()
            )
        )

        return result.scalars().all()

    # =====================================
    # GET STOCK BY ID
    # =====================================

    @staticmethod
    async def get_stock_by_id(
        db: AsyncSession,
        stock_id: int
    ):

        result = await db.execute(

            select(BookStock)

            .where(
                BookStock.id == stock_id,
                BookStock.is_active == True
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # UPDATE STOCK
    # =====================================

    @staticmethod
    async def update_stock(
        db: AsyncSession,
        stock_id: int,
        payload: BookStockUpdate,
        updated_by: int = 1
    ):

        stock = await db.get(
            BookStock,
            stock_id
        )

        if not stock:

            raise ValueError(
                "Stock not found"
            )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        for field, value in (
            update_data.items()
        ):

            setattr(
                stock,
                field,
                value
            )

        # Recalculate available stock

        stock.available_quantity = (

            stock.received_quantity

            - stock.damaged_quantity

            - stock.lost_quantity
        )

        stock.updated_by = updated_by

        await db.commit()

        await db.refresh(stock)

        return stock

    # =====================================
    # DELETE STOCK
    # =====================================

    @staticmethod
    async def delete_stock(
        db: AsyncSession,
        stock_id: int
    ):

        stock = await db.get(
            BookStock,
            stock_id
        )

        if not stock:

            raise ValueError(
                "Stock not found"
            )

        stock.is_active = False

        await db.commit()

        return True

    # =====================================
    # STOCK SUMMARY
    # =====================================

    @staticmethod
    async def get_stock_summary(
        db: AsyncSession
    ):

        total_received = await db.scalar(

            select(
                func.sum(
                    BookStock.received_quantity
                )
            )
        )

        total_available = await db.scalar(

            select(
                func.sum(
                    BookStock.available_quantity
                )
            )
        )

        total_damaged = await db.scalar(

            select(
                func.sum(
                    BookStock.damaged_quantity
                )
            )
        )

        total_lost = await db.scalar(

            select(
                func.sum(
                    BookStock.lost_quantity
                )
            )
        )

        return {

            "total_received_quantity":
                total_received or 0,

            "total_available_quantity":
                total_available or 0,

            "total_damaged_quantity":
                total_damaged or 0,

            "total_lost_quantity":
                total_lost or 0
        }