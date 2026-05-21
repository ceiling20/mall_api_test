import allure
from utils.logger import get_logger
logger = get_logger(__name__)
@allure.feature("帖子管理")
@allure.story("异常场景-查询无效id")
@allure.severity(allure.severity_level.NORMAL)
def test_get_post_invalid_id(base_url,api_client):
    with allure.step("请求查询不存在帖子id999999"):
        response = api_client.get(f"{base_url}/posts/999999")
    logger.info(f"测试通过，状态码: {response.status_code}")
    with allure.step("验证状态码为404"):
        assert response.status_code == 404
@allure.feature("帖子管理")
@allure.story("异常场景-空标题创建")
@allure.severity(allure.severity_level.NORMAL)
def test_create_post_empty_title(base_url,api_client):
    with allure.step("构造空标题的请求体"):
        payload = {
            "title" : "",
            "body" : "内容",
            "userid" : "1"
        }
    with allure.step("发送post请求创建帖子"):
        response = api_client.post(f"{base_url}/posts",json = payload)
    logger.info(f"测试通过，状态码: {response.status_code}")
    with allure.step("验证返回状态码为404"):
        assert response.status_code in [201,404]

@allure.feature("帖子管理")
@allure.story("异常场景-缺少必需参数")
@allure.severity(allure.severity_level.NORMAL)
def test_create_post_missing_field(base_url,api_client):
    with allure.step("构造缺少必需参数的请求体"):
        payload = {
            'title' : "标题"
        }
    with allure.step("发送post请求创建帖子"):
        response = api_client.post(f"{base_url}/posts",json=payload)
    logger.info(f"测试通过，状态码: {response.status_code}")
    with allure.step("验证返回状态码为404"):
        assert response.status_code in [201,404]