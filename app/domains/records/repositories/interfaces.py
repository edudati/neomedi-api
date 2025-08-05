"""
Repository Interfaces - Contratos para persistência de dados
Define as abstrações que os use cases utilizam para acessar dados.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.record import Record
from ..entities.visit import Visit
from ..entities.follow_up import FollowUp
from ..entities.exam import Exam, ExamType
from ..entities.decision_support import DecisionSupport


class IRecordRepository(ABC):
    """Interface para repositório de Records"""
    
    @abstractmethod
    async def create(self, record: Record) -> Record:
        """Cria um novo record"""
        pass
    
    @abstractmethod
    async def get_by_id(self, record_id: UUID) -> Optional[Record]:
        """Busca record por ID"""
        pass
    
    @abstractmethod
    async def get_by_patient_id(self, patient_id: UUID) -> Optional[Record]:
        """Busca record por ID do paciente"""
        pass
    
    @abstractmethod
    async def update(self, record: Record) -> Record:
        """Atualiza um record existente"""
        pass
    
    @abstractmethod
    async def exists_for_patient(self, patient_id: UUID) -> bool:
        """Verifica se já existe record para o paciente"""
        pass


class IVisitRepository(ABC):
    """Interface para repositório de Visits"""
    
    @abstractmethod
    async def create(self, visit: Visit) -> Visit:
        """Cria uma nova visit"""
        pass
    
    @abstractmethod
    async def get_by_id(self, visit_id: UUID) -> Optional[Visit]:
        """Busca visit por ID"""
        pass
    
    @abstractmethod
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[Visit]:
        """Busca visits por record ID com paginação"""
        pass
    
    @abstractmethod
    async def update(self, visit: Visit) -> Visit:
        """Atualiza uma visit existente"""
        pass
    
    @abstractmethod
    async def get_latest_by_record_id(self, record_id: UUID) -> Optional[Visit]:
        """Busca a última visit de um record"""
        pass


class IFollowUpRepository(ABC):
    """Interface para repositório de FollowUps"""
    
    @abstractmethod
    async def create(self, follow_up: FollowUp) -> FollowUp:
        """Cria um novo follow-up"""
        pass
    
    @abstractmethod
    async def get_by_id(self, follow_up_id: UUID) -> Optional[FollowUp]:
        """Busca follow-up por ID"""
        pass
    
    @abstractmethod
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[FollowUp]:
        """Busca follow-ups por record ID com paginação"""
        pass
    
    @abstractmethod
    async def get_by_visit_id(self, visit_id: UUID) -> List[FollowUp]:
        """Busca follow-ups por visit ID"""
        pass
    
    @abstractmethod
    async def update(self, follow_up: FollowUp) -> FollowUp:
        """Atualiza um follow-up existente"""
        pass


class IExamRepository(ABC):
    """Interface para repositório de Exams"""
    
    @abstractmethod
    async def create(self, exam: Exam) -> Exam:
        """Cria um novo exam"""
        pass
    
    @abstractmethod
    async def get_by_id(self, exam_id: UUID) -> Optional[Exam]:
        """Busca exam por ID"""
        pass
    
    @abstractmethod
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[Exam]:
        """Busca exams por record ID com paginação"""
        pass
    
    @abstractmethod
    async def get_by_visit_id(self, visit_id: UUID) -> List[Exam]:
        """Busca exams por visit ID"""
        pass
    
    @abstractmethod
    async def get_by_type(self, record_id: UUID, exam_type: ExamType) -> List[Exam]:
        """Busca exams por tipo"""
        pass
    
    @abstractmethod
    async def update(self, exam: Exam) -> Exam:
        """Atualiza um exam existente"""
        pass


class IDecisionSupportRepository(ABC):
    """Interface para repositório de DecisionSupport"""
    
    @abstractmethod
    async def create(self, decision_support: DecisionSupport) -> DecisionSupport:
        """Cria um novo decision support"""
        pass
    
    @abstractmethod
    async def get_by_id(self, decision_support_id: UUID) -> Optional[DecisionSupport]:
        """Busca decision support por ID"""
        pass
    
    @abstractmethod
    async def get_by_visit_id(self, visit_id: UUID) -> Optional[DecisionSupport]:
        """Busca decision support por visit ID"""
        pass
    
    @abstractmethod
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[DecisionSupport]:
        """Busca decision supports por record ID com paginação"""
        pass
    
    @abstractmethod
    async def update(self, decision_support: DecisionSupport) -> DecisionSupport:
        """Atualiza um decision support existente"""
        pass