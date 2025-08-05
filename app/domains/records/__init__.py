# Records Domain - Clean Architecture Implementation
# 
# Este domínio implementa o gerenciamento completo de prontuários médicos
# seguindo os princípios de Clean Code e Domain-Driven Design.

# Entities (Domain Layer)
from .entities import (
    Record,
    Visit,
    FollowUp,
    Exam,
    DecisionSupport
)

# Use Cases (Application Layer)
from .use_cases import (
    # Record Use Cases
    CreateRecordUseCase,
    GetRecordUseCase,
    UpdateRecordUseCase,
    # Visit Use Cases
    CreateVisitUseCase,
    GetVisitUseCase,
    UpdateVisitUseCase,
    GetVisitsByRecordUseCase,
    # FollowUp Use Cases
    CreateFollowUpUseCase,
    GetFollowUpsByRecordUseCase,
    UpdateFollowUpUseCase,
    # Exam Use Cases
    CreateExamUseCase,
    GetExamsByRecordUseCase,
    UpdateExamResultsUseCase,
    # DecisionSupport Use Cases
    CreateDecisionSupportUseCase,  
    GetDecisionSupportByVisitUseCase
)

# Repository Interfaces & Implementations (Infrastructure Layer) 
from .repositories import (
    # Interfaces
    IRecordRepository,
    IVisitRepository,
    IFollowUpRepository,
    IExamRepository,
    IDecisionSupportRepository,
    # Implementations
    RecordRepository,
    VisitRepository,
    FollowUpRepository,
    ExamRepository,
    DecisionSupportRepository
)

# SQLAlchemy Models (Infrastructure Layer)
from .models import (
    RecordModel,
    VisitModel,
    FollowUpModel,
    ExamModel,
    ExamTypeEnum,
    DecisionSupportModel
)

# Pydantic Schemas (Interface Layer - DTOs)
from .schemas import (
    # Record Schemas
    RecordCreateRequest,
    RecordUpdateRequest,
    RecordResponse,
    # Visit Schemas
    VisitCreateRequest,
    VisitUpdateRequest,
    VisitResponse,
    # FollowUp Schemas
    FollowUpCreateRequest,
    FollowUpUpdateRequest,
    FollowUpResponse,
    # Exam Schemas
    ExamCreateRequest,
    ExamUpdateRequest,
    ExamResponse,
    ExamTypeResponse,
    # DecisionSupport Schemas
    DecisionSupportCreateRequest,
    DecisionSupportUpdateRequest,
    DecisionSupportResponse
)

# FastAPI Routes (Interface Layer - Controllers)
from .routes import (
    record_router,
    visit_router,
    follow_up_router,
    exam_router,
    decision_support_router
)

__all__ = [
    # Entities
    "Record",
    "Visit", 
    "FollowUp",
    "Exam",
    "DecisionSupport",
    # Use Cases
    "CreateRecordUseCase",
    "GetRecordUseCase",
    "UpdateRecordUseCase",
    "CreateVisitUseCase",
    "GetVisitUseCase",
    "UpdateVisitUseCase",
    "GetVisitsByRecordUseCase",
    "CreateFollowUpUseCase",
    "GetFollowUpsByRecordUseCase",
    "UpdateFollowUpUseCase",
    "CreateExamUseCase",
    "GetExamsByRecordUseCase",
    "UpdateExamResultsUseCase",
    "CreateDecisionSupportUseCase",
    "GetDecisionSupportByVisitUseCase",
    # Repository Interfaces
    "IRecordRepository",
    "IVisitRepository",
    "IFollowUpRepository",
    "IExamRepository",
    "IDecisionSupportRepository",
    # Repository Implementations
    "RecordRepository",
    "VisitRepository",
    "FollowUpRepository",
    "ExamRepository",
    "DecisionSupportRepository",
    # SQLAlchemy Models
    "RecordModel",
    "VisitModel",
    "FollowUpModel",
    "ExamModel",
    "ExamTypeEnum",
    "DecisionSupportModel",
    # Pydantic Schemas
    "RecordCreateRequest",
    "RecordUpdateRequest",
    "RecordResponse",
    "VisitCreateRequest",
    "VisitUpdateRequest",
    "VisitResponse",
    "FollowUpCreateRequest",
    "FollowUpUpdateRequest",
    "FollowUpResponse",
    "ExamCreateRequest",
    "ExamUpdateRequest",
    "ExamResponse",
    "ExamTypeResponse",
    "DecisionSupportCreateRequest",
    "DecisionSupportUpdateRequest",
    "DecisionSupportResponse",
    # FastAPI Routes
    "record_router",
    "visit_router",
    "follow_up_router",
    "exam_router",
    "decision_support_router"
]