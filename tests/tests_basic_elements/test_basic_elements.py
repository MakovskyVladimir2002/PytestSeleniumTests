import pytest
import allure
from pages.basic_elements_page import BasicElementsPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@allure.feature("Форма базовых элементов")
class TestBasicElementsForm:

    @pytest.fixture(autouse=True)
    def setup(self, browser, wait, base_url):
        self.page = BasicElementsPage(browser, wait)
        self.page.open(base_url)

    @allure.story("Текстовое поле Имя")
    @pytest.mark.smoke
    def test_username_input_valid(self, test_data):
        with allure.step("Вводим валидное имя"):
            self.page.enter_username(test_data["valid_name"])

        with allure.step("Проверяем, что значение сохранилось"):
            assert self.page.get_attribute(self.page.USERNAME_INPUT, "value") == test_data["valid_name"]
            assert self.page.get_attribute(self.page.USERNAME_INPUT, "placeholder") == "Введите ваше имя"

    @allure.story("Поле Email")
    @pytest.mark.smoke
    @pytest.mark.parametrize("email_input, is_valid", [
        ("user@example.com", True),
        ("invalid-email-without-domain", False),
        ("", False)  # Проверка required
    ])
    def test_email_field_validation(self, email_input, is_valid, test_data):
        with allure.step(f"Вводим email: {email_input}"):
            self.page.enter_email(email_input)

        with allure.step("Проверяем атрибуты поля"):
            assert self.page.get_attribute(self.page.EMAIL_INPUT, "type") == "email"
            assert self.page.get_attribute(self.page.EMAIL_INPUT, "required") == "true"

        if is_valid:
            assert self.page.get_attribute(self.page.EMAIL_INPUT, "value") == email_input

    @allure.story("Поле Пароль")
    @pytest.mark.smoke
    def test_password_field_masking_and_length(self, test_data):
        with allure.step("Вводим короткий пароль (нарушение minlength)"):
            self.page.enter_password(test_data["short_password"])

        with allure.step("Проверяем атрибуты безопасности"):
            assert self.page.get_attribute(self.page.PASSWORD_INPUT, "type") == "password"
            assert self.page.get_attribute(self.page.PASSWORD_INPUT, "minlength") == "8"
            # Значение введено, но HTML5 валидация не даст отправить форму (проверка атрибута)
            assert self.page.get_attribute(self.page.PASSWORD_INPUT, "value") == test_data["short_password"]

    @allure.story("Текстовая область (Textarea)")
    @pytest.mark.smoke
    def test_textarea_maxlength(self, test_data):
        with allure.step("Вводим текст, превышающий maxlength"):
            self.page.enter_comment(test_data["long_comment"])

        with allure.step("Проверяем, что браузер обрезал или ограничил ввод до 500 символов"):
            actual_value = self.page.get_attribute(self.page.COMMENT_TEXTAREA, "value")
            assert len(actual_value) <= 500, f"Длина текста {len(actual_value)} превышает лимит 500"
            assert self.page.get_attribute(self.page.COMMENT_TEXTAREA, "maxlength") == "500"

    @allure.story("Выпадающий список (Select)")
    @pytest.mark.smoke
    def test_country_dropdown_selection(self, test_data):
        with allure.step("Выбираем первую страну"):
            self.page.select_country(test_data["countries"][0])

        with allure.step("Проверяем, что страна отобразилась в кнопке"):
            dropdown_text = self.page.find_element(self.page.COUNTRY_DROPDOWN_BTN).text
            assert test_data["countries"][0] in dropdown_text

        with allure.step("Перевыбираем вторую страну"):
            self.page.select_country(test_data["countries"][1])
            dropdown_text = self.page.find_element(self.page.COUNTRY_DROPDOWN_BTN).text
            assert test_data["countries"][1] in dropdown_text

    @allure.story("Чекбоксы и Радиокнопки")
    @pytest.mark.smoke
    def test_checkbox_and_radio_interaction(self):
        with allure.step("Кликаем чекбокс соглашений"):
            assert not self.page.is_selected(self.page.TERMS_CHECKBOX)
            self.page.toggle_terms_checkbox()
            assert self.page.is_selected(self.page.TERMS_CHECKBOX)

        with allure.step("Выбираем радиокнопку 'Да'"):
            self.page.select_newsletter_radio("yes")
            assert self.page.is_selected(self.page.RADIO_NEWSLETTER_YES)
            assert not self.page.is_selected(self.page.RADIO_NEWSLETTER_NO)

    @allure.story("Интерактивные элементы (Alert)")
    @pytest.mark.smoke
    def test_browser_alert_handling(self):
        with allure.step("Нажимаем кнопку вызова алерта"):
            alert_text = self.page.trigger_alert()

        with allure.step("Проверяем текст алерта"):
            assert "уведомление" in alert_text.lower() or "alert" in alert_text.lower()

    @allure.story("Ссылки")
    @pytest.mark.regression
    def test_external_link_attributes(self):
        with allure.step("Проверяем атрибуты внешней ссылки"):
            href = self.page.get_attribute(self.page.LINK_EXTERNAL, "href")
            target = self.page.get_attribute(self.page.LINK_EXTERNAL, "target")

            assert "example.com" in href
            assert target == "_blank"