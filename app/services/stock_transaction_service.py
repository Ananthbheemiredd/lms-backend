from sqlalchemy import (
    select,
    func
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.stock_transaction_model import (
    StockTransaction
)

from app.schemas.stock_transaction_schema import (
    StockTransactionCreate
)


class StockTransactionService:

    # =====================================
    # CREATE TRANSACTION
    # =====================================

    @staticmethod
    async def create_transaction(
        db: AsyncSession,
        payload: StockTransactionCreate
    ):

        transaction = StockTransaction(

            product_id=payload.product_id,

            book_id=payload.book_id,

            transaction_type=
                payload.transaction_type,

            quantity=payload.quantity,

            reference_id=
                payload.reference_id,

            remarks=payload.remarks,

            created_by=
                payload.created_by
        )

        db.add(transaction)

        await db.commit()

        await db.refresh(transaction)

        return transaction

    # =====================================
    # GET ALL TRANSACTIONS
    # =====================================

    @staticmethod
    async def get_all_transactions(
        db: AsyncSession
    ):

        result = await db.execute(

            select(
                StockTransaction
            )

            .order_by(
                StockTransaction
                .created_at
                .desc()
            )
        )

        return (
            result
            .scalars()
            .all()
        )

    # =====================================
    # GET BY ID
    # =====================================

    @staticmethod
    async def get_transaction_by_id(
        db: AsyncSession,
        transaction_id: int
    ):

        result = await db.execute(

            select(
                StockTransaction
            )

            .where(
                StockTransaction.id
                == transaction_id
            )
        )

        return (
            result
            .scalar_one_or_none()
        )

    # =====================================
    # GET BY BOOK
    # =====================================

    @staticmethod
    async def get_transactions_by_book(
        db: AsyncSession,
        book_id: int
    ):

        result = await db.execute(

            select(
                StockTransaction
            )

            .where(
                StockTransaction.book_id
                == book_id
            )

            .order_by(
                StockTransaction
                .created_at
                .desc()
            )
        )

        return (
            result
            .scalars()
            .all()
        )

    # =====================================
    # GET BY PRODUCT
    # =====================================

    @staticmethod
    async def get_transactions_by_product(
        db: AsyncSession,
        product_id: str
    ):

        result = await db.execute(

            select(
                StockTransaction
            )

            .where(
                StockTransaction.product_id
                == product_id
            )

            .order_by(
                StockTransaction
                .created_at
                .desc()
            )
        )

        return (
            result
            .scalars()
            .all()
        )

    # =====================================
    # SUMMARY
    # =====================================

    @staticmethod
    async def get_summary(
        db: AsyncSession
    ):

        total_stock_in = await db.scalar(

            select(
                func.sum(
                    StockTransaction.quantity
                )
            )

            .where(
                StockTransaction
                .transaction_type
                == "STOCK_IN"
            )
        )

        total_issued = await db.scalar(

            select(
                func.sum(
                    StockTransaction.quantity
                )
            )

            .where(
                StockTransaction
                .transaction_type
                == "ISSUE"
            )
        )

        total_returned = await db.scalar(

            select(
                func.sum(
                    StockTransaction.quantity
                )
            )

            .where(
                StockTransaction
                .transaction_type
                == "RETURN"
            )
        )

        total_lost = await db.scalar(

            select(
                func.sum(
                    StockTransaction.quantity
                )
            )

            .where(
                StockTransaction
                .transaction_type
                == "LOST"
            )
        )

        total_damaged = await db.scalar(

            select(
                func.sum(
                    StockTransaction.quantity
                )
            )

            .where(
                StockTransaction
                .transaction_type
                == "DAMAGED"
            )
        )

        return {

            "total_stock_in":
                total_stock_in or 0,

            "total_issued":
                total_issued or 0,

            "total_returned":
                total_returned or 0,

            "total_lost":
                total_lost or 0,

            "total_damaged":
                total_damaged or 0
        }