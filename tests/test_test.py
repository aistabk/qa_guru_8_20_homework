import json
import logging
import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have

url_api = 'https://demowebshop.tricentis.com'
url_web = 'https://demowebshop.tricentis.com'


def api_request(url, **kwargs):
    result = requests.post(url=url_api + url, **kwargs)

    allure.attach(body=result.request.url, name="Request url",
                  attachment_type=AttachmentType.TEXT)
    allure.attach(body=json.dumps(result.request.body, indent=4, ensure_ascii=True), name="Request body",
                  attachment_type=AttachmentType.JSON, extension="json")

    allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + result.request.url)
    if result.request.body:
        logging.info("INFO Request body: " + result.request.body)
        logging.info("Request headers: " + str(result.request.headers))
        logging.info("Response code " + str(result.status_code))
        logging.info("Response: " + result.text)
    return result


def test_adding_to_cart_one_item(browser_setup):
    response = api_request('/addproducttocart/catalog/31/1/1')
    cookie = response.cookies.get("Nop.customer")

    browser.open('/')

    browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    browser.open('/cart')

    browser.all('.cart-item-row').should(have.size(1))
    browser.all('.product-name').element_by(have.text('Laptop'))


def test_adding_to_chart_several_items(browser_setup):
    response = api_request('/addproducttocart/catalog/65/1/1')
    cookie = response.cookies.get("Nop.customer")
    api_request('/addproducttocart/catalog/14/1/1', cookies={"Nop.customer": cookie})

    browser.open('/')

    browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    browser.open('/cart')

    browser.all('.cart-item-row').should(have.size(2))


def test_price(browser_setup):
    response = api_request('/addproducttocart/details/53/1',
                           data={"addtocart_53.EnteredQuantity": 7},
                           )
    cookie = response.cookies.get("Nop.customer")

    browser.open('/')

    browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    browser.open('/cart')

    browser.all('.product-subtotal').element_by(have.text('7.00'))
