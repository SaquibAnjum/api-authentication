import sys
import os

# Add src to python path so api_security can be imported
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from api_security import app as flask_app

class VercelWSGIMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path_info = environ.get("PATH_INFO", "")
        # If Vercel prepends /api/index.py, /api/index, or /api, strip it
        for prefix in ("/api/index.py", "/api/index", "/api"):
            if path_info.startswith(prefix):
                path_info = path_info[len(prefix):]
                if not path_info.startswith("/"):
                    path_info = "/" + path_info
                environ["PATH_INFO"] = path_info
                break

        if not environ.get("PATH_INFO"):
            environ["PATH_INFO"] = "/"

        # If root / is accessed, return service info
        existing_rules = [r.rule for r in flask_app.url_map.iter_rules()]
        if environ["PATH_INFO"] == "/" and "/" not in existing_rules:
            status = "200 OK"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [b'{"status":"online","message":"API Authentication Service is running on Vercel!","endpoints":{"POST /login":"Authenticate user","GET /protected-route":"Access protected route with JWT Bearer token"}}\n']

        # If /login is accessed via browser GET, return helpful instructions
        if environ["PATH_INFO"] == "/login" and environ.get("REQUEST_METHOD", "") == "GET":
            status = "200 OK"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [b'{"message":"Send a POST request with JSON body to log in.","example_body":{"email":"saquib1312@gmail.com","password":"12345"}}\n']

        return self.wsgi_app(environ, start_response)

app = VercelWSGIMiddleware(flask_app.wsgi_app)
