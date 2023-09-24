# CSE Archive RESTful API

This is the source code of our API backend implemented in Django framework, which is opened for educational purposes and contributions.

## Installation & Deploy

CSE Archive API project uses **pipenv** to set up its virtual environment. If you don't have it already, install it first

```bash
pip install pipenv
```

At the project root, use pipenv *install* command to install project dependencies listed in [Pipfile](https://github.com/CSE-Archive/RESTful-API/blob/main/Pipfile). After that, use its *shell* command to enable installed virtual environment

```bash
pipenv install
pipenv shell
```

To set the environment variables, copy the **.env.example** file to **.env** and set its variables according to the description below.

- DEBUG: This Boolean variable can be **True** or **False** depending on the program's environment. To run the program in the production environment, set the Boolean variable to False.
- SECRET_KEY: This is used to sign sensitive data, so it is important to generate a strong key. You can generate a key yourself or use command
    ```bash
    python manage.py generate_secret_key
    ```
- ALLOWED_HOSTS: Specifies the hosts that Django can accept requests from. Separate multiple hosts with commas, or use * to accept all requests.
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT: These variables specify the database used for the project.

Now that the environment is ready, you can run the following commands to start the API:

First we should apply database migrations

```bash
python manage.py migrate
```

To use the sample data, run this command

```bash
python manage.py loaddata fixtures/admin_interface_theme_uswds.json fixtures/courses.json fixtures/course_relations.json fixtures/chartnodes.json fixtures/professors.json fixtures/tas.json fixtures/classrooms.json fixtures/references.json fixtures/resources.json fixtures/recordings.json
```

Now you can start an instance of API on your local machine

```bash
python manage.py runserver 
```

By default, you can access the project at `localhost:8000`, the admin panel at `/admin` path, and the API documentation at `/swagger` path.

## Database Design

To generate a diagram of the models used in the API, first install Graphviz on your OS from [here](https://graphviz.org/download/). Then, run the following commands:

```bash
python manage.py graph_models -a -g --dot -o cse_archive_erd.dot
dot -Tpng cse_archive_erd.dot -o cse_archive_erd.png
```

## Contribution

We welcome contributions of any size to this project. To contribute, you can:

1. Fork the project on GitHub.
2. Make your changes in a new branch.
3. Create a pull request with a title that summarizes your changes and a description that explains your changes in more detail.

If you have any enhancement ideas but don't feel like to do it yourself, you can always [open a new issue](https://github.com/CSE-Archive/RESTful-API/issues/new?labels=enhancement) for that.
