import pytest
import requests
@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"
def test_get_post_invalid_id(base_url):
    response = requests.get(f"{base_url}/posts/999999")
    print(f"实际返回的状态码:{response.status_code}")
    assert response.status_code == 404
def test_create_post_empty_title(base_url):
    payload = {
        "title" : "",
        "body" : "内容",
        "userid" : "1"
    }
    response = requests.post(f"{base_url}/posts/1",json = payload)
    print(f"实际返回的状态码:{response.status_code}")
    assert response.status_code == 404
def test_create_post_missing_field(base_url):
    payload = {
        'title' : "标题"
    }
    response = requests.post(f"{base_url}/posts/1",json=payload)
    print(f"实际返回的状态码:{response.status_code}")
    assert response.status_code == 404