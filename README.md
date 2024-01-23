# Word Puzzle Project

This project is designed to provide the functionality of generating sequences of words between two given words wherein every subsequent word is one character different.

## Getting Started

This project has been setup using python version `3.10.10`. Poetry is being used for dependency management.
Necessary requirements can be found in `pyproject.toml` file.

To get started with the Word Puzzle project, follow these steps:

1. **Project Setup:**

   - Go to wordpuzzle directory

      ```bash
      cd wordpuzzle
      ```

   - **Recommendation**: Set poetry virtual env path to project directory for clearer management

      ```bash
      poetry config virtualenvs.in-project true
      ```

   - Install project dependencies using [Poetry](https://python-poetry.org/).

      ```bash
      poetry install
      ```

   - Activate virtual env

      ```bash
      poetry shell
      ```

2. **Database Migration:**
   - Apply database migrations.

     ```bash
     poetry run python manage.py migrate
     ```

3. **Run the Server:**
   - Start the development server.

     ```bash
     poetry run python manage.py runserver
     ```

4. **API Interaction:**
   - Once the server is running, send a `GET` request to the endpoint eg:
   [wordpuzzle?startWord=oyster&endWord=mussel](http://127.0.0.1:8000/api/wordpuzzle?startWord=oyster&endWord=mussel)

    *More details (including request / response data types) can be found in [API Docs](#api-docs)*

5. **Run Tests:**
   - Execute the test suite to ensure everything is working. The tests are written for the core components inline with Django best practices

     ```bash
     poetry run python manage.py test
     ```

   - In order to generate coverage, run (currently at 💯).

     ```bash
     coverage run --source='.' manage.py test && coverage report
     ```

## Project Details

### Core Components

- **`api` Package:**
  - Contains models, views, and other components related to the API.

- **`data` Folder:**
  - Contains data files `words.txt`.

- **`migrations` Folder:**
  - Stores database migration files.

- **`tests` Folder:**
  - Includes test files for middleware, views, and models.

### Word Puzzle Logic

- **Word Loader:**
  - `api/word_loader.py` provides functionality to load words from data file.

- **Middleware:**
  - `api/middleware.py` implements middleware logic for handing request/response.

- **Views:**
  - `api/views.py` contains views for word puzzle functionality.

## API Docs

- The project also contains necessary setup to generate and publish Swagger/OpenAPI specification. Once the server is running, it can be found on <http://127.0.0.1:8000/api/swagger/>. It contains details of request and response data types and can be used to test the `GET` endpoint.

## Contributing

Feel free to contribute to the Word Puzzle project! If you have suggestions, feature requests, or find issues, please submit them through the [GitHub repository](https://github.com/anuragverma65/wordpuzzle).

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
