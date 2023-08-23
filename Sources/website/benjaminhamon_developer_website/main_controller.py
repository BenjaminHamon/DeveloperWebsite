import flask


class MainController:


    def home(self) -> str:
        return flask.render_template("home.html", title = "Home")


    def education(self) -> str:
        return flask.render_template("education.html", title = "Education")


    def skills(self) -> str:
        return flask.render_template("skills.html", title = "Skills")


    def projects(self) -> str:
        return flask.render_template("projects.html", title = "Projects")


    def work_experience(self) -> str:
        return flask.render_template("work_experience.html", title = "Work Experience")


    def contact(self) -> str:
        return flask.render_template("contact.html", title = "Contact")
