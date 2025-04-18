from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from database_config import url_to_db

# Створення підключення до бази даних
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    # Перевірка підключення
    try:
        connection = engine.connect()
        print("Підключення до бази даних успішне!")
        connection.close()
    except Exception as e:
        print("Помилка підключення до бази даних:", e)