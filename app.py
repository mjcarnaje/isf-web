from web import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()
celery_app = app.extensions["celery"]

if __name__ == '__main__':
    app.run(debug=True)
