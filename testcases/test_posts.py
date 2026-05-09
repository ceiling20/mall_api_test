import requests
import pytest
from utils.logger import get_logger
logger = get_logger(__name__)
@pytest.mark.parametrize("user_id",[1,2,3])
def test_get_post(base_url,api_client,user_id):
    logger.info(f"开始测试：获取用户{user_id}的帖子")
    response = api_client.get(f"{base_url}/posts?userId={user_id}")
    posts = response.json()
    assert response.status_code == 200
    assert len(posts) > 0
    for post in posts:
         assert post["userId"] == user_id
    logger.info(f"测试通过，找到{len(posts)}条帖子")
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
def test_get_post_list(base_url,api_client):
    logger.info(f"开始测试，获取帖子列表")
    response = requests.get(f"{base_url}/posts")
    assert response.status_code == 200
    assert len(response.json()) > 0
    logger.info(f"测试通过，共 {len(response.json())} 条帖子")
def test_create_post(base_url,api_client):
    logger.info("开始测试：创造帖子")
    payload = {
        "title" : "测试标题",
        "body" : "测试内容",
        "userid" : "1"
    }
    response = requests.post(f"{base_url}/posts",json= payload)
    assert response.status_code == 201
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
    response = requests.put(f"{base_url}/posts/1",json = payload)
    assert response.status_code == 200
    assert response.json()["title"] == "更改后标题"
    logger.info("测试通过，帖子已更新")
def test_delete_post(base_url,api_client):
    logger.info("开始测试：删除帖子")
    response = requests.delete(f"{base_url}/posts/1")
    assert response.status_code == 200
    logger.info("测试通过，帖子已删除")
