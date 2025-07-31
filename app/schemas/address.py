from pydantic import BaseModel, Field, model_validator
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
    user_id: Optional[UUID] = None
    company_id: Optional[UUID] = None

    @model_validator(mode="after")
    def check_user_or_company(cls, values):
        user_id = values.user_id
        company_id = values.company_id
        if not user_id and not company_id:
            raise ValueError('É necessário informar user_id ou company_id.')
        if user_id and company_id:
            raise ValueError('Informe apenas user_id ou company_id, não ambos.')
        return values


class AddressCreateForCompany(AddressBase):
    """Schema para criação de Address de company (sem user_id/company_id)"""
    pass


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


class UserAddressUpdate(AddressUpdate):
    """Schema para atualização de endereço de usuário"""
    pass


class CompanyAddressUpdate(AddressUpdate):
    """Schema para atualização de endereço de empresa"""
    company_id: UUID


class AddressResponse(AddressBase):
    """Schema para resposta de Address"""
    id: UUID
    user_id: Optional[UUID] = None
    company_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class AddressWithUserResponse(AddressResponse):
    """Schema para resposta de Address com dados do usuário"""
    user: dict  # Dados básicos do User

    class Config:
        from_attributes = True 