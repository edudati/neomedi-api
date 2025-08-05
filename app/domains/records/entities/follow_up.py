"""
FollowUp Entity - Evolução Rápida
Representa registro breve de evolução ou nota entre atendimentos formais.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4


class FollowUp:
    """
    Entidade FollowUp - Evolução Rápida
    
    Representa um registro breve de evolução ou nota entre atendimentos.
    Permite acompanhamento contínuo do paciente de forma simplificada.
    """
    
    def __init__(
        self,
        record_id: UUID,
        note: str,
        visit_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        follow_up_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = follow_up_id or uuid4()
        self._record_id = record_id
        self._visit_id = visit_id
        self._note = note
        self._tags = tags or []
        self._created_at = created_at or datetime.utcnow()
        
        # Validações
        self._validate()
    
    def _validate(self) -> None:
        """Valida regras de negócio da entidade"""
        if not self._record_id:
            raise ValueError("Record ID é obrigatório")
        if not self._note or not self._note.strip():
            raise ValueError("Nota é obrigatória e não pode estar vazia")
    
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
    def note(self) -> str:
        return self._note
    
    @property
    def tags(self) -> List[str]:
        return self._tags.copy()
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    # Business Methods
    def update_note(self, note: str) -> None:
        """Atualiza a nota do follow-up"""
        if not note or not note.strip():
            raise ValueError("Nota não pode estar vazia")
        self._note = note
    
    def add_tag(self, tag: str) -> None:
        """Adiciona uma tag ao follow-up"""
        if tag and tag not in self._tags:
            self._tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove uma tag do follow-up"""
        if tag in self._tags:
            self._tags.remove(tag)
    
    def update_tags(self, tags: List[str]) -> None:
        """Atualiza todas as tags"""
        self._tags = tags or []
    
    def link_to_visit(self, visit_id: UUID) -> None:
        """Vincula o follow-up a um atendimento específico"""
        self._visit_id = visit_id
    
    def unlink_from_visit(self) -> None:
        """Remove a vinculação com atendimento"""
        self._visit_id = None
    
    def is_linked_to_visit(self) -> bool:
        """Verifica se está vinculado a um atendimento"""
        return self._visit_id is not None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade para dicionário"""
        return {
            "id": self._id,
            "record_id": self._record_id,
            "visit_id": self._visit_id,
            "note": self._note,
            "tags": self._tags,
            "created_at": self._created_at
        }
    
    def __eq__(self, other) -> bool:
        """Compara entidades por ID"""
        if not isinstance(other, FollowUp):
            return False
        return self._id == other._id
    
    def __repr__(self) -> str:
        return f"FollowUp(id={self._id}, record_id={self._record_id})"