import allure


@staticmethod
def take_screenshot(driver, name="Screenshot"):
    screenshot_png = driver.get_screenshot_as_png()
    allure.attach(
        screenshot_png,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
