# Records Domain Use Cases
from .record_use_cases import (
    CreateRecordUseCase,
    GetRecordUseCase,
    UpdateRecordUseCase
)
from .visit_use_cases import (
    CreateVisitUseCase,
    GetVisitUseCase,
    UpdateVisitUseCase,
    GetVisitsByRecordUseCase
)
from .follow_up_use_cases import (
    CreateFollowUpUseCase,
    GetFollowUpsByRecordUseCase,
    UpdateFollowUpUseCase
)
from .exam_use_cases import (
    CreateExamUseCase,
    GetExamsByRecordUseCase,
    UpdateExamResultsUseCase
)
from .decision_support_use_cases import (
    CreateDecisionSupportUseCase,
    GetDecisionSupportByVisitUseCase,
    UpdateDecisionSupportUseCase
)

__all__ = [
    # Record Use Cases
    "CreateRecordUseCase",
    "GetRecordUseCase", 
    "UpdateRecordUseCase",
    # Visit Use Cases
    "CreateVisitUseCase",
    "GetVisitUseCase",
    "UpdateVisitUseCase",
    "GetVisitsByRecordUseCase",
    # FollowUp Use Cases
    "CreateFollowUpUseCase",
    "GetFollowUpsByRecordUseCase",
    "UpdateFollowUpUseCase",
    # Exam Use Cases
    "CreateExamUseCase",
    "GetExamsByRecordUseCase",
    "UpdateExamResultsUseCase",
    # DecisionSupport Use Cases
    "CreateDecisionSupportUseCase",
    "GetDecisionSupportByVisitUseCase",
    "UpdateDecisionSupportUseCase"
]