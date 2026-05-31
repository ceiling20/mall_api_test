import pymysql
from utils.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def get_mysql_conn():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
def get_brand_by_id(brand_id: int, conn):
    with conn.cursor() as cursor:
        sql = "SELECT id ,name FROM pms_brand WHERE id = %s"
        cursor.execute(sql, (brand_id,))
        result = cursor.fetchone()
    return result


def assert_product_created_by_sn(product_sn: str, expected_name: str, conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT name, price, stock FROM pms_product WHERE product_sn = %s", (product_sn,))
        row = cursor.fetchone()
        print(f"数据库查询结果（商品）: {row}")
        assert row is not None, f"未找到 product_sn={product_sn}"
        assert row["name"] == expected_name


def sql_delete_product_by_sn(product_sn: str, conn):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM pms_product WHERE product_sn = %s", (product_sn,))
        conn.commit()


def sql_delete_brand_by_name(brand_name: str, conn):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM pms_brand WHERE name = %s", (brand_name,))
        conn.commit()
