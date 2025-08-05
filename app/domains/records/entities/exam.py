"""
Exam Entity - Exame Clínico, Laboratorial ou de Imagem
Representa registro de exames solicitados e resultados do paciente.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from enum import Enum


class ExamType(Enum):
    """Tipos de exame disponíveis"""
    CLINICAL = "clinical"      # Exame clínico  
    LABORATORY = "laboratory"  # Exame laboratorial
    IMAGE = "image"           # Exame de imagem


class Exam:
    """
    Entidade Exam - Exame Clínico, Laboratorial ou de Imagem
    
    Representa um exame solicitado para o paciente, incluindo
    informações de solicitação e resultados.
    """
    
    def __init__(
        self,
        record_id: UUID,
        exam_type: ExamType,
        name: str,
        requested_at: datetime,
        visit_id: Optional[UUID] = None,
        result_text: Optional[str] = None,
        result_file: Optional[str] = None,
        exam_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = exam_id or uuid4()
        self._record_id = record_id
        self._visit_id = visit_id
        self._type = exam_type
        self._name = name
        self._requested_at = requested_at
        self._result_text = result_text
        self._result_file = result_file
        self._created_at = created_at or datetime.utcnow()
        
        # Validações
        self._validate()
    
    def _validate(self) -> None:
        """Valida regras de negócio da entidade"""
        if not self._record_id:
            raise ValueError("Record ID é obrigatório")
        if not self._name or not self._name.strip():
            raise ValueError("Nome do exame é obrigatório")
        if not isinstance(self._type, ExamType):
            raise ValueError("Tipo de exame deve ser uma instância de ExamType")
        if not self._requested_at:
            raise ValueError("Data de solicitação é obrigatória")
    
    # Properties (Getters)
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def record_id(self) -> UUID:
        return self._record_id
    
    @property
    def visit_id(self) -> Optional[UUID]:
        return self._visit_id
    
    @property
    def type(self) -> ExamType:
        return self._type
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def requested_at(self) -> datetime:
        return self._requested_at
    
    @property
    def result_text(self) -> Optional[str]:
        return self._result_text
    
    @property
    def result_file(self) -> Optional[str]:
        return self._result_file
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    # Business Methods
    def update_name(self, name: str) -> None:
        """Atualiza o nome do exame"""
        if not name or not name.strip():
            raise ValueError("Nome do exame não pode estar vazio")
        self._name = name
    
    def update_result_text(self, result_text: str) -> None:
        """Atualiza resultado em texto do exame"""
        self._result_text = result_text
    
    def update_result_file(self, result_file: str) -> None:
        """Atualiza arquivo de resultado do exame"""
        self._result_file = result_file
    
    def add_results(self, result_text: Optional[str] = None, result_file: Optional[str] = None) -> None:
        """Adiciona resultados ao exame"""
        if result_text:
            self._result_text = result_text
        if result_file:
            self._result_file = result_file
    
    def link_to_visit(self, visit_id: UUID) -> None:
        """Vincula o exame a um atendimento específico"""
        self._visit_id = visit_id
    
    def unlink_from_visit(self) -> None:
        """Remove a vinculação com atendimento"""
        self._visit_id = None
    
    def has_results(self) -> bool:
        """Verifica se o exame possui resultados"""
        return bool(self._result_text or self._result_file)
    
    def is_linked_to_visit(self) -> bool:
        """Verifica se está vinculado a um atendimento"""
        return self._visit_id is not None
    
    def is_complete(self) -> bool:
        """Verifica se o exame está completo (com resultados)"""
        return self.has_results()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade para dicionário"""
        return {
            "id": self._id,
            "record_id": self._record_id,
            "visit_id": self._visit_id,
            "type": self._type.value,
            "name": self._name,
            "requested_at": self._requested_at,
            "result_text": self._result_text,
            "result_file": self._result_file,
            "created_at": self._created_at
        }
    
    def __eq__(self, other) -> bool:
        """Compara entidades por ID"""
        if not isinstance(other, Exam):
            return False
        return self._id == other._id
    
    def __repr__(self) -> str:
        return f"Exam(id={self._id}, name='{self._name}', type={self._type.value})"