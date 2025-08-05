"""
DecisionSupport Entity - Suporte à Decisão
Representa suporte à decisão clínica gerado por LLM com base nos dados do paciente.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class DecisionSupport:
    """
    Entidade DecisionSupport - Suporte à Decisão Clínica
    
    Representa uma análise e sugestão gerada por LLM para auxiliar
    na tomada de decisão clínica baseada nos dados do paciente.
    """
    
    def __init__(
        self,
        record_id: UUID,
        visit_id: UUID,
        professional_id: UUID,
        llm_model: str,
        sentiment_summary: Optional[str] = None,
        symptom_summary: Optional[str] = None,
        goal_summary: Optional[str] = None,
        practice_summary: Optional[str] = None,
        insight_summary: Optional[str] = None,
        suggested_conduct: Optional[str] = None,
        evidence_summary: Optional[str] = None,
        decision_support_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = decision_support_id or uuid4()
        self._record_id = record_id
        self._visit_id = visit_id
        self._professional_id = professional_id
        self._sentiment_summary = sentiment_summary
        self._symptom_summary = symptom_summary
        self._goal_summary = goal_summary
        self._practice_summary = practice_summary
        self._insight_summary = insight_summary
        self._suggested_conduct = suggested_conduct
        self._evidence_summary = evidence_summary
        self._llm_model = llm_model
        self._created_at = created_at or datetime.utcnow()
        
        # Validações
        self._validate()
    
    def _validate(self) -> None:
        """Valida regras de negócio da entidade"""
        if not self._record_id:
            raise ValueError("Record ID é obrigatório")
        if not self._visit_id:
            raise ValueError("Visit ID é obrigatório")
        if not self._professional_id:
            raise ValueError("Professional ID é obrigatório")
        if not self._llm_model or not self._llm_model.strip():
            raise ValueError("Modelo LLM é obrigatório")
    
    # Properties (Getters)
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def record_id(self) -> UUID:
        return self._record_id
    
    @property
    def visit_id(self) -> UUID:
        return self._visit_id
    
    @property
    def professional_id(self) -> UUID:
        return self._professional_id
    
    @property
    def sentiment_summary(self) -> Optional[str]:
        return self._sentiment_summary
    
    @property
    def symptom_summary(self) -> Optional[str]:
        return self._symptom_summary
    
    @property
    def goal_summary(self) -> Optional[str]:
        return self._goal_summary
    
    @property
    def practice_summary(self) -> Optional[str]:
        return self._practice_summary
    
    @property
    def insight_summary(self) -> Optional[str]:
        return self._insight_summary
    
    @property
    def suggested_conduct(self) -> Optional[str]:
        return self._suggested_conduct
    
    @property
    def evidence_summary(self) -> Optional[str]:
        return self._evidence_summary
    
    @property
    def llm_model(self) -> str:
        return self._llm_model
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    # Business Methods
    def update_sentiment_summary(self, sentiment_summary: str) -> None:
        """Atualiza resumo da nuvem de sentimentos"""
        self._sentiment_summary = sentiment_summary
    
    def update_symptom_summary(self, symptom_summary: str) -> None:
        """Atualiza resumo da nuvem de sintomas percebidos"""
        self._symptom_summary = symptom_summary
    
    def update_goal_summary(self, goal_summary: str) -> None:
        """Atualiza resumo da nuvem de intenções ou objetivos"""
        self._goal_summary = goal_summary
    
    def update_practice_summary(self, practice_summary: str) -> None:
        """Atualiza resumo da nuvem de experiências ou práticas"""
        self._practice_summary = practice_summary
    
    def update_insight_summary(self, insight_summary: str) -> None:
        """Atualiza resumo da nuvem de insights ou autoavaliações"""
        self._insight_summary = insight_summary
    
    def update_suggested_conduct(self, suggested_conduct: str) -> None:
        """Atualiza conduta sugerida pelo LLM"""
        self._suggested_conduct = suggested_conduct
    
    def update_evidence_summary(self, evidence_summary: str) -> None:
        """Atualiza resumo de literatura ou protocolos usados"""
        self._evidence_summary = evidence_summary
    
    def has_summaries(self) -> bool:
        """Verifica se possui ao menos um resumo"""
        return bool(
            self._sentiment_summary or 
            self._symptom_summary or 
            self._goal_summary or 
            self._practice_summary or 
            self._insight_summary
        )
    
    def has_suggestions(self) -> bool:
        """Verifica se possui sugestões ou evidências"""
        return bool(self._suggested_conduct or self._evidence_summary)
    
    def is_complete(self) -> bool:
        """Verifica se o suporte à decisão está completo"""
        return self.has_summaries() and self.has_suggestions()
    
    def get_summary_count(self) -> int:
        """Retorna quantidade de resumos preenchidos"""
        summaries = [
            self._sentiment_summary,
            self._symptom_summary,
            self._goal_summary,
            self._practice_summary,
            self._insight_summary
        ]
        return sum(1 for summary in summaries if summary)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade para dicionário"""
        return {
            "id": self._id,
            "record_id": self._record_id,
            "visit_id": self._visit_id,
            "professional_id": self._professional_id,
            "sentiment_summary": self._sentiment_summary,
            "symptom_summary": self._symptom_summary,
            "goal_summary": self._goal_summary,
            "practice_summary": self._practice_summary,
            "insight_summary": self._insight_summary,
            "suggested_conduct": self._suggested_conduct,
            "evidence_summary": self._evidence_summary,
            "llm_model": self._llm_model,
            "created_at": self._created_at
        }
    
    def __eq__(self, other) -> bool:
        """Compara entidades por ID"""
        if not isinstance(other, DecisionSupport):
            return False
        return self._id == other._id
    
    def __repr__(self) -> str:
        return f"DecisionSupport(id={self._id}, visit_id={self._visit_id}, model='{self._llm_model}')"