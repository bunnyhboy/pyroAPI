import re
import os

class Response:
    def __init__(self, body, status="200 OK", headers=None):
        self.body = body.encode() if isinstance(body, str) else body
        self.status = status
        self.headers = headers or [('Content-Type', 'text/html')]

    def __iter__(self):
        yield self.body

class Bumbo:
    def __init__(self):
        self.routes = []
        self.middlewares = []  # Middleware list

    def add_middleware(self, middleware_func):
        self.middlewares.append(middleware_func)

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD'].lower()
        handler = None
        kwargs = {}

        # Run middleware (before route handling)
        for middleware in self.middlewares:
            response = middleware(environ)
            if response:  # Short-circuit if middleware returns a response
                start_response(response.status, response.headers)
                return response

        for pattern, h in self.routes:
            match = pattern.match(path)
            if match:
                handler = h
                kwargs = match.groups()
                break

        if handler is None:
            res = Response("Not Found", status="404 Not Found", headers=[('Content-Type', 'text/plain')])
        else:
            if callable(handler):
                result = handler(*kwargs)
            else:
                handler_instance = handler()
                if not hasattr(handler_instance, method):
                    result = Response("Method Not Allowed", status="405 Method Not Allowed", headers=[('Content-Type', 'text/plain')])
                else:
                    result = getattr(handler_instance, method)(*kwargs)

            res = result if isinstance(result, Response) else Response(result)

        start_response(res.status, res.headers)
        return res

    def route(self, path):
        pattern_str = re.sub(r'<(\w+)>', r'([^/]+)', path)
        pattern = re.compile(f'^{pattern_str}$')

        def wrapper(handler):
            self.routes.append((pattern, handler))
            return handler
        return wrapper

def render_template(filename, **context):
    path = os.path.join("templates", filename)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))

    return content
