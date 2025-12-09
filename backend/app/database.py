from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path
import socket
from urllib.parse import urlparse, urlunparse

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")


def _force_ipv4_in_url(db_url: str) -> str:
    try:
        parsed = urlparse(db_url)
        host = parsed.hostname
        port = parsed.port
        if not host:
            return db_url
        # Resolve only IPv4 addresses
        infos = socket.getaddrinfo(
            host, port or 5432, family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        if not infos:
            return db_url
        ipv4 = infos[0][4][0]
        # Rebuild URL with IPv4 literal
        netloc = (
            f"{parsed.username}:{parsed.password}@{ipv4}:{port}"
            if parsed.username and parsed.password
            else f"{ipv4}:{port}"
        )
        new_parsed = parsed._replace(netloc=netloc)
        return urlunparse(new_parsed)
    except Exception:
        return db_url


# Force IPv4 to avoid IPv6 'Network is unreachable' in some Docker/WIN networks
SQLALCHEMY_DATABASE_URL = _force_ipv4_in_url(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 10,
    },
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
