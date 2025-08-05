# Records Domain Routes - FastAPI Controllers
from .record_routes import router as record_router
from .visit_routes import router as visit_router  
from .follow_up_routes import router as follow_up_router
from .exam_routes import router as exam_router
from .decision_support_routes import router as decision_support_router

__all__ = [
    "record_router",
    "visit_router",
    "follow_up_router", 
    "exam_router",
    "decision_support_router"
]