# CSE Archive RESTful API

This is the source code of our REST API backend implemented with the Django framework, which is open source for educational purposes and contributions.

## Deployment

The steps described below are suitable for deploying this project in a development environment. If you intend to deploy this to production, you can read 
[this article](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04).

### Requirements

It is assumed that [Python](https://www.cherryservers.com/blog/install-python-on-ubuntu), [PIP](https://www.cherryservers.com/blog/how-to-install-pip-ubuntu) tool and [PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart) database are installed on your OS.

### Setup Database

To deploy the project you need a database, which you can create by entering the following command in the PostgreSQL shell, where `<db_name>` is the name of the database you want to create. Don't forget to exit the PostgreSQL shell after creating your database.

```bash
CREATE DATABASE <db_name>;
```

### Setup Virtual Environment

This project uses `pipenv` for its virtual environment, if you don't have pipenv already install it with

```bash
pip install pipenv
```

Now at the project root, use pipenv *install* command to install project dependencies listed in [Pipfile](https://github.com/CSE-Archive/archive-api/blob/main/Pipfile). After that, use its *shell* command to enable the newly created virtual environment

```bash
pipenv install
pipenv shell
```

### Environment Configuration

Copy the `.env.example` file content and paste it to a new file named `.env` at the project's root. Now fill in the variables values according to the description below.

- **DEBUG**: This Boolean variable can be **True** or **False** depending on environment. To run the program in the production environment, set the Boolean variable to False.
- **SECRET_KEY**: This is used to sign sensitive data, so it is important to generate a strong key. You can generate a key yourself or use the command
    ```bash
    python manage.py generate_secret_key
    ```
- **ALLOWED_HOSTS**: Specifies the hosts that Django can accept requests from. Separate multiple hosts with commas, or use `*` to accept all requests.
- **CORS_ALLOWED_ORIGIN_REGEXES**: This variable is a string representing regex that matches Origins that are authorized to make cross-site HTTP requests. If the DEBUG setting is True, this value will not be considered and all origins will be allowed.
- **DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT**: These variables describe the database you created for this project.

### Running the API

Now that everything is ready, you can run the following commands to start the API.

First, we should apply database migrations

```bash
python manage.py migrate
```

To use the sample data, run this command (Optional)

```bash
python manage.py loaddata fixtures/admin_interface_theme_uswds.json fixtures/courses.json fixtures/course_relations.json fixtures/chartnodes.json fixtures/professors.json fixtures/tas.json fixtures/classrooms.json fixtures/references.json fixtures/resources.json fixtures/recordings.json
```

Now use this command to start an instance of API on your local machine

```bash
python manage.py runserver 
```

By default, you can access the project at `localhost:8000`, the admin panel at `/admin` route, and the API documentation at `/swagger` route.

## Database Design

To generate a diagram of the models used in the API, make sure you have [Graphviz](https://graphviz.org/download) on your OS. Then, run the following commands:

```bash
python manage.py graph_models -a -g --dot -o cse_archive_erd.dot
dot -Tpng cse_archive_erd.dot -o cse_archive_erd.png
```

## Contribution

Contributions of any size are welcomed here. You only need to:

1. Fork the project.
2. Make your changes in a new branch.
3. Create a Pull Request with a title that summarizes your changes and a description that explains your changes in more detail.

If you have any enhancement ideas but don't feel like doing it yourself, you can always [open a new issue](https://github.com/CSE-Archive/archive-api/issues/new?labels=enhancement) for that.
