from sqlalchemy import Column, ForeignKey, Integer, String, relationship
from .database import Base

class User(Base):
    __tablename__="users"
    user_id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    profiles = relationship("Perfil", backref="usuario", lazy=False, uselist=True, primaryjoin="usuarios.id_usuario == perfiles.id_usuario")
    favoriteProfiles = relationship("Perfil", backref="usuario", lazy=False, uselist=True, primaryjoin="usuarios.id_usuario == perfiles.id_usuario")

class Profile(Base):
    __tablename__ = "profiles"
    profile_id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)