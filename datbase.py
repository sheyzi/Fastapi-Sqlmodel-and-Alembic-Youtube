from sqlmodel import Session, create_engine, SQLModel

sqlite_file_url = "sqlite:///database.sqlite"
engine = create_engine(
    sqlite_file_url, echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_db():
    with Session(engine) as db:
        try:
            yield db
        finally:
            db.close()
