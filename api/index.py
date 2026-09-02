import sys
import os

# Add src to python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from api_security import app as flask_app

class VercelWSGIMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # Determine actual requested path from WSGI/Vercel headers
        # Vercel sets HTTP_X_FORWARDED_URI or RAW_URI or REQUEST_URI
        original_path = (
            environ.get("HTTP_X_FORWARDED_URI")
            or environ.get("RAW_URI")
            or environ.get("REQUEST_URI")
            or environ.get("PATH_INFO")
            or "/"
        ).split("?")[0]

        # Strip any Vercel internal prefixes
        for prefix in ("/api/index.py", "/api/index", "/api"):
            if original_path.startswith(prefix) and len(original_path) > len(prefix):
                original_path = original_path[len(prefix):]
                if not original_path.startswith("/"):
                    original_path = "/" + original_path
                break

        if not original_path:
            original_path = "/"

        environ["PATH_INFO"] = original_path

        # If root / is accessed, return a status response
        existing_rules = [r.rule for r in flask_app.url_map.iter_rules()]
        if original_path == "/" and "/" not in existing_rules:
            status = "200 OK"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [b'{"status":"online","message":"API Authentication Service is running on Vercel!","endpoints":{"POST /login":"Authenticate user","GET /protected-route":"Access protected route with JWT Bearer token"}}\n']

        # If /login is accessed via browser GET, return helpful instructions
        if original_path == "/login" and environ.get("REQUEST_METHOD", "") == "GET":
            status = "200 OK"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [b'{"message":"Send a POST request with JSON body to log in.","example_body":{"email":"saquib1312@gmail.com","password":"12345"}}\n']

        return self.wsgi_app(environ, start_response)

app = VercelWSGIMiddleware(flask_app.wsgi_app)
