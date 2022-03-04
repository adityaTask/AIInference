import logging
from traceback import print_stack
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
import utilities.custom_logger as cl


class SeleniumDriver():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType +
                          " not correct/supported")
        return False

    def get_element(self, locator="", locator_type="id"):
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.getByType(locatorType=locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info("Element with Locator: " + locator + " and Locator Type: " + locator_type + " found.")
        except:
            self.log.error("Element with Locator: " + locator + " and Locator Type: " + locator_type + " not found.")

        return element

    def element_click(self, locator="", locator_type="id", element=None):
        """
        Click on an element -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info("Clicked on element with locator: " + locator +
                          " locatorType: " + locator_type)
        except:
            self.log.info("Cannot click on the element with locator: " + locator +
                          " locatorType: " + locator_type)
            print_stack()

    def send_keys(self, data, locator="", locator_type="id", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + locator +
                          " locatorType: " + locator_type)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator +
                          " locatorType: " + locator_type)
            self.log.error("Exception Caught: {}".format(traceback.format_exc()))
            self.log.error("".join(traceback.format_stack()))

    def get_element_list(self, locator, locatorType="id"):
        """
        Get list of elements
        """
        locatorType = locatorType.lower()
        byType = self.getByType(locatorType)
        elements = self.driver.find_elements(byType, locator)
        if len(elements) > 0:
            self.log.info("Element list FOUND with locator: " + locator +
                          " and locatorType: " + locatorType)
        else:
            self.log.info("Element list NOT FOUND with locator: " + locator +
                              " and locatorType: " + locatorType)
        return elements

    def is_element_present(self, locator="", locatorType="id", element=None):
        """
        Check if element is present -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element_list = self.get_element_list(locator, locatorType)
            if len(element_list) > 0:
                self.log.info("Element present with locator: " + locator +
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def switchToFrame(self, id="", name="", index=None):
        """
        Switch to iframe using element locator inside iframe

        Parameters:
            1. Required:
                None
            2. Optional:
                1. id    - id of the iframe
                2. name  - name of the iframe
                3. index - index of the iframe
        Returns:
            None
        Exception:
            None
        """
        if id:
            self.driver.switch_to.frame(id)
        if name:
            self.driver.switch_to.frame(name)
        if index:
            self.log.info("Switch frame with index:")
            self.log.info(str(index))
            self.driver.switch_to.frame(index)

    def switchToDefaultContent(self):
        """
        Switch to default content

        Parameters:
            None
        Returns:
            None
        Exception:
            None
        """
        self.driver.switch_to.default_content()

    def element_presence_check(self, locator, byType):
        """
        Check if element is present
        """
        print("came to method element presence check")
        try:
            element = self.driver.find_element(byType, locator)
            print(locator)
            print(byType)
            print("Printing Element: "+ element)
            if element:
                self.log.info("Element present with locator: " + locator +
                              " locatorType: " + str(byType))
                return True
            else:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + str(byType))
                return False
        except:
            print_stack()
            self.log.info("Element not found")
            return False

    def refresh(self):
        self.driver.refresh()

    def clear(self,locator="", locator_type="id", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.clear()
            self.log.info("Cleared data on element with locator: " + locator +
                          " locatorType: " + locator_type)
        except:
            self.log.info("Cannot clear data on the element with locator: " + locator +
                          " locatorType: " + locator_type)
            self.log.error("Exception Caught: {}".format(traceback.format_exc()))
            self.log.error("".join(traceback.format_stack()))
