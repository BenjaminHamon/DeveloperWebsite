import flask
from flask.typing import ResponseValue


class MainController:


    def redirect_for_locale_en(self) -> ResponseValue:
        return flask.redirect(flask.url_for("main_controller.home", locale = "en"))


    def redirect_for_locale_fr(self) -> ResponseValue:
        return flask.redirect(flask.url_for("main_controller.home", locale = "fr"))


    def home(self) -> ResponseValue:
        return flask.render_template(flask.session["locale"] + "/" + "home.html")


    def education(self) -> ResponseValue:
        return flask.render_template(flask.session["locale"] + "/" + "education.html")


    def skills(self) -> ResponseValue:
        return flask.render_template(flask.session["locale"] + "/" + "skills.html")


    def projects(self) -> ResponseValue:
        return flask.render_template(flask.session["locale"] + "/" + "projects.html")


    def work_experience(self) -> ResponseValue:
        return flask.render_template(flask.session["locale"] + "/" + "work_experience.html")


    def contact(self) -> ResponseValue:
        return flask.render_template(flask.session["locale"] + "/" + "contact.html")
