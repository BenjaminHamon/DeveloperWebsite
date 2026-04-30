""" Unit tests for application_factory """

from benjaminhamon_developer_website import application_factory


def test_create_application():
    application_factory.create_application(open_to_work = False, metrics_token = "metrics")
