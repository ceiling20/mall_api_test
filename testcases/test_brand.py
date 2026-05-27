import allure
import time
import pytest
import json
from utils.db_helper import get_mysql_conn, sql_delete_brand_by_name
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("品牌管理")
@allure.story("查询品牌列表")
@allure.severity(allure.severity_level.NORMAL)
def test_get_brand_list(auth_client, base_url):
    logger.info("开始测试")
    with allure.step("发送get请求，验证响应码正确"):
        response = auth_client.get(f"{base_url}/brand/list", params={"pageNum": 1, "pageSize": 5})
    logger.info(f"响应码为:{response.status_code}")
    logger.info(f"响应内容:{response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    brand_list = data["data"]["list"]
    logger.info(f"品牌列表为:{brand_list}")
    logger.info(f"品牌有多少类:{len(brand_list)}")
    assert isinstance(brand_list, list)
    with allure.step("测试响应体主要参数是否存在"):
        if not brand_list:
            pytest.skip("没有品牌数据，跳过本次测试")
        first = brand_list[0]
        assert "id" in first
        assert "name" in first
        assert "logo" in first
        logger.info("品牌列表查询测试通过")


with open("data/test_brand_data.json", "r", encoding="utf-8") as s:
    get_brand_data_list = json.load(s)["get_brand"]


@allure.feature("品牌管理")
@allure.story("查询品牌")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case", get_brand_data_list, ids=[f"test_{c['id']}" for c in get_brand_data_list])
def test_get_brand(auth_client, base_url, case):
    logger.info("开始测试")
    with allure.step("发送get请求查询品牌，验证响应码是否正确"):
        response = auth_client.get(f"{base_url}/brand/{case['id']}")
    logger.info(f"响应码：{response.status_code}")
    logger.info(f"响应内容:{response.text}")
    data = response.json()
    expected = case["expected"]
    assert response.status_code == case["expected"]["http_status"]
    if expected["business_code"] is not None:
        assert data["code"] == case["expected"]["business_code"]
    brand = data["data"]
    with allure.step("预测数据是否为空，有数据的话，测试响应体主要参数是否存在"):
        if expected["expected_normal"]:
            assert brand is not None
            for body in expected.get("body", []):
                assert body in brand
        else:
            if response.status_code == 200:
                assert brand is None


with open("data/test_brand_data.json", "r", encoding="utf-8") as f:
    create_brand_data = json.load(f)["create_brand"]


@allure.feature("品牌管理")
@allure.story("创建品牌")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case", create_brand_data,
                         ids=[f"cre_test{case['description']}" for case in create_brand_data])
def test_create_brand_by_name(auth_client, base_url, case):
    logger.info("开始测试：")
    test_name = f"cre_{int(time.time())}"
    body = case["body"]
    payload = {"name": test_name,
               "logo": body.get("logo")
               }
    if "name" in body:
        payload["name"] = body["name"]
    with allure.step("发送post请求创建品牌，验证返回状态码为200"):
        cre_response = auth_client.post(f"{base_url}/brand/create", json=payload)
        expected = case["expected"]
        business_code = expected.get("business_code")
        create_data = cre_response.json()
        assert cre_response.status_code == expected["http_status"]
        if business_code is not None:
            assert create_data["code"] == expected["business_code"]
        logger.info(f"创建品牌响应: {cre_response.text}")
        if expected["expected_normal"]:
            with allure.step("数据库断言验证："):
                conn = get_mysql_conn()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id,logo FROM pms_brand WHERE name = %s", (test_name,))
                    row = cursor.fetchone()
                    assert row is not None, f"未找到brand_name={test_name}"
                    assert body["logo"] in row["logo"]
                    brand_id = row["id"]
            finally:
                conn.close()
    with allure.step("清理测试品牌"):
        sql_delete_brand_by_name(test_name)
        logger.info(f"已删除测试品牌 name={test_name}")


with open("data/test_brand_data.json", "r", encoding="utf-8") as f:
    update_data = json.load(f)["update_brand"]


@allure.feature("品牌管理")
@allure.story("更新品牌")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case", update_data, ids=[f"upd_test{case['description']}" for case in update_data])
def test_update_brand_by_name(auth_client, base_url, case):
    logger.info("开始测试：")
    test_name = f"cre_{int(time.time())}"
    body = case["body"]
    payload = {"name": test_name,
               "logo": 8676 }
    with allure.step("发送post请求创建品牌，验证返回状态码为200"):
        cre_response = auth_client.post(f"{base_url}/brand/create", json=payload)
        assert cre_response.status_code == 200
        create_data = cre_response.json()
        assert create_data["code"] == 200
        logger.info(f"创建品牌响应: {cre_response.text}")
    with allure.step("数据库断言验证："):
        conn = get_mysql_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM pms_brand WHERE name = %s", (test_name,))
                row = cursor.fetchone()
                assert row is not None, f"未找到brand_name={test_name}"
                brand_id = row["id"]
        finally:
            conn.close()
    logger.info("开始更新品牌")
    body = case.get("body")
    expected = case["expected"]
    u_id = body.get("id", brand_id)
    business_code = expected.get("business_code", None)
    if body:
        update_payload = {
            "name": test_name,
            "id": u_id
        }
        if "logo" in body:
            update_payload["logo"] = body.get("logo")
    else:
        update_payload = {
            "id": u_id,
        }
    with allure.step(f"发送post请求更新品牌，验证返回状态码为200，更新品牌id：{u_id}", ):
        upd_response = auth_client.post(f"{base_url}/brand/update/{u_id}", json=update_payload)
        assert upd_response.status_code == expected["http_status"]
        if business_code is not None:
            assert upd_response.json()["code"] == business_code
        logger.info(f"更新品牌响应：{upd_response.text}")
        if expected["expected_normal"]:
            with allure.step("验证数据库中品牌信息已更新"):
                conn = get_mysql_conn()
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT name,logo FROM pms_brand WHERE id = %s", (brand_id,))
                        row = cursor.fetchone()
                        assert row is not None
                        assert row["name"] == test_name
                        assert row["logo"] == body.get("logo")
                finally:
                    conn.close()
    with allure.step("清理测试品牌"):
        sql_delete_brand_by_name(test_name)
        logger.info(f"已删除测试品牌 name={test_name}")


with open("data/test_brand_data.json", "r", encoding="utf-8") as f:
    delete_data = json.load(f)["delete_brand"]


@allure.feature("品牌管理")
@allure.story("删除品牌")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("case", delete_data, ids=[f"del_test{case['description']}" for case in delete_data])
def test_delete_brand_by_name(auth_client, base_url, case):
    logger.info("开始测试")
    test_name = f"del_{int(time.time())}"
    payload = {"name": test_name,
               "logo": 500}
    with allure.step("发送post请求创建新品牌，验证返回状态码为200"):
        cre_response = auth_client.post(f"{base_url}/brand/create", json=payload)
        expected = case["expected"]
        business_code = expected.get("business_code", None)
        assert cre_response.status_code == expected["http_status"]
        if business_code is not None:
            assert cre_response.json()["code"] == business_code
        if expected['expected_normal']:
            conn = get_mysql_conn()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM pms_brand WHERE name = %s", (test_name,))
                    row = cursor.fetchone()
                    assert row is not None, f"未找到 brand_name={test_name}"
                    brand_id = row["id"]
            finally:
                conn.close()
            delete_resp = auth_client.get(f"{base_url}/brand/delete/{brand_id}")
            print("状态码:", delete_resp.status_code)
            print("响应内容:", delete_resp.text)
            assert delete_resp.status_code == 200
            assert delete_resp.json()["code"] == 200
            conn = get_mysql_conn()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM pms_brand WHERE id = %s", (brand_id,))
                    row = cursor.fetchone()
                    assert row is None
            finally:
                conn.close()
    with allure.step("清理测试品牌"):
        sql_delete_brand_by_name(test_name)
        logger.info(f"已删除测试品牌 name={test_name}")
