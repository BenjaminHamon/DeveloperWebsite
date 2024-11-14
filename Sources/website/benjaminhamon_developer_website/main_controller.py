import flask


class MainController:


    def home(self) -> str:
        return flask.render_template(flask.session["locale"] + "/" + "home.html")


    def education(self) -> str:
        return flask.render_template(flask.session["locale"] + "/" + "education.html")


    def skills(self) -> str:
        return flask.render_template(flask.session["locale"] + "/" + "skills.html")


    def projects(self) -> str:
        return flask.render_template(flask.session["locale"] + "/" + "projects.html")


    def work_experience(self) -> str:
        return flask.render_template(flask.session["locale"] + "/" + "work_experience.html")


    def contact(self) -> str:
        return flask.render_template(flask.session["locale"] + "/" + "contact.html")
