from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import (
    Base,
    engine
)

# ==========================
# Import Models
# ==========================

from app.models.library_model import Library
from app.models.library_floor_model import LibraryFloor
from app.models.library_rack_model import LibraryRack
from app.models.library_shelf_model import LibraryShelf
from app.models.library_row_model import LibraryRow
from app.models.notification_model import Notification
from app.models.book_category_model import (
    BookCategory
)
from app.models.stock_transaction_model import StockTransaction
from app.models.book_stock_model import BookStock
from app.models.book_copy_model import (
    BookCopy
)
from app.models.student_model import Student

from app.models.profile_information_model import (
    ProfileInformation
)
# ==========================
# Import Routers
# ==========================

from app.routers.library_router import (
    router as library_router
)

from app.routers.library_floor_router import (
    router as floor_router
)
from app.models.stock_transaction_model import (
    StockTransaction
)
from app.routers.stock_transaction_router import (
    router as stock_transaction_router
)

from app.routers.library_rack_router import (
    router as rack_router
)

from app.routers.library_shelf_router import (
    router as shelf_router
)

from app.routers.library_row_router import (
    router as row_router
)

from app.routers.notification_router import (
    router as notification_router
)

from app.routers.notification_ws_router import (
    router as notification_ws_router
)
from app.routers.book_category_router import (
    router as book_category_router
)

from app.routers.book_copy_router import (
    router as book_copy_router
)

from app.routers.library_borrow_rule_router import (
    router as library_borrow_rule_router
)
from app.routers.student_search_router import (
    router as student_search_router
)
from app.routers.employee_search_router import (
    router as employee_search_router
)
from app.routers.book_issue_router import (
    router as book_issue_router
)
from app.routers.book_search_router import (
    router as book_search_router
)
from fastapi.staticfiles import (
    StaticFiles
)
from app.routers.student_router import (
    router as student_router
)
from app.routers.employee_router import (
router as employee_router
)
from app.routers.report_router import (
    router as report_router
)
from app.routers.book_stock_request_router import (
    router as book_stock_request_router
)
from app.routers.school_router import (
    router as school_router
)
from app.routers.branch_router import (
    router as branch_router
)
from app.routers.book_stock_router import (
    router as book_stock_router
)
from app.services.email_service import EmailService
from app.routers.book_router import router as book_router
# ==========================
# FastAPI App
# ==========================

app = FastAPI(
    title="Library Management System",
    version="1.0.0"
)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================
# Startup Event
# ==========================

@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print("🚀 LMS Started Successfully")

# ==========================
# Shutdown Event
# ==========================

@app.on_event("shutdown")
async def shutdown():

    print("🛑 LMS Stopped")

# ==========================
# Register Routers
# ==========================

app.include_router(
    school_router,
    prefix="/api/v1"
)
app.include_router(
    branch_router,
    prefix="/api/v1"
)
app.include_router(
    library_router,
    prefix="/api/v1"
)

app.include_router(
    floor_router,
    prefix="/api/v1"
)

app.include_router(
    rack_router,
    prefix="/api/v1"
)

app.include_router(
    shelf_router,
    prefix="/api/v1"
)

app.include_router(
    row_router,
    prefix="/api/v1"
)
app.include_router(
    book_category_router,
    prefix="/api/v1"
)

app.include_router(
    book_router,
    prefix="/api/v1")
app.include_router(
    book_copy_router,
    prefix="/api/v1"
)
app.include_router(
    library_borrow_rule_router,
    prefix="/api/v1"
)
app.include_router(
    student_search_router,
    prefix="/api/v1"
)
app.include_router(
    employee_search_router,
    prefix="/api/v1"
)
app.include_router(
    book_search_router,
    prefix="/api/v1"
)
app.include_router(
    book_issue_router,
    prefix="/api/v1"
)



app.include_router(
    student_router,
    prefix="/api/v1"
)
app.include_router(
    employee_router,
    prefix="/api/v1"
)
app.include_router(
    report_router,
    prefix="/api/v1"
)
app.include_router(
    book_stock_request_router,
    prefix="/api/v1"
)
app.include_router(
    book_stock_router,
    prefix="/api/v1"
)
app.include_router(
    stock_transaction_router,
    prefix="/api/v1"
)
app.include_router(
    notification_router,
    prefix="/api/v1"
)

app.include_router(
    notification_ws_router
)


# ==========================
# Root Endpoint
# ==========================

@app.get("/")
async def root():

    return {
        "status": "success",
        "message": "Library Management System Running"
    }
