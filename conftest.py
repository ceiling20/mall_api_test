import pytest
import requests
from utils.config import BASE_URL


@pytest.fixture(scope="session")
def unauth_client():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    yield session
    session.close()


@pytest.fixture(scope="session")
def auth_token(base_url, unauth_client):
    auth_url = f"{base_url}/admin/login"
    payload = {"username": "admin", "password": "macro123"}
    response = unauth_client.post(auth_url, json=payload)
    print("\n===== 调试信息 =====")
    print("状态码:", response.status_code)
    print("响应内容 text:", response.text)  # 查看原始内容
    print("响应内容 json():", response.json())  # 查看解析后的对象
    print("==================")
    assert response.status_code == 200
    return response.json()["data"]["token"]


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="function")
def auth_client(auth_token):
    session = requests.session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    })
    yield session
    session.close()


def pytest_collection_modifyitems(items):
    for item in items:
        # 把 ids 里的 unicode 转义还原成中文
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
