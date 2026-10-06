from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BasicElementsPage(BasePage):
    # --- Локаторы ---
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-testid='username-field']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-testid='email-field']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='password-field']")
    COMMENT_TEXTAREA = (By.CSS_SELECTOR, "[data-testid='comment-field']")

    # Выпадающий список (Radix UI Combobox)
    COUNTRY_DROPDOWN_BTN = (By.CSS_SELECTOR, "[data-testid='country-dropdown']")

    TERMS_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='terms-agreement']")
    RADIO_NEWSLETTER_YES = (By.CSS_SELECTOR, "[data-testid='newsletter-yes']")
    RADIO_NEWSLETTER_NO = (By.CSS_SELECTOR, "[data-testid='newsletter-no']")

    BTN_SHOW_ALERT = (By.CSS_SELECTOR, "[data-testid='show-alert-button']")
    BTN_PRIMARY = (By.CSS_SELECTOR, "[data-testid='primary-button']")
    LINK_EXTERNAL = (By.CSS_SELECTOR, "[data-testid='external-link']")

    # --- Бизнес-методы ---
    def enter_username(self, text: str):
        self.send_keys(self.USERNAME_INPUT, text)

    def enter_email(self, text: str):
        self.send_keys(self.EMAIL_INPUT, text)

    def enter_password(self, text: str):
        self.send_keys(self.PASSWORD_INPUT, text)

    def enter_comment(self, text: str):
        self.send_keys(self.COMMENT_TEXTAREA, text)

    def select_country(self, country_name: str):
        """Умная работа с кастомным выпадающим списком (Radix UI Portal)"""
        self.click(self.COUNTRY_DROPDOWN_BTN)
        # Ищем опцию по role="option" и тексту.
        # Современные UI-библиотеки рендерят дропдауны в отдельном портале в конце <body>
        option_locator = (By.XPATH, f"//*[@role='option' and contains(text(), '{country_name}')]")
        self.click(option_locator)

    def toggle_terms_checkbox(self):
        self.click(self.TERMS_CHECKBOX)

    def select_newsletter_radio(self, value: str):
        if value == "yes":
            self.click(self.RADIO_NEWSLETTER_YES)
        else:
            self.click(self.RADIO_NEWSLETTER_NO)

    def trigger_alert(self):
        self.click(self.BTN_SHOW_ALERT)
        return self.switch_to_alert_and_accept()