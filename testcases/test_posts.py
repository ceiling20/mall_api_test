import requests
import pytest
@pytest.mark.parametrize("user_id",[1,2,3])
def test_get_post(base_url,user_id):
     response = requests.get(f"{base_url}/posts?userId={user_id}")
     posts = response.json()
     assert response.status_code == 200
     assert len(posts) > 0
     for post in posts:
         assert post["userId"] == user_id
def test_get_post_list(base_url):
    response = requests.get(f"{base_url}/posts")
    assert response.status_code == 200
    assert len(response.json()) > 0
def test_create_post(base_url):
    payload = {
        "title" : "测试标题",
        "body" : "测试内容",
        "userid" : "1"
    }
    response = requests.post(f"{base_url}/posts",json= payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试标题"
def test_update_post(base_url):
    payload = {
        "id" : "1",
        "title" : "更改后标题",
        "body" : "更改后内容",
        "userid" : "1"
    }
    response = requests.put(f"{base_url}/posts/1",json = payload)
    assert response.status_code == 200
    assert response.json()["title"] == "更改后标题"
def test_delete_post(base_url):
    response = requests.delete(f"{base_url}/posts/1")
    assert response.status_code == 200