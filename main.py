#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



def convert(x):
    ''' convert x or y into integer '''
    if x == "":
        return ""
    try:
        x = float(x)
        return x
    except ValueError:  # user entered non-numeric value
        return "invalid input"


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        parametri = {"sporocilo": "To sem jaz Main Handler"}
        return self.render_template("index.html", params=parametri)


class RezultatHandler(BaseHandler):
    def post(self):
        x = self.request.get("vnos1")
        y = self.request.get("vnos2")
        operation = self.request.get("vnos3")
        x1 = convert(x)
        y1 = convert(y)
        if x1 == "invalid input" or y1 == "invalid input":
            rezultat = "Not valid input"
        elif operation == "+":
            rezultat = x1 + y1
        elif operation == "-":
            rezultat = x1 - y1
        elif operation == "*":
            rezultat = x1 * y1
        elif operation == "/":
            if y1 == 0:
                rezultat = "Y is zero. The devision can not be executed."
            else:
                rezultat = float(x1) / y1
        elif operation == "**":
            rezultat = x1 ** y1
        elif operation == "%":
            rezultat = x1 % y1
        else:
            rezultat = "Not working - choosen operation does not exist."

        parametri = {"rezultat": rezultat}
        return self.render_template("rezultat.html", params=parametri)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
], debug=True)
