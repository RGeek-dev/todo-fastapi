from app.config.database import Base, engine
from app.models.todo import Todo


Base.metadata.create_all(bind=engine)

