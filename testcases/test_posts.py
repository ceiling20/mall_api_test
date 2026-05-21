import allure
import pytest
import json
from utils.logger import get_logger
from utils.db_helper import assert_post_matches_api
logger = get_logger(__name__)
with open("data/test_data.json","r",encoding="utf-8")as f:
    get_data_test = json.load(f)["get_posts"]
@allure.feature("帖子管理")
@allure.story("查询帖子")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case",get_data_test,
    ids=[f"{d["id"]}-{d["expected"]}"for d in get_data_test])
def test_get_post(base_url,api_client,case):
    post_id = case["id"]
    expected_status = case["expected"]
    description = case.get("description", "无描述")
    logger.info(f"测试场景:{description},测试帖子id:{post_id},测试预测状态码:{expected_status}")
    with allure.step(f"发送get请求获取帖子{post_id}"):
        response = api_client.get(f"{base_url}/posts/{post_id}")
    api_data = response.json()
    with allure.step(f"验证返回状态码为{expected_status}"):
        if isinstance(expected_status,list):
            assert response.status_code in expected_status
        else:
            assert response.status_code == expected_status,\
            f"期望状态码{expected_status},实际状态码{response.status_code}"
    if expected_status == 200:
        assert_post_matches_api(post_id,api_data)
@allure.feature("帖子管理")
@allure.story("帖子查询")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("post_id, expected", [
    (1, 200),
    (100, 200),
    (999, 404),
])
def test_get_post_by_id(base_url, api_client, post_id, expected):
    logger.info(f"开始测试：获取帖子 {post_id}")
    with allure.step("发送get请求获取对应帖子"):
        r = api_client.get(f"{base_url}/posts/{post_id}")
    with allure.step("验证返回的状态码是否与预期状态码相同"):
        assert r.status_code == expected
    if expected == 200:
        with allure.step("验证预测的id与返回的一致"):
            assert r.json()["id"] == post_id
    logger.info(f"测试通过，状态码: {r.status_code}")
@allure.feature("帖子管理")
@allure.story("获取帖子列表")
@allure.severity(allure.severity_level.NORMAL)
def test_get_post_list(base_url,api_client):
    logger.info(f"开始测试，获取帖子列表")
    with allure.step("发送get请求获取所有帖子"):
        response = api_client.get(f"{base_url}/posts")
    with allure.step("验证状态码为200"):
        assert response.status_code == 200
    with allure.step("验证返回列表不为空"):
        assert len(response.json()) > 0
    logger.info(f"测试通过，共 {len(response.json())} 条帖子")
with open("data/test_data.json","r",encoding="utf-8") as f:
    create_post_test = json.load(f)["create_posts"]
@allure.feature("帖子管理")
@allure.story("创建新帖子")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("case",create_post_test,ids=(f"{c["expected"]}"for c in create_post_test))
def test_create_post(base_url,api_client,case):
    expected_status = case["expected"]
    description = case["description"]
    logger.info(f"测试场景:{description},测试预测状态码:{expected_status}")
    logger.info("开始测试：创造帖子")
    with allure.step("准备请求数据"):
        payload = {
            "title" : case.get("title"),
            "body" : case["body"],
            "userid" : case["userId"]
        }
    with allure.step("发送post请求创建新帖子"):
        response = api_client.post(f"{base_url}/posts",json= payload)
    with allure.step("验证返回的状态码为预期状态码"):
        assert response.status_code in [expected_status,200,201]
    with allure.step("验证返回数据包含标题"):
        data = response.json()
    assert data["title"] == case.get("title")
    logger.info(f"测试通过，创建帖子 ID: {data.get('id')}")
with open("data/test_data.json","r",encoding="utf-8") as f:
    update_post_data = json.load(f)["update_posts"]
@allure.feature("帖子管理")
@allure.story("更新帖子")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case",update_post_data,ids=(f"{u["id"]}-{u["expected"]}"for u in update_post_data))
def test_update_post(base_url,api_client,case):
    logger.info("开始测试：更新帖子")
    with allure.step("构造请求体内容"):
        payload = {
            "id" : case["id"],
            "title" : case["title"],
            "body" : case["body"],
            "userid" : case["userId"]
        }
    with allure.step("发送put请求更新帖子"):
        response = api_client.put(f"{base_url}/posts/{case["id"]}",json = payload)
    with allure.step("验证返回的状态码为{case[expected]}"):
        if case["expected"] == 200:
            assert response.status_code == 200
            with allure.step("验证返回数据包含更改后标题"):
                assert response.json()["title"] == case["title"]
        else:
            assert response.status_code in [case["expected"], 200, 201]
    logger.info("测试通过，帖子已更新")
@allure.feature("帖子管理")
@allure.story("删除帖子")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_post(base_url,api_client):
    logger.info("开始测试：删除帖子")
    with allure.step("发送delete请求删除帖子"):
        response = api_client.delete(f"{base_url}/posts/1")
    with allure.step("验证返回的状态码为200"):
        assert response.status_code == 200
    logger.info("测试通过，帖子已删除")
