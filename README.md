# shortify

A simple URL shortening service built with Flask.

## Usage

1. Build and run the app using Docker compose:
    ```
    docker compose up --build
    ```
2. The app will be available at http://localhost:8080.

## Tests

To run the unit tests:

```
docker compose run web python3 -m unittest discover -s tests -p "test_*.py"
```

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
