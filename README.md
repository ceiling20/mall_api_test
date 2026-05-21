# api-test 接口自动化项目
![run pytest](https://github.com/ceiling20/api-automation-test/actions/workflows/test.yml/badge.svg)
## 项目结构

```text
api_test/                      # 项目根目录
├── data/                      # 测试数据目录
│   └── test_data.json         # 数据驱动测试的输入数据（帖子ID、预期状态码等）
├── db/                        # 本地数据库目录（SQLite 文件存放位置，通常不提交到 git）
│   └── test.db                # SQLite 数据库文件（由 init_db.py 生成）
├── docs/                      # 文档及截图
│   └── allure-screenshots/    # Allure 报告截图（用于 README 展示）
├── testcases/                 # 测试用例目录
│   ├── __init__.py            # 标识为 Python 包
│   ├── test_exceptions.py     # 异常场景测试（无效ID、空参数、超长字符串等）
│   └── test_posts.py          # 正常接口测试（GET/POST/PUT/DELETE，数据驱动）
├── utils/                     # 工具函数/类目录
│   ├── __init__.py
│   ├── config.py              # 配置管理（BASE_URL, TIMEOUT 等）
│   ├── db_helper.py           # 数据库操作函数（get_post_by_id, assert_post_matches_api）
│   └── logger.py              # 日志工具（封装 logging，输出到控制台）
├── .gitignore                 # Git 忽略规则（临时文件、虚拟环境、报告等）
├── conftest.py                # pytest 全局配置（fixture：base_url, api_client）
├── init_db.py                 # 初始化 SQLite 数据库（创建表，插入示例数据）
├── pyproject.toml             # 项目元数据和构建配置（如 pytest 配置）
├── pytest.ini                 # pytest 运行时配置（测试路径、命令行参数等）
├── README.md                  # 项目说明文档（结构、用法、报告示例）
└── requirements.txt           # Python 依赖列表（pytest, requests, allure-pytest 等）
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

本项目已集成 Allure 框架，
可生成可视化测试报告，按业务模块分组展示，并支持步骤级断言查看。

### 生成报告
```bash
# 运行测试并收集数据（已配置在 pytest.ini 中，直接运行 pytest 即可）
pytest

# 查看报告（本地临时服务）
allure serve allure-results

## 报告示例
按文件和类组织的测试套件 (Suites)
(./docs/allure-screenshots/suites.png)

单个用例步骤详情（含 severity 和 step）
(./docs/allure-screenshots/test_create_post.png)

测试严重程度分布 (Graphs)
(./docs/allure-screenshots/graphs.png)

## 数据驱动测试
测试数据存放在 `data/test_data.json` 中，
通过 `@pytest.mark.parametrize` 实现数据与逻辑分离。
新增测试场景只需修改 JSON 文件，无需改动代码。

运行数据驱动测试：
```bash
pytest testcases/test_posts.py -k "test_get_post" -v
## 数据库断言
使用前请先运行 `python init_db.py` 
初始化 SQLite 数据库（会在 `db/` 目录下生成 `test.db` 文件）。
本框架支持接口返回数据与数据库内容的一致性校验。
通过 `utils/db_helper.py` 中的 `assert_post_matches_api` 函数，
可快速验证 GET 请求返回的帖子信息与本地 SQLite 数据库中的记录完全一致。

此能力可用于真实业务系统中，确保接口读取的数据与落库数据一致。