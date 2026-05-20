import sqlite3
import allure
from pathlib import Path
DB_PATH = Path(__file__).parent.parent/"db"/"test.db"
def get_post_by_id(post_id:int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id,title,body,userId FROM posts where id = ?",(post_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
def assert_post_matches_api(post_id:int,api_data:dict):
    db_post = get_post_by_id(post_id)
    with allure.step(f"验证数据库存在帖子{post_id}"):
        assert db_post is not None,f"数据库中找不到帖子{post_id}"
    with allure.step(f"验证接口返回数据与数据库一致"):
        assert api_data["id"] == db_post["id"]
        assert api_data["title"] == db_post["title"]
        assert api_data["body"] == db_post["body"]
        assert api_data["userId"] == db_post["userId"]