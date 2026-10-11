import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
if DATABASE_URL.startswith("sqlite"):
    Path("data").mkdir(parents=True, exist_ok=True)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(500))


class MessageInput(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class MessageOutput(MessageInput):
    id: int


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(title="SBSB Demo App", lifespan=lifespan)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from the SBSB web + database demo app"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/messages", response_model=list[MessageOutput])
def list_messages() -> list[MessageOutput]:
    with Session(engine) as session:
        rows = session.scalars(select(Message).order_by(Message.id.desc())).all()
        return [MessageOutput(id=row.id, text=row.text) for row in rows]


@app.post("/messages", response_model=MessageOutput, status_code=201)
def create_message(payload: MessageInput) -> MessageOutput:
    with Session(engine) as session:
        message = Message(text=payload.text)
        session.add(message)
        session.commit()
        session.refresh(message)
        return MessageOutput(id=message.id, text=message.text)


@app.get("/messages/{message_id}", response_model=MessageOutput)
def get_message(message_id: int) -> MessageOutput:
    with Session(engine) as session:
        message = session.get(Message, message_id)
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageOutput(id=message.id, text=message.text)
