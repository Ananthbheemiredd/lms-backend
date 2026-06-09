from sqlalchemy import (
    select,
    func
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_category_model import (
    BookCategory
)

from app.models.library_model import (
    Library
)

from app.services.notification_service import (
    NotificationService
)


class BookCategoryService:

    # =====================================
    # CREATE CATEGORY
    # =====================================

    @staticmethod
    async def create_category(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        # -----------------------------
        # Validate Library
        # -----------------------------

        library = await db.get(
            Library,
            payload.library_id
        )

        if not library:

            raise ValueError(
                "Selected library does not exist"
            )

        if library.school_id != payload.school_id:

            raise ValueError(
                "Library does not belong to selected school"
            )

        if library.branch_id != payload.branch_id:

            raise ValueError(
                "Library does not belong to selected branch"
            )

        # -----------------------------
        # Duplicate Validation
        # -----------------------------

        existing = await db.execute(
            select(BookCategory).where(
                BookCategory.library_id == payload.library_id,
                BookCategory.category_name == payload.category_name
            )
        )

        if existing.scalar_one_or_none():

            raise ValueError(
                "Category already exists in this library"
            )

        # -----------------------------
        # Generate Category Code
        # -----------------------------

        result = await db.execute(
            select(
                func.max(BookCategory.id)
            )
        )

        last_id = result.scalar()

        if last_id is None:
            next_id = 1
        else:
            next_id = last_id + 1

        category_code = (
            f"CAT-{next_id:05d}"
        )

        # -----------------------------
        # Create Category
        # -----------------------------

        category = BookCategory(
            school_id=payload.school_id,
            branch_id=payload.branch_id,
            library_id=payload.library_id,

            category_code=category_code,
            category_name=payload.category_name,

            description=payload.description,

            creator_role=payload.creator_role,

            created_by=created_by
        )

        db.add(category)

        await db.commit()

        await db.refresh(category)

        # -----------------------------
        # Notification
        # -----------------------------

        await NotificationService.create_notification(
            db=db,
            title="Category Created",
            message=f"{category.category_name} category created successfully",
            notification_type="CATEGORY_CREATED",
            recipient_role=payload.creator_role
        )

        return category

    # =====================================
    # GET ALL CATEGORIES
    # =====================================

    @staticmethod
    async def get_all_categories(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookCategory)
        )

        return result.scalars().all()

    # =====================================
    # GET CATEGORY BY ID
    # =====================================

    @staticmethod
    async def get_category_by_id(
        db: AsyncSession,
        category_id: int
    ):

        result = await db.execute(
            select(BookCategory).where(
                BookCategory.id == category_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # UPDATE CATEGORY
    # =====================================

    @staticmethod
    async def update_category(
        db: AsyncSession,
        category_id: int,
        payload,
        updated_by: int
    ):

        category = await (
            BookCategoryService
            .get_category_by_id(
                db,
                category_id
            )
        )

        if not category:
            return None

        if payload.category_name is not None:
            category.category_name = payload.category_name

        if payload.description is not None:
            category.description = payload.description

        if payload.is_active is not None:
            category.is_active = payload.is_active

        category.updated_by = updated_by

        await db.commit()

        await db.refresh(category)

        await NotificationService.create_notification(
            db=db,
            title="Category Updated",
            message=f"{category.category_name} category updated successfully",
            notification_type="CATEGORY_UPDATED",
            recipient_role=category.creator_role
        )

        return category

    # =====================================
    # DELETE CATEGORY
    # =====================================

    @staticmethod
    async def delete_category(
        db: AsyncSession,
        category_id: int
    ):

        category = await (
            BookCategoryService
            .get_category_by_id(
                db,
                category_id
            )
        )

        if not category:
            return False

        category_name = category.category_name
        role = category.creator_role

        await db.delete(category)

        await db.commit()

        await NotificationService.create_notification(
            db=db,
            title="Category Deleted",
            message=f"{category_name} category deleted successfully",
            notification_type="CATEGORY_DELETED",
            recipient_role=role
        )

        return True