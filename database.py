from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# On essaie de récupérer les informations de connexion depuis Azure
# Ces variables ("DB_HOST", etc.) seront configurées dans Azure plus tard
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "postgres") # Par défaut, on utilise la base 'postgres'

# LOGIQUE DE BASCULEMENT (SWITCH)
if DB_HOST:
    # --- MODE PRODUCTION (SUR AZURE) ---
    print(f"Connexion à la base de données PostgreSQL : {DB_HOST}...")
    
    # Construction de l'URL de connexion pour PostgreSQL
    # Format : postgresql://utilisateur:motdepasse@serveur/nom_base
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    
    # Azure exige souvent une connexion sécurisée (SSL)
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"sslmode": "require"})

else:
    # --- MODE DEVELOPPEMENT (LOCAL) ---
    print("Aucune variable Azure détectée. Utilisation de SQLite local.")
    
    SQLALCHEMY_DATABASE_URL = "sqlite:///./travel.db"
    # check_same_thread est nécessaire uniquement pour SQLite
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()
