import os
import jinja2
import webapp2
from models import Message


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_environment.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class GuestbookHandler(BaseHandler):
    def get(self):
        messages = Message.query().fetch()
        params = {"messages": messages}
        return self.render_template("guestbook.html", params=params)

    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        message = self.request.get("message")

        if "<script>" in message:
            return self.write("You will not hack me, no sir!")

        message_object = Message(author_name=name, email=email, message=message)
        message_object.put()

        return self.redirect_to("guestbook")

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/guestbook', GuestbookHandler, name="guestbook"),
webapp2.Route('/about', AboutHandler, name="about"),
], debug=True)