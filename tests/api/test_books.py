import requests
import allure
import pytest
from jsonschema import validate, ValidationError
from config import Config

@allure.feature("Book Store API")
@pytest.mark.regression
def test_get_books():
    with allure.step("Preparar la URL de la solicitud"):
        url = f"{Config.BASE_URL}/BookStore/v1/Books"
        allure.attach(url, "Request URL", allure.attachment_type.TEXT)

    with allure.step("Enviar la solicitud GET a la API"):
        response = requests.get(url)
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
        allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)

    with allure.step("Validar el código de respuesta"):
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    with allure.step("Validar estructura JSON de la respuesta"):
        expected_schema = {
            "type": "object",
            "properties": {
                "books": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "isbn": {"type": "string"},
                            "title": {"type": "string"},
                            "subTitle": {"type": "string"},
                            "author": {"type": "string"},
                            "publish_date": {"type": "string", "format": "date-time"},
                            "publisher": {"type": "string"},
                            "pages": {"type": "integer"},
                            "description": {"type": "string"},
                            "website": {"type": "string", "format": "uri"},
                        },
                        "required": [
                            "isbn", "title", "author", "publish_date",
                            "publisher", "pages", "description", "website"
                        ]
                    }
                }
            },
            "required": ["books"]
        }

        try:
            validate(instance=response.json(), schema=expected_schema)
            allure.attach("JSON schema validation passed", name="Schema Validation", attachment_type=allure.attachment_type.TEXT)
        except ValidationError as e:
            allure.attach(str(e), name="Schema Validation Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"JSON schema validation failed: {e}")

    with allure.step("Validar valores específicos de la respuesta"):
        response_json = response.json()
        first_book = response_json['books'][0]

        assert first_book["title"] == "Git Pocket Guide", "Title mismatch"
        assert first_book["author"] == "Richard E. Silverman", "Author mismatch"
        assert first_book["isbn"] == "9781449325862", "ISBN mismatch"

        allure.attach(str(first_book), "First Book Details", allure.attachment_type.JSON)
