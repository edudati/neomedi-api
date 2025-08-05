"""
Visit Entity - Atendimento ou Consulta
Representa o registro detalhado de cada sessão clínica ou terapêutica.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class Visit:
    """
    Entidade Visit - Atendimento ou Consulta
    
    Representa um atendimento específico realizado com o paciente.
    Contém todos os detalhes da sessão clínica ou terapêutica.
    """
    
    def __init__(
        self,
        record_id: UUID,
        professional_id: UUID,
        company_id: Optional[UUID] = None,
        main_complaint: Optional[str] = None,
        current_illness_history: Optional[str] = None,
        past_history: Optional[str] = None,
        physical_exam: Optional[str] = None,
        diagnostic_hypothesis: Optional[str] = None,
        procedures: Optional[str] = None,
        prescription: Optional[str] = None,
        visit_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = visit_id or uuid4()
        self._record_id = record_id
        self._professional_id = professional_id
        self._company_id = company_id
        self._main_complaint = main_complaint or ""
        self._current_illness_history = current_illness_history or ""
        self._past_history = past_history or ""
        self._physical_exam = physical_exam or ""
        self._diagnostic_hypothesis = diagnostic_hypothesis or ""
        self._procedures = procedures or ""
        self._prescription = prescription or ""
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
        
        # Validações
        self._validate()
    
    def _validate(self) -> None:
        """Valida regras de negócio da entidade"""
        if not self._record_id:
            raise ValueError("Record ID é obrigatório")
        if not self._professional_id:
            raise ValueError("Professional ID é obrigatório")
    
    # Properties (Getters)
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def record_id(self) -> UUID:
        return self._record_id
    
    @property
    def professional_id(self) -> UUID:
        return self._professional_id
    
    @property
    def company_id(self) -> Optional[UUID]:
        return self._company_id
    
    @property
    def main_complaint(self) -> str:
        return self._main_complaint
    
    @property
    def current_illness_history(self) -> str:
        return self._current_illness_history
    
    @property
    def past_history(self) -> str:
        return self._past_history
    
    @property
    def physical_exam(self) -> str:
        return self._physical_exam
    
    @property
    def diagnostic_hypothesis(self) -> str:
        return self._diagnostic_hypothesis
    
    @property
    def procedures(self) -> str:
        return self._procedures
    
    @property
    def prescription(self) -> str:
        return self._prescription
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    # Business Methods
    def update_main_complaint(self, main_complaint: str) -> None:
        """Atualiza queixa principal"""
        self._main_complaint = main_complaint
        self._mark_as_updated()
    
    def update_current_illness_history(self, history: str) -> None:
        """Atualiza história da moléstia atual (HMA)"""
        self._current_illness_history = history
        self._mark_as_updated()
    
    def update_past_history(self, past_history: str) -> None:
        """Atualiza histórico e antecedentes"""
        self._past_history = past_history
        self._mark_as_updated()
    
    def update_physical_exam(self, physical_exam: str) -> None:
        """Atualiza exame físico"""
        self._physical_exam = physical_exam
        self._mark_as_updated()
    
    def update_diagnostic_hypothesis(self, hypothesis: str) -> None:
        """Atualiza hipótese diagnóstica"""
        self._diagnostic_hypothesis = hypothesis
        self._mark_as_updated()
    
    def update_procedures(self, procedures: str) -> None:
        """Atualiza condutas ou evoluções aplicadas"""
        self._procedures = procedures
        self._mark_as_updated()
    
    def update_prescription(self, prescription: str) -> None:
        """Atualiza prescrição ou recomendações"""
        self._prescription = prescription
        self._mark_as_updated()
    
    def is_complete(self) -> bool:
        """Verifica se o atendimento está completo com informações mínimas"""
        return bool(
            self._main_complaint and 
            (self._current_illness_history or self._physical_exam or self._diagnostic_hypothesis)
        )
    
    def _mark_as_updated(self) -> None:
        """Marca o registro como atualizado"""
        self._updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade para dicionário"""
        return {
            "id": self._id,
            "record_id": self._record_id,
            "professional_id": self._professional_id,
            "company_id": self._company_id,
            "main_complaint": self._main_complaint,
            "current_illness_history": self._current_illness_history,
            "past_history": self._past_history,
            "physical_exam": self._physical_exam,
            "diagnostic_hypothesis": self._diagnostic_hypothesis,
            "procedures": self._procedures,
            "prescription": self._prescription,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    def __eq__(self, other) -> bool:
        """Compara entidades por ID"""
        if not isinstance(other, Visit):
            return False
        return self._id == other._id
    
    def __repr__(self) -> str:
        return f"Visit(id={self._id}, record_id={self._record_id})"