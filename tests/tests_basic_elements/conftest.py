import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from faker import Faker

fake = Faker('ru_RU')


@pytest.fixture(scope="function")
def browser():
    """Инициализация браузера с оптимальными настройками"""
    options = Options()
    # options.add_argument("--headless")  # Раскомментировать для CI/CD
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)  # Базовая подстраховка

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def wait(browser):
    """Фикстура для явных ожиданий"""
    return WebDriverWait(browser, 10)


@pytest.fixture(scope="function")
def base_url():
    return "https://lms.threadqa.ru/xpath-practice-hub/practice/basic-elements"


@pytest.fixture
def test_data():
    """Централизованное хранение тестовых данных"""
    return {
        "valid_name": fake.name(),
        "valid_email": fake.email(),
        "invalid_email": "not-an-email",
        "valid_password": "SuperSecret123!",
        "short_password": "123",
        "long_comment": "A" * 600,  # Для проверки maxlength=500
        "valid_comment": "Это тестовый комментарий.\nВторая строка.",
        "countries": ["США", "Германия", "Казахстан"]
    }