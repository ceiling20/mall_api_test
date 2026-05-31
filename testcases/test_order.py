import allure
import pytest
from utils.logger import get_logger
logger = get_logger(__name__)
@allure.feature("订单管理")
@allure.story("查询订单")
@allure.severity(allure.severity_level.NORMAL)
def test_get_order(admin_base_url,auth_client):
    with allure.step("发送get请求查询订单，验证返回码为预期值"):
        get_response = auth_client.get(f"{admin_base_url}/order/15")
        data = get_response.json()
        assert get_response.status_code == 200
        assert "id" in data["data"]
        logger.info("测试完成")
        logger.info(f"{data['data']}")
@allure.feature("订单管理")
@allure.story("查询订单列表")
@allure.severity(allure.severity_level.NORMAL)
def test_get_order_list(auth_client,admin_base_url):
    with allure.step("发送get请求查询订单列表，验证返回码为预期值"):
        GL_response = auth_client.get(f"{admin_base_url}/order/list",params={"pageNum":4,"pageSize":5})
    data = GL_response.json()
    assert GL_response.status_code == 200
    assert "list" in data["data"]
    logger.info(f"{data['data']}")


def test_portal_login(portal_token):
    """简单的登录测试，用于验证 portal_auth_token fixture 是否工作"""
    assert portal_token is not None
    print(f"\nPortal Token 获取成功: {portal_token}")