This project is a web application like Jira. Key features include:

- Authentication using JWT token
- Create, view and edit tasks
- Large permission system 
- API documentation in Swagger

**To run this application locally, follow these steps:**

Clone the repository: git clone https://github.com/AnastasiaSavenok/customJira.git

Go to the project directory: cd customJira/

Create a .env file and specify the following variables in it:

- SECRET_KEY 
- DEBUG
- DJANGO_ALLOWED_HOSTS
- POSTGRES_ENGINE = django.db.backends.postgresql_psycopg2
- POSTGRES_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT

Launch the application in one of two ways:
- Build and run Docker containers: **docker-compose up --build**
- Install requirements: **pip install -r requirements.txt** and run: **python manage.py runserver**
  
Open the swagger application documentation in a browser: http://localhost:8000/api/v1/docs/
