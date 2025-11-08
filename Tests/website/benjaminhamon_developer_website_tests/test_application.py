import itertools
import sys

import pytest
import pytest_asyncio
import requests

from .website_runner import WebsiteRunner


@pytest_asyncio.fixture(name = "website", scope = "module", loop_scope = "module")
async def website_fixture():
    python_executable = sys.executable
    application_module = "benjaminhamon_developer_website.run"
    address = "localhost"
    port = 4999

    command = [ python_executable, "-m", application_module, "--address", address, "--port", str(port) ]

    async with WebsiteRunner(command, address, port) as website:
        yield website.get_url()


_locale_collection = [ "en", "fr" ]

_route_collection = [
    "home",
    "contact",
    "education",
    "projects",
    "skills",
    "work_experience",
]

_route_collection_with_locale = itertools.product(_locale_collection, _route_collection)


@pytest.mark.parametrize("locale,route_identifier", _route_collection_with_locale)
def test_web_page(website, locale, route_identifier):
    route_as_path = "/" + locale + ("/" + route_identifier if route_identifier != "home" else "")
    response = requests.request("GET", website + route_as_path, timeout = 1)

    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "text/html"
    assert response.text != ""


def test_metrics_with_authorization(website):
    response = requests.request("GET", website + "/metrics", headers = { "Authorization": "Bearer metrics" }, timeout = 1)

    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text != ""


def test_metrics_with_bad_authorization(website):
    response = requests.request("GET", website + "/metrics", headers = { "Authorization": "Bearer wrong" }, timeout = 1)

    assert response.status_code == 403
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text == ""


def test_metrics_without_authorization(website):
    response = requests.request("GET", website + "/metrics", timeout = 1)

    assert response.status_code == 401
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text == ""
