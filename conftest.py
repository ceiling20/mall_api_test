import pytest
import requests
from utils.config import BASE_URL
@pytest.fixture
def base_url():
    return BASE_URL
@pytest.fixture
def api_client():
    session = requests.session()
    session.headers.update({
        "Content-Type" : "application/json",
        "Accept" : "application/json"
    })
    yield session
    session.close()