"""
Record Entity - Aggregate Root do domínio Records
Representa o prontuário único do paciente com dados permanentes e histórico clínico global.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4


class Record:
    """
    Entidade Record - Prontuário Único do Paciente
    
    Aggregate Root que mantém consistência dos dados clínicos do paciente.
    Contém dados permanentes e histórico clínico global.
    """
    
    def __init__(
        self,
        patient_id: UUID,
        professional_id: UUID,
        company_id: Optional[UUID] = None,
        clinical_history: Optional[str] = None,
        surgical_history: Optional[str] = None,
        family_history: Optional[str] = None,
        habits: Optional[str] = None,
        allergies: Optional[str] = None,
        current_medications: Optional[str] = None,
        last_diagnoses: Optional[str] = None,
        tags: Optional[List[str]] = None,
        record_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = record_id or uuid4()
        self._patient_id = patient_id
        self._professional_id = professional_id
        self._company_id = company_id
        self._clinical_history = clinical_history or ""
        self._surgical_history = surgical_history or ""
        self._family_history = family_history or ""
        self._habits = habits or ""
        self._allergies = allergies or ""
        self._current_medications = current_medications or ""
        self._last_diagnoses = last_diagnoses or ""
        self._tags = tags or []
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
        
        # Validações
        self._validate()
    
    def _validate(self) -> None:
        """Valida regras de negócio da entidade"""
        if not self._patient_id:
            raise ValueError("Patient ID é obrigatório")
        if not self._professional_id:
            raise ValueError("Professional ID é obrigatório")
    
    # Properties (Getters)
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def patient_id(self) -> UUID:
        return self._patient_id
    
    @property
    def professional_id(self) -> UUID:
        return self._professional_id
    
    @property
    def company_id(self) -> Optional[UUID]:
        return self._company_id
    
    @property
    def clinical_history(self) -> str:
        return self._clinical_history
    
    @property
    def surgical_history(self) -> str:
        return self._surgical_history
    
    @property
    def family_history(self) -> str:
        return self._family_history
    
    @property
    def habits(self) -> str:
        return self._habits
    
    @property
    def allergies(self) -> str:
        return self._allergies
    
    @property
    def current_medications(self) -> str:
        return self._current_medications
    
    @property
    def last_diagnoses(self) -> str:
        return self._last_diagnoses
    
    @property
    def tags(self) -> List[str]:
        return self._tags.copy()
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    # Business Methods
    def update_clinical_history(self, clinical_history: str) -> None:
        """Atualiza histórico clínico"""
        self._clinical_history = clinical_history
        self._mark_as_updated()
    
    def update_surgical_history(self, surgical_history: str) -> None:
        """Atualiza histórico cirúrgico"""
        self._surgical_history = surgical_history
        self._mark_as_updated()
    
    def update_family_history(self, family_history: str) -> None:
        """Atualiza histórico familiar"""
        self._family_history = family_history
        self._mark_as_updated()
    
    def update_habits(self, habits: str) -> None:
        """Atualiza hábitos do paciente"""
        self._habits = habits
        self._mark_as_updated()
    
    def update_allergies(self, allergies: str) -> None:
        """Atualiza alergias do paciente"""
        self._allergies = allergies
        self._mark_as_updated()
    
    def update_current_medications(self, medications: str) -> None:
        """Atualiza medicamentos em uso"""
        self._current_medications = medications
        self._mark_as_updated()
    
    def update_last_diagnoses(self, diagnoses: str) -> None:
        """Atualiza últimos diagnósticos"""
        self._last_diagnoses = diagnoses
        self._mark_as_updated()
    
    def add_tag(self, tag: str) -> None:
        """Adiciona uma tag ao prontuário"""
        if tag and tag not in self._tags:
            self._tags.append(tag)
            self._mark_as_updated()
    
    def remove_tag(self, tag: str) -> None:
        """Remove uma tag do prontuário"""
        if tag in self._tags:
            self._tags.remove(tag)
            self._mark_as_updated()
    
    def update_tags(self, tags: List[str]) -> None:
        """Atualiza todas as tags"""
        self._tags = tags or []
        self._mark_as_updated()
    
    def _mark_as_updated(self) -> None:
        """Marca o registro como atualizado"""
        self._updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade para dicionário"""
        return {
            "id": self._id,
            "patient_id": self._patient_id,
            "professional_id": self._professional_id,
            "company_id": self._company_id,
            "clinical_history": self._clinical_history,
            "surgical_history": self._surgical_history,
            "family_history": self._family_history,
            "habits": self._habits,
            "allergies": self._allergies,
            "current_medications": self._current_medications,
            "last_diagnoses": self._last_diagnoses,
            "tags": self._tags,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    def __eq__(self, other) -> bool:
        """Compara entidades por ID"""
        if not isinstance(other, Record):
            return False
        return self._id == other._id
    
    def __repr__(self) -> str:
        return f"Record(id={self._id}, patient_id={self._patient_id})"