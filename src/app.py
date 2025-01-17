from src import create_app, ext_celery
from src.database import default_db, init_db
from src.config import settings

from .tasks import import_csv_task # noqa

app = create_app(db=default_db)
celery = ext_celery.celery

if __name__ == "__main__":
    app.run(
        host=settings.FLASK_RUN_HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )

