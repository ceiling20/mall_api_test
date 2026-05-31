import allure
import time
import pytest
import json
from utils.db_helper import sql_delete_product_by_sn,assert_product_created_by_sn
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("商品管理")
@allure.story("查询商品列表")
@allure.severity(allure.severity_level.NORMAL)
def test_get_product_list(auth_client, admin_base_url):
    logger.info("开始测试")
    with allure.step("发送get请求，验证响应码正确"):
        response = auth_client.get(f"{admin_base_url}/product/list", params={"pageNum": 1, "pageSize": 5})
    logger.info(f"响应码为:{response.status_code}")
    logger.info(f"响应内容:{response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    product_list = data["data"]["list"]
    logger.info(f"商品列表为:{product_list}")
    logger.info(f"商品有多少类:{len(product_list)}")
    assert isinstance(product_list, list)
    with allure.step("测试响应体主要参数是否存在"):
        if not product_list:
            pytest.skip("没有商品数据，跳过本次测试")
        first = product_list[0]
        assert "id" in first
        assert "name" in first
        assert "price" in first
        assert "stock" in first
        assert "productSn" in first
        logger.info("商品列表查询测试通过")


with open("data/test_product_data.json", "r", encoding="utf-8") as s:
    get_product_data_list = json.load(s)["get_product"]


@allure.feature("商品管理")
@allure.story("查询商品")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case", get_product_data_list, ids=[f"test_{c['id']}" for c in get_product_data_list])
def test_get_product(auth_client, admin_base_url, case):
    logger.info("开始测试")
    with allure.step("发送get请求查询商品，验证响应码是否正确"):
        response = auth_client.get(f"{admin_base_url}/product/updateInfo/{case['id']}")
    logger.info(f"响应码：{response.status_code}")
    logger.info(f"响应内容:{response.text}")
    get_data = response.json()
    expected = case["expected"]
    assert response.status_code == case["expected"]["http_status"]
    if "business_code" in expected:
        assert get_data["code"] == expected["business_code"]
    if "data" in expected:
        assert get_data["data"] == expected["data"]
    if "message" in expected:
        assert get_data["message"] == expected["message"]
    product = get_data["data"]
    with allure.step("预测数据是否为空，有数据的话，测试响应体主要参数是否存在"):
        if expected["expected_normal"]:
            assert product is not None
            for body in expected.get("body", []):
                assert body in product
        else:
            if response.status_code == 200:
                assert product is None


with open("data/test_product_data.json", "r", encoding="utf-8") as f:
    create_product_data = json.load(f)["create_product"]


@allure.feature("商品管理")
@allure.story("创建商品")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case", create_product_data,
                         ids=[f"cre_test{case['description']}" for case in create_product_data])
def test_create_product_by_sn(auth_client, admin_base_url, case,db_conn):
    logger.info("开始测试：")
    test_sn = f"cre_{int(time.time())}"
    body = case["body"]
    payload = {"price": body.get("price",{}),
               "stock": body.get("stock",{}),
               "productSn": test_sn}
    if "name" in body:
        payload["name"] = body["name"]
    with allure.step("发送post请求创建商品，验证返回状态码为200"):
        cre_response = auth_client.post(f"{admin_base_url}/product/create", json=payload)
        expected = case["expected"]
        business_code = expected.get("business_code")
        create_data = cre_response.json()
        assert cre_response.status_code == expected["http_status"]
        if "business_code" in expected:
            assert create_data["code"] == business_code
        if "data" in expected:
            assert create_data["data"] == expected["data"]
        if "message" in expected:
            assert create_data["message"] == expected["message"]
        logger.info(f"创建商品响应: {cre_response.text}")
        if expected["expected_normal"]:
            with allure.step("数据库断言验证："):
                assert_product_created_by_sn(test_sn,body["name"],db_conn)

    with allure.step("清理测试商品"):
        sql_delete_product_by_sn(test_sn,db_conn)
        logger.info(f"已删除测试商品 productSn={test_sn}")


with open("data/test_product_data.json", "r", encoding="utf-8") as f:
    update_data = json.load(f)["update_product"]


@allure.feature("商品管理")
@allure.story("更新商品")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case", update_data, ids=[f"upd_test{case['description']}" for case in update_data])
def test_update_product_by_sn(auth_client, admin_base_url, case,db_conn):
    logger.info("开始测试：")
    test_sn = f"update_{int(time.time())}"
    unique_name = f"测试商品{int(time.time())}"
    payload = {"name": unique_name,
               "price": 456456,
               "stock": 745,
               "productSn": test_sn}
    with allure.step("发送post请求创建商品，验证返回状态码为200"):
        cre_response = auth_client.post(f"{admin_base_url}/product/create", json=payload)
        assert cre_response.status_code == 200
        create_data = cre_response.json()
        assert create_data["code"] == 200
        logger.info(f"创建商品响应: {cre_response.text}")
    with allure.step("数据库断言验证："):
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT id FROM pms_product WHERE product_sn = %s", (test_sn,))
            row = cursor.fetchone()
            assert row is not None, f"未找到product_sn={test_sn}"
            product_id = row["id"]
    logger.info("开始更新商品")
    body = case.get("body")
    expected = case["expected"]
    u_id = body.get("id", product_id)
    business_code = expected.get("business_code",None)
    if body:
        update_payload = {
            "id": u_id,
            "price": body.get("price"),
            "stock": body.get("stock")
        }
        if "name" in body:
            update_payload["name"] = body.get("name")
    else:
        update_payload = {
            "id": u_id,
        }
    with allure.step(f"发送post请求更新商品，验证返回状态码为200，更新商品id：{u_id}", ):
        upd_response = auth_client.post(f"{admin_base_url}/product/update/{u_id}", json=update_payload)
        assert upd_response.status_code == expected["http_status"]
        if "business_code" in expected:
            assert upd_response.json()["code"] == business_code
        if "data" in expected:
            assert upd_response.json()["data"] == expected["data"]
        if "message" in expected:
            assert upd_response.json()["message"] == expected["message"]
        logger.info(f"更新商品响应：{upd_response.text}")
        if expected["expected_normal"]:
            with allure.step("验证数据库中商品信息已更新"):
                with db_conn.cursor() as cursor:
                    cursor.execute("SELECT name,price,stock FROM pms_product WHERE id = %s", (product_id,))
                    row = cursor.fetchone()
                    assert row is not None
                    assert row["name"] == body.get("name")
                    assert row["price"] == body.get("price")
                    assert row["stock"] == body.get("stock")
    with allure.step("清理测试商品"):
        sql_delete_product_by_sn(test_sn,db_conn)
        logger.info(f"已删除测试商品 productSn={test_sn}")

with open("data/test_product_data.json","r",encoding="utf-8")as f:
    delete_data = json.load(f)["delete_product"]
@allure.feature("商品管理")
@allure.story("删除商品")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("case",delete_data,ids=[f"del_test{case['description']}"for case in delete_data])
def test_delete_product_by_sn(auth_client, admin_base_url,case,db_conn):
    logger.info("开始测试")
    expected = case["expected"]
    if "ids" in case:
        product_id = case["ids"]
    else:
        test_name = f"测试商品{int(time.time())}"
        test_sn = f"del_{int(time.time())}"
        payload = {"name": test_name,
                   "stock": 500,
                   "price": 5000,
                   "productSn": test_sn}
        with allure.step("发送post请求创建新商品"):
            cre_response = auth_client.post(f"{admin_base_url}/product/create", json=payload)
            assert cre_response.status_code == expected["http_status"]
            if "business_code" in expected:
                assert cre_response.json()["code"] == expected["business_code"]
            if "data" in expected:
                assert cre_response.json()["data"] == expected["data"]
            if "message" in expected:
                assert cre_response.json()["message"] == expected["message"]
        if expected['expected_normal']:
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT id FROM pms_product WHERE product_sn = %s", (test_sn,))
                row = cursor.fetchone()
                assert row is not None, f"未找到 product_sn={test_sn}"
                product_id = row["id"]
    if "ids" in case or expected['expected_normal']:
        with allure.step("发送删除请求"):
            delete_url = f"{admin_base_url}/product/update/deleteStatus"
            delete_resp = auth_client.post(delete_url, params={"ids": product_id, "deleteStatus": 1})
            print("状态码:", delete_resp.status_code)
            print("响应内容:", delete_resp.text)
            if "ids" in case:
                assert delete_resp.status_code == expected["http_status"]
                if "business_code" in expected:
                    assert delete_resp.json()["code"] == expected["business_code"]
                if "message" in expected:
                    assert delete_resp.json()["message"] == expected["message"]
                if "data" in expected:
                    assert delete_resp.json()["data"] == expected["data"]
            else:
                assert delete_resp.status_code == 200
                assert delete_resp.json()["code"] == 200
                with db_conn.cursor() as cursor:
                    cursor.execute("SELECT delete_status FROM pms_product WHERE id = %s", (product_id,))
                    row = cursor.fetchone()
                    assert row is not None
                    assert row["delete_status"] == 1, f"商品 {product_id} 的 delete_status 未变为 1"
    if "ids" not in case:
        with allure.step("清理测试商品"):
            sql_delete_product_by_sn(test_sn,db_conn)
            logger.info(f"已删除测试商品 productSn={test_sn}")
