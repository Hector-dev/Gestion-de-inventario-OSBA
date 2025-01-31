# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class Database:
    def __init__(self):
        # Obtiene la ruta del directorio actual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo de la base de datos
        db_path = os.path.join(current_dir, '..', 'bodega.db')
        # Crea el engine de SQLAlchemy
        self.engine = create_engine(f'sqlite:///{db_path}')
        # Crea una clase de sesión
        Session = sessionmaker(bind=self.engine)
        # Crea una instancia de sesión
        self.session = Session()
        
    def create_tables(self):
        """Crea todas las tablas definidas en los modelos"""
        from db.models import Base  # Importa el Base registrado con los modelos
        Base.metadata.create_all(self.engine)  # Usa el Base correcto
        
    def close(self):
        """Cierra la sesión de la base de datos"""
        self.session.close()
