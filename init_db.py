import sqlite3
conn = sqlite3.connect("db/test.db")
cursor = conn.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY,
        title TEXT,
        body TEXT,
        userId INTEGER
        )
        ''')
sample_posts = [
    (1,"sunt aut facere repellat provident occaecati excepturi optio reprehenderit", "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto", 1),
    (2, "qui est esse", "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla", 1),
    (3, "ea molestias quasi exercitationem repellat qui ipsa sit aut", "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut", 1),
]
cursor.executemany("INSERT OR REPLACE INTO posts VALUES(?,?,?,?)",sample_posts)
conn.commit()
conn.close()
print("数据库初始化完成")
