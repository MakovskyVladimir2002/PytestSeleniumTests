from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class BasePage:
    def __init__(self, browser, wait: WebDriverWait):
        self.browser = browser
        self.wait = wait

    def open(self, url: str):
        self.browser.get(url)

    def find_element(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_element_located(locator),
                               message=f"Элемент не найден: {locator}")

    def wait_for_visibility(self, locator, timeout=10):
        return self.wait.until(EC.visibility_of_element_located(locator),
                               message=f"Элемент не виден: {locator}")

    def wait_for_clickable(self, locator, timeout=10):
        return self.wait.until(EC.element_to_be_clickable(locator),
                               message=f"Элемент не кликабелен: {locator}")

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        # 1. Принудительно прокручиваем элемент в центр viewport,
        # чтобы избежать перекрытия sticky-хедером или футером
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            # 2. Пробуем стандартный клик
            element.click()
        except ElementClickInterceptedException:
            # 3. Fallback: если клик всё равно перехвачен (оверлей, анимация), используем JS
            self.browser.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text: str):
        element = self.wait_for_visibility(locator)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.clear()
        element.send_keys(text)

    def get_attribute(self, locator, attr_name: str) -> str:
        return self.find_element(locator).get_attribute(attr_name)

    def is_selected(self, locator) -> bool:
        return self.find_element(locator).is_selected()

    def switch_to_alert_and_accept(self):
        alert = self.wait.until(EC.alert_is_present(), message="Алерт не появился в течение таймаута")
        alert_text = alert.text
        alert.accept()
        return alert_text