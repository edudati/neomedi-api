#!/usr/bin/env python3
"""
Script de manutenção para criar companies para usuários admin legados
que não possuem company associada.
"""

import sys
import os
from uuid import UUID
from sqlalchemy.orm import Session

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.address import Address
from app.services.company_service import CompanyService


def create_companies_for_admin_users():
    """Criar companies para usuários admin que não possuem company"""
    
    # Obter sessão do banco
    db = SessionLocal()
    
    try:
        # Verificar se há usuários no banco
        total_users = db.query(User).count()
        print(f"Total de usuários no banco: {total_users}")
        
        # Verificar usuários admin
        admin_users = db.query(User).filter(
            User.role == UserRole.ADMIN,
            User.is_active == True
        ).all()
        
        print(f"Encontrados {len(admin_users)} usuários admin ativos")
        
        if not admin_users:
            print("Nenhum usuário admin encontrado!")
            # Listar todos os usuários para debug
            all_users = db.query(User).all()
            print("Usuários existentes:")
            for user in all_users:
                print(f"  - {user.name} (Role: {user.role}, Ativo: {user.is_active})")
            return
        
        companies_created = 0
        
        for user in admin_users:
            print(f"Verificando usuário: {user.name} (ID: {user.id})")
            
            # Verificar se o usuário já possui company
            existing_company = db.query(Company).filter(
                Company.user_id == user.id,
                Company.is_deleted == False
            ).first()
            
            if existing_company:
                print(f"  → Já possui company: {existing_company.name}")
                continue
            
            # Verificar se o usuário tem auth_user
            if not user.auth_user:
                print(f"  ✗ Usuário não tem auth_user associado")
                continue
            
            # Criar company para o usuário
            try:
                print(f"  → Criando company...")
                company = CompanyService.create_company_for_admin(
                    db=db,
                    user_id=user.id,
                    user_name=user.name,
                    user_email=user.auth_user.email
                )
                
                companies_created += 1
                print(f"  ✓ Company criada: {company.name}")
                
            except Exception as e:
                print(f"  ✗ Erro: {str(e)}")
        
        print(f"\nResumo:")
        print(f"- Usuários admin verificados: {len(admin_users)}")
        print(f"- Companies criadas: {companies_created}")
        
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        db.rollback()
    finally:
        db.close()


def create_addresses_for_companies():
    """Criar endereços em branco para companies que não possuem endereço"""
    
    # Obter sessão do banco
    db = SessionLocal()
    
    try:
        # Buscar todas as companies ativas
        companies = db.query(Company).filter(
            Company.is_deleted == False
        ).all()
        
        print(f"Encontradas {len(companies)} companies ativas")
        
        addresses_created = 0
        
        for company in companies:
            print(f"Verificando company: {company.name} (ID: {company.id})")
            
            # Verificar se a company já possui endereço
            existing_address = db.query(Address).filter(
                Address.company_id == company.id
            ).first()
            
            if existing_address:
                print(f"  → Já possui endereço: {existing_address.street}, {existing_address.number}")
                continue
            
            # Criar endereço em branco para a company
            try:
                print(f"  → Criando endereço em branco...")
                address_data = {
                    "street": "",
                    "number": "",
                    "complement": "",
                    "neighbourhood": "",
                    "city": "",
                    "state": "",
                    "zip_code": "",
                    "country": "Brasil",
                    "latitude": None,
                    "longitude": None,
                    "company_id": company.id
                }
                
                new_address = Address(**address_data)
                db.add(new_address)
                db.commit()
                db.refresh(new_address)
                
                addresses_created += 1
                print(f"  ✓ Endereço criado (ID: {new_address.id})")
                
            except Exception as e:
                print(f"  ✗ Erro: {str(e)}")
                db.rollback()
        
        print(f"\nResumo:")
        print(f"- Companies verificadas: {len(companies)}")
        print(f"- Endereços criados: {addresses_created}")
        
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=== Script de Manutenção ===")
    print("1. Criar companies para admins")
    print("2. Criar endereços em branco para companies")
    print("3. Executar ambos")
    print()
    
    choice = input("Escolha uma opção (1/2/3): ").strip()
    
    if choice == "1":
        print("\n=== Criando Companies para Admins ===")
        response = input("Deseja continuar? (s/N): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            create_companies_for_admin_users()
        else:
            print("Operação cancelada.")
    
    elif choice == "2":
        print("\n=== Criando Endereços para Companies ===")
        response = input("Deseja continuar? (s/N): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            create_addresses_for_companies()
        else:
            print("Operação cancelada.")
    
    elif choice == "3":
        print("\n=== Executando Ambos ===")
        response = input("Deseja continuar? (s/N): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            create_companies_for_admin_users()
            print("\n" + "="*50 + "\n")
            create_addresses_for_companies()
        else:
            print("Operação cancelada.")
    
    else:
        print("Opção inválida.") 