from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user_client import UserClient
from app.models.client_professional_company import ClientProfessionalCompany
from app.models.user import UserRole
from app.models.user_professional import UserProfessional
from app.models.company import Company
from fastapi import HTTPException, status
from typing import Optional
import logging

# Configurar logger
logger = logging.getLogger(__name__)

class UserClientService:
    @staticmethod
    def create_user_client(
        db: Session, 
        professional_user_id: UUID,
        company_id: UUID,
        client_name: str,
        firebase_token: str
    ) -> dict:
        """
        Cria um novo client associado a um professional e company.
        
        Args:
            db: Sessão do banco
            professional_user_id: ID do user professional (vem do JWT)
            company_id: ID da company onde o client será criado
            client_name: Nome do novo client (enviado pelo front)
            firebase_token: Token do Firebase para criar AuthUser do client
        """
        try:
            logger.info(f"Iniciando criação de client: professional_id={professional_user_id}, company_id={company_id}, client_name={client_name}")
            
            from app.services.auth import AuthService
            from app.services.user import UserService
            from app.services.address import AddressService
            
            # 1. Validar se o professional existe e tem role PROFESSIONAL
            logger.info("Validando professional...")
            professional_user = db.query(UserProfessional).filter(
                UserProfessional.user_id == professional_user_id
            ).first()
            
            if not professional_user:
                logger.error(f"Professional não encontrado: {professional_user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Professional não encontrado"
                )
            
            logger.info(f"Professional validado: {professional_user_id}")
            
            # 2. Validar se a company existe e pertence ao professional
            logger.info("Validando company...")
            company = db.query(Company).filter(
                Company.id == company_id,
                Company.user_professional_id == professional_user_id
            ).first()
            
            if not company:
                logger.error(f"Company não encontrada ou não pertence ao professional: {company_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company não encontrada ou não pertence ao professional"
                )
            
            logger.info(f"Company validada: {company_id}")
            
            # 3. Criar AuthUser do client usando o firebase_token
            logger.info("Criando AuthUser do client...")
            try:
                auth_user = AuthService.create_auth_user_from_firebase(db, firebase_token)
                logger.info(f"AuthUser criado com sucesso: {auth_user.id}")
            except Exception as e:
                logger.error(f"Erro ao criar AuthUser: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao criar AuthUser: {str(e)}"
                )
            
            # 4. Criar User com role CLIENT usando o nome enviado pelo front
            # e dados do AuthUser (email e picture)
            logger.info("Criando User com role CLIENT...")
            try:
                user = UserService.create_user(
                    db=db, 
                    auth_user=auth_user, 
                    role=UserRole.CLIENT,
                    name=client_name  # Usar o nome enviado pelo front
                )
                logger.info(f"User criado com sucesso: {user.id}")
            except Exception as e:
                logger.error(f"Erro ao criar User: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao criar User: {str(e)}"
                )
            
            # 5. Criar Address em branco para o User
            logger.info("Criando Address em branco...")
            try:
                address = AddressService.create_address(
                    db=db, 
                    user_id=user.id, 
                    street="", 
                    number="", 
                    neighbourhood="", 
                    city="", 
                    state="", 
                    zip_code="", 
                    country="Brasil"
                )
                logger.info(f"Address criado com sucesso: {address.id}")
            except Exception as e:
                logger.error(f"Erro ao criar Address: {str(e)}")
                # Por enquanto, vamos continuar sem criar o address para testar
                logger.warning("Continuando sem criar Address devido ao erro")
                address = None
            
            # 6. Criar UserClient em branco vinculado ao User
            logger.info("Criando UserClient...")
            try:
                user_client = UserClient(user_id=user.id)
                db.add(user_client)
                db.commit()
                db.refresh(user_client)
                logger.info(f"UserClient criado com sucesso: {user_client.user_id}")
            except Exception as e:
                logger.error(f"Erro ao criar UserClient: {str(e)}")
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao criar UserClient: {str(e)}"
                )
            
            # 7. Criar associação ClientProfessionalCompany
            logger.info("Criando associação ClientProfessionalCompany...")
            try:
                client_professional_company = ClientProfessionalCompany(
                    client_id=user_client.user_id,
                    professional_id=professional_user_id,
                    company_id=company_id
                )
                db.add(client_professional_company)
                db.commit()
                logger.info("Associação ClientProfessionalCompany criada com sucesso")
            except Exception as e:
                logger.error(f"Erro ao criar associação ClientProfessionalCompany: {str(e)}")
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao criar associação ClientProfessionalCompany: {str(e)}"
                )
            
            # 8. Retornar dados do client criado
            logger.info("Buscando dados do client criado...")
            try:
                client_data = UserClientService.get_client_with_auth(db, user_client.user_id)
                logger.info("Dados do client recuperados com sucesso")
            except Exception as e:
                logger.error(f"Erro ao buscar dados do client: {str(e)}")
                # Não falhar aqui, retornar dados básicos
                client_data = {
                    "user_id": user_client.user_id,
                    "notes": user_client.notes,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "role": user.role.value
                    }
                }
            
            logger.info("Client criado com sucesso!")
            return {
                "success": True,
                "message": "Client criado com sucesso",
                "client_id": user_client.user_id,
                "client_data": client_data
            }
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Erro inesperado na criação de client: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno na criação de client: {str(e)}"
            )
    
    @staticmethod
    def get_client_with_auth(db: Session, client_id: UUID, professional_user_id: Optional[UUID] = None) -> Optional[dict]:
        """Buscar client com dados de autenticação"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Buscando client com ID: {client_id}")
            
            from app.models.user import User
            from app.models.auth_user import AuthUser
            
            query = db.query(UserClient).join(User).join(AuthUser).filter(
                UserClient.user_id == client_id
            )
            
            # Se professional_user_id for fornecido, validar se o client pertence ao professional
            if professional_user_id:
                logger.info(f"Validando pertencimento ao professional: {professional_user_id}")
                query = query.join(ClientProfessionalCompany).filter(
                    ClientProfessionalCompany.professional_id == professional_user_id
                )
            
            user_client = query.first()
            
            if not user_client:
                logger.warning(f"Client não encontrado: {client_id}")
                return None
            
            logger.info(f"Client encontrado: {user_client.user_id}")
            
            # Buscar endereço do client
            logger.info("Buscando endereço do client...")
            address_data = None
            if user_client.user.address:
                logger.info("Endereço encontrado")
                address_data = {
                    "id": user_client.user.address.id,
                    "street": user_client.user.address.street,
                    "number": user_client.user.address.number,
                    "complement": user_client.user.address.complement,
                    "neighbourhood": user_client.user.address.neighbourhood,
                    "city": user_client.user.address.city,
                    "state": user_client.user.address.state,
                    "zip_code": user_client.user.address.zip_code,
                    "country": user_client.user.address.country,
                    "latitude": user_client.user.address.latitude,
                    "longitude": user_client.user.address.longitude
                }
            else:
                logger.info("Nenhum endereço encontrado")
            
            logger.info("Montando dados de resposta...")
            
            # Montar dados de resposta
            response_data = {
                "user_id": user_client.user_id,
                "notes": user_client.notes,
                "user": {
                    "id": user_client.user.id,
                    "auth_user_id": user_client.user.auth_user_id,
                    "name": user_client.user.name,
                    "email": user_client.user.email,
                    "picture": user_client.user.picture,
                    "phone": user_client.user.phone,
                    "birth_date": user_client.user.birth_date,
                    "gender": user_client.user.gender.value if user_client.user.gender else None,
                    "is_active": user_client.user.is_active,
                    "is_deleted": user_client.user.is_deleted,
                    "is_verified": user_client.user.is_verified,
                    "has_access": user_client.user.has_access,
                    "role": user_client.user.role.value,
                    "social_media": user_client.user.social_media,
                    "suspended_at": user_client.user.suspended_at,
                    "created_at": user_client.user.created_at,
                    "updated_at": user_client.user.updated_at,
                    "auth_user": {
                        "id": user_client.user.auth_user.id,
                        "email": user_client.user.auth_user.email,
                        "firebase_uid": user_client.user.auth_user.firebase_uid,
                        "display_name": user_client.user.auth_user.display_name,
                        "email_verified": user_client.user.auth_user.email_verified,
                        "picture": user_client.user.auth_user.picture
                    }
                },
                "address": address_data
            }
            
            logger.info("Dados de resposta montados com sucesso")
            return response_data
            
        except Exception as e:
            logger.error(f"Erro ao buscar client com auth: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    @staticmethod
    def get_clients_by_professional(
        db: Session, 
        professional_user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> list:
        """Listar clients de um professional"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Buscando clients do professional: {professional_user_id}")
            
            from app.models.user import User
            from app.models.auth_user import AuthUser
            
            # Buscar todos os clients do professional em uma única query
            clients = db.query(UserClient).join(User).join(AuthUser).join(
                ClientProfessionalCompany
            ).filter(
                ClientProfessionalCompany.professional_id == professional_user_id
            ).offset(skip).limit(limit).all()
            
            logger.info(f"Encontrados {len(clients)} clients")
            
            # Montar dados de resposta para cada client
            result = []
            for client in clients:
                try:
                    # Buscar endereço do client
                    address_data = None
                    if client.user.address:
                        address_data = {
                            "id": client.user.address.id,
                            "street": client.user.address.street,
                            "number": client.user.address.number,
                            "complement": client.user.address.complement,
                            "neighbourhood": client.user.address.neighbourhood,
                            "city": client.user.address.city,
                            "state": client.user.address.state,
                            "zip_code": client.user.address.zip_code,
                            "country": client.user.address.country,
                            "latitude": client.user.address.latitude,
                            "longitude": client.user.address.longitude
                        }
                    
                    client_data = {
                        "user_id": client.user_id,
                        "notes": client.notes,
                        "user": {
                            "id": client.user.id,
                            "auth_user_id": client.user.auth_user_id,
                            "name": client.user.name,
                            "email": client.user.email,
                            "picture": client.user.picture,
                            "phone": client.user.phone,
                            "birth_date": client.user.birth_date,
                            "gender": client.user.gender.value if client.user.gender else None,
                            "is_active": client.user.is_active,
                            "is_deleted": client.user.is_deleted,
                            "is_verified": client.user.is_verified,
                            "has_access": client.user.has_access,
                            "role": client.user.role.value,
                            "social_media": client.user.social_media,
                            "suspended_at": client.user.suspended_at,
                            "created_at": client.user.created_at,
                            "updated_at": client.user.updated_at,
                            "auth_user": {
                                "id": client.user.auth_user.id,
                                "email": client.user.auth_user.email,
                                "firebase_uid": client.user.auth_user.firebase_uid,
                                "display_name": client.user.auth_user.display_name,
                                "email_verified": client.user.auth_user.email_verified,
                                "picture": client.user.auth_user.picture
                            }
                        },
                        "address": address_data
                    }
                    result.append(client_data)
                    
                except Exception as e:
                    logger.error(f"Erro ao processar client {client.user_id}: {str(e)}")
                    # Continuar com os próximos clients
                    continue
            
            logger.info(f"Retornando {len(result)} clients processados")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao buscar clients do professional: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    @staticmethod
    def update_client_notes(
        db: Session, 
        client_id: UUID, 
        notes: str,
        professional_user_id: Optional[UUID] = None
    ) -> Optional[dict]:
        """Atualizar notas do client"""
        query = db.query(UserClient).filter(
            UserClient.user_id == client_id
        )
        
        # Se professional_user_id for fornecido, validar se o client pertence ao professional
        if professional_user_id:
            query = query.join(ClientProfessionalCompany).filter(
                ClientProfessionalCompany.professional_id == professional_user_id
            )
        
        user_client = query.first()
        
        if not user_client:
            return None
        
        user_client.notes = notes
        db.commit()
        db.refresh(user_client)
        
        return UserClientService.get_client_with_auth(db, client_id) 