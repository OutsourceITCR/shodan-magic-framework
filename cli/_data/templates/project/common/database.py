import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
migrate = Migrate()

engine = None
SessionLocal = None


def init_db(app, schema="public"):
    base_uri = app.config.get("DATABASE_URI", "")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{base_uri}?options=-c%20search_path%3D{schema}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)


def init_standalone_db(schema="public"):
    """Initialize database session without Flask."""
    database_uri = os.getenv("DATABASE_URI")
    global engine, SessionLocal
    db_uri = f"{database_uri}?options=-c%20search_path%3D{schema}"
    engine = create_engine(db_uri, pool_pre_ping=True)
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    return SessionLocal  # Return session for seeders to use
