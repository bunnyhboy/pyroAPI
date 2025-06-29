from api import Bumbo, Response, render_template

app = Bumbo()

def block_forbidden_path(environ):
    if environ['PATH_INFO'] == '/forbidden':
        return Response("Forbidden!", status="403 Forbidden", headers=[('Content-Type', 'text/plain')])
    return None 

app.add_middleware(block_forbidden_path)

@app.route("/greet/<name>/<location>")
def greet(name, location):
    html = render_template("greet.html", name=name, location=location)
    return Response(html)
