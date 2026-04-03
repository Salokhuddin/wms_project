from django.test import TestCase


class SmokeTest(TestCase):
    def test_server_responds(self):
        """Verify Django is configured correctly and can handle a request."""
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 404])