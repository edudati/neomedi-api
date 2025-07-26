from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class AddressBase(BaseModel):
    """Schema base para Address"""
    street: str = Field(..., description="Rua/Avenida")
    number: str = Field(..., description="Número")
    complement: Optional[str] = Field(None, description="Bloco, apto, sala")
    neighbourhood: str = Field(..., description="Bairro")
    city: str = Field(..., description="Cidade")
    state: str = Field(..., description="Estado (sigla ou nome completo)")
    zip_code: str = Field(..., description="CEP")
    country: str = Field("Brasil", description="País")
    latitude: Optional[float] = Field(None, description="Coordenada latitude")
    longitude: Optional[float] = Field(None, description="Coordenada longitude")


class AddressCreate(AddressBase):
    """Schema para criação de Address"""
    user_id: UUID


class AddressUpdate(BaseModel):
    """Schema para atualização de Address"""
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighbourhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AddressResponse(AddressBase):
    """Schema para resposta de Address"""
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class AddressWithUserResponse(AddressResponse):
    """Schema para resposta de Address com dados do usuário"""
    user: dict  # Dados básicos do User

    class Config:
        from_attributes = True 