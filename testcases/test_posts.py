import allure
import pytest
import json
from utils.logger import get_logger
logger = get_logger(__name__)
with open("data/test_data.json","r",encoding="utf-8")as f:
    data_test_list = json.load(f)["posts"]
@allure.feature("帖子管理")
@allure.story("查询帖子")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("case",data_test_list,
    ids=[f"{d["id"]}-{d["expected"]}"for d in data_test_list])
def test_get_post(base_url,api_client,case):
    post_id = case["id"]
    expected_status = case["expected"]
    description = case.get("description", "无描述")
    logger.info(f"测试场景:{description},测试帖子id:{post_id},测试预测状态码:{expected_status}")
    with allure.step(f"发送get请求获取帖子{post_id}"):
        response = api_client.get(f"{base_url}/posts/{post_id}")
    posts = response.json()
    with allure.step(f"验证返回状态码为{expected_status}"):
        assert response.status_code == expected_status,\
        f"期望状态码{expected_status},实际状态码{response.status_code}"
    if expected_status == 200:
        with allure.step("验证预测的id与返回的一致"):
            assert post_id == posts["id"],"预测的id与返回的不一致"
@pytest.mark.parametrize("post_id, expected", [
    (1, 200),
    (100, 200),
    (999, 404),
])
def test_get_post_by_id(base_url, api_client, post_id, expected):
    logger.info(f"开始测试：获取帖子 {post_id}")
    r = api_client.get(f"{base_url}/posts/{post_id}")
    assert r.status_code == expected
    if expected == 200:
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
@allure.feature("帖子管理")
@allure.story("创建新帖子")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_post(base_url,api_client):
    logger.info("开始测试：创造帖子")
    with allure.step("准备请求数据"):
        payload = {
            "title" : "测试标题",
            "body" : "测试内容",
            "userid" : "1"
        }
    with allure.step("发送post请求创建新帖子"):
        response = api_client.post(f"{base_url}/posts",json= payload)
    with allure.step("验证返回的状态码为201"):
        assert response.status_code == 201
    with allure.step("验证返回数据包含测试标题"):
        data = response.json()
    assert data["title"] == "测试标题"
    logger.info(f"测试通过，创建帖子 ID: {data.get('id')}")
def test_update_post(base_url,api_client):
    logger.info("开始测试：更新帖子")
    payload = {
        "id" : "1",
        "title" : "更改后标题",
        "body" : "更改后内容",
        "userid" : "1"
    }
    response = api_client.put(f"{base_url}/posts/1",json = payload)
    assert response.status_code == 200
    assert response.json()["title"] == "更改后标题"
    logger.info("测试通过，帖子已更新")
def test_delete_post(base_url,api_client):
    logger.info("开始测试：删除帖子")
    response = api_client.delete(f"{base_url}/posts/1")
    assert response.status_code == 200
    logger.info("测试通过，帖子已删除")
