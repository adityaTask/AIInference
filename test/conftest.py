import pytest
from base.web_driver import WebDriver

@pytest.fixture(scope = "class")
def one_time_setup(request):
    print("setup")
    wd = WebDriver()
    driver = wd.web_driver_instance()
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    print("tear down")
    driver.quit()