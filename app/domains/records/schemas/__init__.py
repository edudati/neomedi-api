# Records Domain Schemas - Pydantic DTOs for API validation
from .record_schemas import (
    RecordCreateRequest,
    RecordUpdateRequest,
    RecordResponse
)
from .visit_schemas import (
    VisitCreateRequest,
    VisitUpdateRequest,
    VisitResponse
)
from .follow_up_schemas import (
    FollowUpCreateRequest,
    FollowUpUpdateRequest,
    FollowUpResponse
)
from .exam_schemas import (
    ExamCreateRequest,
    ExamUpdateRequest,
    ExamResponse,
    ExamTypeResponse
)
from .decision_support_schemas import (
    DecisionSupportCreateRequest,
    DecisionSupportUpdateRequest,
    DecisionSupportResponse
)

__all__ = [
    # Record Schemas
    "RecordCreateRequest",
    "RecordUpdateRequest", 
    "RecordResponse",
    # Visit Schemas
    "VisitCreateRequest",
    "VisitUpdateRequest",
    "VisitResponse",
    # FollowUp Schemas
    "FollowUpCreateRequest",
    "FollowUpUpdateRequest",
    "FollowUpResponse",
    # Exam Schemas
    "ExamCreateRequest",
    "ExamUpdateRequest",
    "ExamResponse",
    "ExamTypeResponse",
    # DecisionSupport Schemas
    "DecisionSupportCreateRequest",
    "DecisionSupportUpdateRequest",
    "DecisionSupportResponse"
]