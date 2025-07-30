from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import re


class CompanyBase(BaseModel):
    """Schema base para Company"""
    name: str
    legal_name: str
    legal_id: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True
    is_visible: bool = True
    is_public: bool = False

    @validator('legal_id')
    def validate_cnpj(cls, v):
        """Validar formato do CNPJ"""
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', v)
        
        if len(cnpj) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        
        # Validação básica de CNPJ
        if cnpj == '00000000000000' or cnpj == '11111111111111' or \
           cnpj == '22222222222222' or cnpj == '33333333333333' or \
           cnpj == '44444444444444' or cnpj == '55555555555555' or \
           cnpj == '66666666666666' or cnpj == '77777777777777' or \
           cnpj == '88888888888888' or cnpj == '99999999999999':
            raise ValueError('CNPJ inválido')
        
        # Validação dos dígitos verificadores
        soma = 0
        peso = 2
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = peso + 1 if peso < 9 else 2
        
        digito1 = 11 - (soma % 11)
        if digito1 > 9:
            digito1 = 0
        
        soma = 0
        peso = 2
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = peso + 1 if peso < 9 else 2
        
        digito2 = 11 - (soma % 11)
        if digito2 > 9:
            digito2 = 0
        
        if int(cnpj[12]) != digito1 or int(cnpj[13]) != digito2:
            raise ValueError('CNPJ inválido')
        
        return v

    @validator('phone')
    def validate_phone(cls, v):
        """Validar formato do telefone"""
        if v is None:
            return v
        
        # Remove caracteres não numéricos
        phone = re.sub(r'[^0-9]', '', v)
        
        if len(phone) < 10 or len(phone) > 11:
            raise ValueError('Telefone deve ter 10 ou 11 dígitos')
        
        return v


class CompanyCreate(CompanyBase):
    """Schema para criação de Company"""
    user_id: UUID
    address_id: Optional[UUID] = None


class CompanyUpdate(BaseModel):
    """Schema para atualização de Company"""
    name: Optional[str] = None
    legal_name: Optional[str] = None
    legal_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    is_visible: Optional[bool] = None
    is_public: Optional[bool] = None

    @validator('legal_id')
    def validate_cnpj(cls, v):
        """Validar formato do CNPJ"""
        if v is None:
            return v
        
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', v)
        
        if len(cnpj) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        
        # Validação básica de CNPJ
        if cnpj == '00000000000000' or cnpj == '11111111111111' or \
           cnpj == '22222222222222' or cnpj == '33333333333333' or \
           cnpj == '44444444444444' or cnpj == '55555555555555' or \
           cnpj == '66666666666666' or cnpj == '77777777777777' or \
           cnpj == '88888888888888' or cnpj == '99999999999999':
            raise ValueError('CNPJ inválido')
        
        # Validação dos dígitos verificadores
        soma = 0
        peso = 2
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = peso + 1 if peso < 9 else 2
        
        digito1 = 11 - (soma % 11)
        if digito1 > 9:
            digito1 = 0
        
        soma = 0
        peso = 2
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = peso + 1 if peso < 9 else 2
        
        digito2 = 11 - (soma % 11)
        if digito2 > 9:
            digito2 = 0
        
        if int(cnpj[12]) != digito1 or int(cnpj[13]) != digito2:
            raise ValueError('CNPJ inválido')
        
        return v

    @validator('phone')
    def validate_phone(cls, v):
        """Validar formato do telefone"""
        if v is None:
            return v
        
        # Remove caracteres não numéricos
        phone = re.sub(r'[^0-9]', '', v)
        
        if len(phone) < 10 or len(phone) > 11:
            raise ValueError('Telefone deve ter 10 ou 11 dígitos')
        
        return v


class CompanyResponse(CompanyBase):
    """Schema para resposta de Company"""
    id: UUID
    user_id: UUID
    address_id: Optional[UUID] = None
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyWithAddressResponse(CompanyResponse):
    """Schema para resposta de Company com dados do endereço"""
    address: Optional[dict] = None

    class Config:
        from_attributes = True 