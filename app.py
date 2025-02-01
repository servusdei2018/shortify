import argparse
from flask import Flask, request, redirect, render_template
from waitress import serve
from werkzeug.exceptions import NotFound
import random
import string

app = Flask(__name__)
url_map = {}


def generate_short_code(length=6):
    """
    Generate a random short code to be used as a shortened URL.

    Args:
        length (int): The length of the generated short code. Default is 6.

    Returns:
        str: A randomly generated string composed of uppercase and lowercase letters and digits.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@app.route("/")
def home():
    """
    Render the homepage of the URL shortening service.

    Returns:
        str: The rendered HTML template for the homepage.
    """
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten_url():
    """
    Handle the request to shorten a given URL.

    The original URL is provided via a POST form. If the URL is already
    shortened, it returns the existing short URL. Otherwise, it generates a
    new short URL.

    Returns:
        str: The full short URL (host + short code) if successful.
        Response: HTTP error if the URL is missing or invalid.
    """
    original_url = request.form.get("url")
    if not original_url:
        return "Error: URL is required", 400

    for short_code, url in url_map.items():
        if url == original_url:
            return request.host_url + short_code

    short_code = generate_short_code()
    while short_code in url_map:
        short_code = generate_short_code()

    url_map[short_code] = original_url
    return request.host_url + short_code


@app.route("/<short_code>")
def redirect_to_url(short_code):
    """
    Redirect the user to the original URL based on the short code.

    Args:
        short_code (str): The shortened code that represents a specific URL.

    Returns:
        Response: A redirect to the original URL if the short code exists.
        Exception: Raises a NotFound error if the short code does not exist in the map.
    """
    original_url = url_map.get(short_code)
    if not original_url:
        raise NotFound("Short URL not found")
    return redirect(original_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true", help="Run the server in debug mode"
    )
    args = parser.parse_args()

    if args.debug:
        app.run(debug=True)
    else:
        serve(app, host="0.0.0.0")
