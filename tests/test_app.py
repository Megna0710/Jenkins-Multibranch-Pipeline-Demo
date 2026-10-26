import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

from app.main import Handler


class ApplicationEndpointTests(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_health_endpoint_returns_healthy_status(self):
        with urllib.request.urlopen(f"{self.base_url}/health") as response:
            payload = json.loads(response.read().decode())
            self.assertEqual(response.status, 200)
            self.assertEqual(payload["status"], "healthy")
            self.assertEqual(payload["service"], "jenkins-multibranch-demo")

    def test_unknown_path_returns_404(self):
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(f"{self.base_url}/missing")
        self.assertEqual(context.exception.code, 404)
        self.assertEqual(json.loads(context.exception.read().decode())["error"], "not_found")


if __name__ == "__main__":
    unittest.main()
