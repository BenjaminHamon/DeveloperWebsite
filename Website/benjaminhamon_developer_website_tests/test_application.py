# cspell:language en fr

import pytest
from playwright.async_api import Page
from playwright.async_api import expect

from benjaminhamon_developer_website_tests.website_runner import WebsiteRunner


@pytest.mark.asyncio(loop_scope = "session")
async def test_home_page_with_gunicorn(website_using_gunicorn: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_gunicorn.get_url() + "/")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Home - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_home_page_with_locale_en(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/en")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Home - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_home_page_with_locale_fr(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/fr")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Accueil - Site développeur de Benjamin Hamon")


@pytest.mark.asyncio(loop_scope = "session")
async def test_education_page_with_locale_en(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/en/education")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Education - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_education_page_with_locale_fr(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/fr/education")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Formation - Site développeur de Benjamin Hamon")


@pytest.mark.asyncio(loop_scope = "session")
async def test_work_experience_page_with_locale_en(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/en/work_experience")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Work experience - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_work_experience_page_with_locale_fr(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/fr/work_experience")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Expérience professionnelle - Site développeur de Benjamin Hamon")


@pytest.mark.asyncio(loop_scope = "session")
async def test_projects_page_with_locale_en(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/en/projects")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Projects - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_projects_page_with_locale_fr(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/fr/projects")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Projets - Site développeur de Benjamin Hamon")


@pytest.mark.asyncio(loop_scope = "session")
async def test_skills_page_with_locale_en(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/en/skills")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Skills - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_skills_page_with_locale_fr(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/fr/skills")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Compétences - Site développeur de Benjamin Hamon")


@pytest.mark.asyncio(loop_scope = "session")
async def test_contact_page_with_locale_en(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/en/contact")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Contact - Benjamin Hamon's developer website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_contact_page_with_locale_fr(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/fr/contact")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Contact - Site développeur de Benjamin Hamon")
