import pytest
from selene import browser


@pytest.fixture(scope="function")
def browser_setup():
    browser.config.base_url = 'https://demowebshop.tricentis.com'

    yield

    browser.quit()
