import flask
import werkzeug


class MainController:


    def home_default(self) -> werkzeug.Response:
        return flask.redirect(flask.url_for("main_controller.home", locale = flask.current_app.config["LOCALE_DEFAULT"]))


    def home(self, locale: str) -> str:
        return flask.render_template(locale + "/" + "home.html")


    def education(self, locale: str) -> str:
        return flask.render_template(locale + "/" + "education.html")


    def skills(self, locale: str) -> str:
        return flask.render_template(locale + "/" + "skills.html")


    def projects(self, locale: str) -> str:
        return flask.render_template(locale + "/" + "projects.html")


    def work_experience(self, locale: str) -> str:
        return flask.render_template(locale + "/" + "work_experience.html")


    def contact(self, locale: str) -> str:
        return flask.render_template(locale + "/" + "contact.html")
