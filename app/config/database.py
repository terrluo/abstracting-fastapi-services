from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL or "sqlite:///./app.db",
    connect_args={"check_same_thread": False},
)

read_engine = create_engine(
    settings.READ_SQLALCHEMY_DATABASE_URL or "sqlite:///./app.db",
    connect_args={"check_same_thread": False},
)

session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

read_session_factory = sessionmaker(read_engine)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


def get_db():
    db: Session = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_read_db():
    db: Session = read_session_factory()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
