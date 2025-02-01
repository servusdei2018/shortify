import unittest
from urllib.parse import urlparse
from app import app, url_map, generate_short_code


class TestURLShortener(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        url_map.clear()

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"URL Shortener", response.data)

    def test_shorten_url_success(self):
        url = "https://example.com"
        response = self.app.post("/shorten", data={"url": url})
        self.assertEqual(response.status_code, 200)
        shortened_url = response.data.decode()
        parsed_url = urlparse(shortened_url)

        # Verify response is a valid URL with the host
        self.assertTrue(parsed_url.netloc)
        self.assertTrue(parsed_url.path.strip("/"))

        # Verify the mapping was created
        short_code = parsed_url.path.strip("/")
        self.assertIn(short_code, url_map)
        self.assertEqual(url_map[short_code], url)

    def test_shorten_url_missing_input(self):
        response = self.app.post("/shorten", data={"url": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Error: URL is required", response.data)

    def test_redirect_to_original_url(self):
        url = "https://example.org"
        short_code = generate_short_code()
        url_map[short_code] = url

        response = self.app.get(f"/{short_code}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, url)

    def test_redirect_invalid_short_code(self):
        response = self.app.get("/nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Short URL not found", response.data)


if __name__ == "__main__":
    unittest.main()
