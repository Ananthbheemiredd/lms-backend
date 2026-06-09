from sqlalchemy import (
    select,
    or_
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.book_model import (
    Book
)


class BookSearchService:

    # =====================================
    # SEARCH BOOKS
    # =====================================

    @staticmethod
    async def search_books(
        db: AsyncSession,
        keyword: str,
        school_id: int,
        branch_id: int,
        limit: int = 20,
        offset: int = 0
    ):

        result = await db.execute(

            select(Book)

            .where(

                # -------------------------
                # SCHOOL FILTER
                # -------------------------

                Book.school_id
                == school_id,

                # -------------------------
                # BRANCH FILTER
                # -------------------------

                Book.branch_id
                == branch_id,

                # -------------------------
                # ACTIVE BOOKS ONLY
                # -------------------------

                Book.is_active
                == True,

                # -------------------------
                # SEARCH CONDITIONS
                # -------------------------

                or_(

                    Book.title.ilike(
                        f"%{keyword}%"
                    ),

                    Book.author_name.ilike(
                        f"%{keyword}%"
                    ),

                    Book.isbn_number.ilike(
                        f"%{keyword}%"
                    ),

                    Book.subject_name.ilike(
                        f"%{keyword}%"
                    ),

                    Book.publisher_name.ilike(
                        f"%{keyword}%"
                    ),

                    Book.book_code.ilike(
                        f"%{keyword}%"
                    )
                )
            )

            # -----------------------------
            # SORTING
            # -----------------------------

            .order_by(
                Book.title.asc()
            )

            # -----------------------------
            # PAGINATION
            # -----------------------------

            .offset(offset)

            .limit(limit)
        )

        return result.scalars().all()