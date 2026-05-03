# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Web Steps for BDD - Selenium step definitions for the Product Admin UI
"""
import logging
from behave import when, then  # pylint: disable=no-name-in-module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions

ID_PREFIX = "product_"


@when('I visit the "Home Page"')
def step_impl(context):
    """Navigate to the base URL"""
    context.driver.get(context.base_url)
    logging.info("Visiting: %s", context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the page title"""
    logging.info("Checking for title: %s", message)
    assert message in context.driver.title


@then('I should not see "{message}"')
def step_impl(context, message):
    """Ensure message is not on the page"""
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert message not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set a text field by label"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select an option from a dropdown"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(
        WebDriverWait(context.driver, context.wait_seconds).until(
            expected_conditions.presence_of_element_located((By.ID, element_id))
        )
    )
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Verify the selected option in a dropdown"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(
        WebDriverWait(context.driver, context.wait_seconds).until(
            expected_conditions.presence_of_element_located((By.ID, element_id))
        )
    )
    assert element.first_selected_option.text == text


@when('I press the "{button}" button')
def step_impl(context, button):
    """Click a button by its text label (data-ui attribute)"""
    button_id = button.lower() + "-btn"
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, button_id))
    )
    element.click()


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check the flash message"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), message
        )
    )
    assert found


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy a field value into context clipboard"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste the clipboard value into a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Verify a field is empty"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    assert element.get_attribute("value") == ""


@then('I should see "{text}" in the "{element_name}" field')
def step_impl(context, text, element_name):
    """Verify a field value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id), text
        )
    )
    assert found


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Verify a product name appears in the search results table"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"), name
        )
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Verify a product name does NOT appear in the search results table"""
    element = context.driver.find_element(By.ID, "search_results")
    assert name not in element.text


@when("I copy the first result id")
def step_impl(context):
    """Copy the id from the first row of the search results table"""
    results_table = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, "search_results"))
    )
    first_row = results_table.find_elements(By.TAG_NAME, "tr")[1]  # skip header
    first_cell = first_row.find_elements(By.TAG_NAME, "td")[0]
    context.clipboard = first_cell.text
    logging.info("Copied first result id: %s", context.clipboard)
