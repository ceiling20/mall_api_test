import allure
import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("订单管理")
@allure.story("查询订单")
@allure.severity(allure.severity_level.NORMAL)
def test_get_order(admin_base_url, auth_client):
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
def test_get_order_list(auth_client, admin_base_url):
    with allure.step("发送get请求查询订单列表，验证返回码为预期值"):
        GL_response = auth_client.get(f"{admin_base_url}/order/list", params={"pageNum": 4, "pageSize": 5})
        data = GL_response.json()
        assert GL_response.status_code == 200
        assert "list" in data["data"]
        logger.info(f"{data['data']}")


def test_portal_login(portal_token):
    """简单的登录测试，用于验证 portal_auth_token fixture 是否工作"""
    assert portal_token is not None
    print(f"\nPortal Token 获取成功: {portal_token}")


@allure.feature("订单管理")
@allure.story("创建订单")
@allure.severity(allure.severity_level.NORMAL)
def test_create_order(portal_client, portal_base_url):
    with allure.step("发送post请求把商品加入购物车，验证返回值为预期"):
        logger.info("开始测试")
        SKUID = 110
        cart_payload = {
            "productId": 26,
            "productSkuId": SKUID,
            "quantity": 1
        }
        cart_response = portal_client.post(f"{portal_base_url}/cart/add", json=cart_payload)
        cart_data = cart_response.json()
        assert cart_response.status_code == 200
        assert cart_data["code"] == 200
        logger.info(f"创建完成：{cart_response.text}")
    with allure.step("发送get请求查询购物车列表，用skuId匹配购物车id，获取购物车id"):
        list_response = portal_client.get(f"{portal_base_url}/cart/list")
        assert list_response.status_code == 200
        list_data = list_response.json()["data"]
        cart_id = next((cart["id"] for cart in list_data if SKUID == cart["productSkuId"]), None)
        assert cart_id is not None, f"未找到skuId：{SKUID}的购物车单"
    logger.info(f"购物车id为{cart_id}")
    with allure.step("发送post请求添加收货地址，验证返回码为预期"):
        detailAddress = "柳东街道"
        address_payload = {
            "name": "ceiling",
            "phoneNumber": "15982406733",
            "province": "广西省",
            "city": "柳州",
            "region": "柳南区",
            "detailAddress": detailAddress
        }
        address_response = portal_client.post(f"{portal_base_url}/member/address/add", json=address_payload)
        assert address_response.status_code == 200
        address_data = address_response.json()
        assert address_data["code"] == 200
        logger.info(f"{address_response.text}")
    with allure.step("发送get请求获取收获地址列表，获取创建地址id"):
        a_list = portal_client.get(f"{portal_base_url}/member/address/list")
        a_list_data = a_list.json()["data"]
        address_id = next((address["id"] for address in a_list_data if detailAddress == address["detailAddress"]),
                              None)
        logger.info(f"获取完成，收获地址id为{address_id}")
    with allure.step("正式创建订单，发送post请求，验证返回值为预期"):
        order_payload = {
            "memberReceiveAddressId": address_id,
            "cartIds": [
                cart_id
            ]
        }
        order_response = portal_client.post(f"{portal_base_url}/order/generateOrder", json=order_payload)
        order_data = order_response.json()["data"]
        assert order_response.status_code == 200
        logger.info(f"{order_data['orderItemList']}")
    with allure.step("发送post请求查询订单详情，并进行数据库断言"):
        order_detail = portal_client.get(f"{portal_base_url}/order/detail/{order_data['orderItemList'][0]['orderId']}")
        assert order_detail.status_code == 200
        detail_o_data = order_detail.json()["data"]
        assert order_detail["code"] == 200
        logger.info("测试完成")
