from app.db.database import engine
from app.models import Base

def create_tables():
    print("creating tables")
    Base.metadata.create_all(bind=engine)
    print("tables are created")

if __name__ == "__main__":
    create_tables()
