# Records Domain Repository Interfaces and Implementations
from .interfaces import (
    IRecordRepository,
    IVisitRepository,
    IFollowUpRepository,
    IExamRepository,
    IDecisionSupportRepository
)
from .implementations import (
    RecordRepository,
    VisitRepository,
    FollowUpRepository,
    ExamRepository,
    DecisionSupportRepository
)

__all__ = [
    # Interfaces
    "IRecordRepository",
    "IVisitRepository", 
    "IFollowUpRepository",
    "IExamRepository",
    "IDecisionSupportRepository",
    # Implementations
    "RecordRepository",
    "VisitRepository",
    "FollowUpRepository",
    "ExamRepository",
    "DecisionSupportRepository"
]