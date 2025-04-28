from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class NetBoxEndpoint(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    ip_address: str = Field(index=True)
    domain: str = Field(index=True)
    port: int = Field(default=443)  # Default to HTTPS port
    token: str = Field()
    verify_ssl: bool = Field(default=True)
    
    @property
    def url(self) -> str:
        """Construct the full URL for the NetBox endpoint."""
        # Use HTTPS if port is 443 or verify_ssl is True
        protocol = 'https' if self.port == 443 or self.verify_ssl else 'http'
        host = self.domain if self.domain else self.ip_address.split('/')[0]
        return f"{protocol}://{host}:{self.port}"

def create_db_and_tables():
    # Drop existing tables and recreate them to ensure schema changes are applied
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]