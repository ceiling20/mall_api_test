import pytest
import requests
from utils.config import BASE_URL_ADMIN, BASE_URL_PORTAL
from utils.db_helper import get_mysql_conn


@pytest.fixture(scope="module")
def db_conn():
    conn = get_mysql_conn()
    conn.autocommit(True)
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def admin_base_url():
    return BASE_URL_ADMIN


@pytest.fixture(scope="session")
def portal_base_url():
    return BASE_URL_PORTAL





@pytest.fixture(scope="session")
def unauth_client():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    yield session
    session.close()


# ==================== admin token / client ====================

@pytest.fixture(scope="session")
def auth_token(admin_base_url, unauth_client):
    auth_url = f"{admin_base_url}/admin/login"
    payload = {"username": "admin", "password": "macro123"}
    response = unauth_client.post(auth_url, json=payload)
    print("\n===== 调试信息 =====")
    print("状态码:", response.status_code)
    print("响应内容 text:", response.text)
    print("响应内容 json():", response.json())
    print("==================")
    assert response.status_code == 200
    return response.json()["data"]["token"]


@pytest.fixture(scope="function")
def auth_client(auth_token):
    """admin 模块的认证客户端"""
    session = requests.session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    })
    yield session
    session.close()


# ==================== portal token / client ====================

@pytest.fixture(scope="session")
def portal_token(portal_base_url, unauth_client):
    """portal 模块的会员 token，需要先注册一个测试会员"""
    auth_url = f"{portal_base_url}/sso/login"
    params={"username": "admin", "password": "macro123"}
    response = unauth_client.post(auth_url,params=params)
    print("\n===== Portal 登录调试 =====")
    print("状态码:", response.status_code)
    print("响应内容 text:", response.text)
    print("==========================")
    assert response.status_code == 200
    return response.json()["data"]["token"]


@pytest.fixture(scope="function")
def portal_client(portal_token):
    """portal 模块的认证客户端"""
    session = requests.session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {portal_token}"
    })
    yield session
    session.close()


def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
