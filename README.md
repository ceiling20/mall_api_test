## 项目结构

```text
api_test/
├── conftest.py                 # pytest fixture 配置
├── testcases/
│   ├── test_posts.py           # 正常接口测试 (GET/POST/PUT/DELETE)
│   └── test_exceptions.py      # 异常场景测试
├── utils/
│   ├── config.py               # 基础配置 (BASE_URL, TIMEOUT)
│   └── logger.py               # 日志工具
├── report/                     # 测试报告输出目录
├── requirements.txt            # 项目依赖
└── pytest.ini                  # pytest 运行配置
```

##环境要求
- Python 3.8+
- pip

##运行方式
```bash

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest

# 运行指定文件
pytest testcases/test_posts.py -v

## Allure 报告

本项目已集成 Allure 框架，可生成可视化测试报告，按业务模块分组展示，并支持步骤级断言查看。

### 生成报告
```bash
# 运行测试并收集数据（已配置在 pytest.ini 中，直接运行 pytest 即可）
pytest

# 查看报告（本地临时服务）
allure serve allure-results

## 报告示例
按文件和类组织的测试套件 (Suites)
https://./docs/allure-screenshots/suites.png

单个用例步骤详情（含 severity 和 step）
https://./docs/allure-screenshots/test_create_post.png

测试严重程度分布 (Graphs)
https://./docs/allure-screenshots/graphs.png

## 数据驱动测试
测试数据存放在 `data/test_data.json` 中，
通过 `@pytest.mark.parametrize` 实现数据与逻辑分离。
新增测试场景只需修改 JSON 文件，无需改动代码。

运行数据驱动测试：
```bash
pytest
## 数据库断言

本框架支持接口返回数据与数据库内容的一致性校验。
通过 `utils/db_helper.py` 中的 `assert_post_matches_api` 函数，
可快速验证 GET 请求返回的帖子信息与本地 SQLite 数据库中的记录完全一致。

此能力可用于真实业务系统中，确保接口读取的数据与落库数据一致。