# mall-api-test 商场接口自动化测试
[![Allure Report](https://img.shields.io/badge/Allure-Report-blue)](https://ceiling20.github.io/mall_api_test/)
[![CI](https://github.com/ceiling20/mall_api_test/actions/workflows/ci.yml/badge.svg)](https://github.com/ceiling20/mall_api_test/actions/workflows/ci.yml)

## 技术栈

- Python 3.11
- pytest（测试框架）
- requests（HTTP 客户端）
- PyMySQL（数据库断言）
- Allure（测试报告）
- Docker Compose（本地环境）
- GitHub Actions（CI/CD）

## 项目结构

```text
mall_api_test/                 # 项目根目录
├── .github/                   # GitHub Actions CI/CD 配置
│   └── workflows/
│       └── ci.yml             # 工作流：启动 MySQL + mall-admin/mall-portal，运行 pytest，部署 Allure 报告
├── data/                      # 测试数据目录
│   ├── test_brand_data.json   # 品牌接口测试数据（品牌名、预期状态码等）
│   └── test_product_data.json # 商品接口测试数据（商品参数、SKU、预期状态码等）
├── docs/                      # 文档及截图
│   └── allure-screenshots/    # Allure 报告截图（用于 README 展示）
├── logs/                      # 运行日志目录（不提交到 git）
│   └── test.log               # 日志文件（自动生成）
├── sql/                       # 数据库初始化脚本
│   └── mall.sql               # 商场数据库完整建表 + 初始数据
├── testcases/                 # 测试用例目录
│   ├── __init__.py
│   ├── test_brand.py          # 品牌管理（增删改查、参数校验）
│   ├── test_product.py        # 商品管理（CRUD + 数据驱动）
│   └── test_order.py          # 订单流程（登录 → 下单完整链路）
├── utils/                     # 工具函数目录
│   ├── __init__.py
│   ├── config.py              # 配置管理（BASE_URL_ADMIN, BASE_URL_PORTAL, DB 连接）
│   ├── db_helper.py           # 数据库操作（MySQL 连接、查询、断言）
│   └── logger.py              # 日志工具（控制台 + 文件输出）
├── .gitignore                 # Git 忽略规则（虚拟环境、报告、日志等）
├── conftest.py                # pytest 全局 fixture（token、客户端、DB 连接）
├── docker-compose.yml         # 本地开发环境（MySQL/Redis/MongoDB/RabbitMQ/ES 等中间件）
├── pyproject.toml             # 项目元数据和 Python 依赖声明
├── pytest.ini                 # pytest 运行时配置（测试路径、命令行参数等）
├── README.md                  # 项目说明文档
└── requirements.txt           # Python 依赖列表
```

## 被测系统

| 服务 | 端口 | 说明 |
|------|------|------|
| mall-admin | 8080 | 后台管理（品牌、商品） |
| mall-portal | 8085 | 前台商城（订单） |
| MySQL | 3306 | 业务数据库 |

> 本地开发需先启动 Docker Compose 中间件，再启动 mall-admin / mall-portal 后端服务。

## 环境要求

- Python 3.8+
- Docker Desktop（本地运行中间件）
- mall-admin / mall-portal 后端服务（Java 17，源码见 [mall](https://github.com/macrozheng/mall)）

## 运行方式

```bash
# 1. 启动中间件
docker-compose up -d mysql redis mongo rabbitmq

# 2. 初始化数据库
mysql -h 127.0.0.1 -uroot -p123456 mall < sql/mall.sql

# 3. 安装 Python 依赖
pip install -r requirements.txt

# 4. 启动后端服务（IDEA 或命令行）后运行测试
pytest

# 运行指定模块
pytest testcases/test_brand.py -v
pytest testcases/test_product.py -v
pytest testcases/test_order.py -v

# 按关键字筛选用例
pytest testcases/test_brand.py -k "create" -v
```

## Allure 报告

本项目已集成 Allure 框架，支持步骤级断言、参数化展示、失败自动截图。

### 本地查看

```bash
# 运行测试并收集数据
pytest

# 启动本地 Allure 服务查看报告
allure serve allure-results
```

### 在线报告

最新测试报告自动部署至 GitHub Pages：

[https://ceiling20.github.io/mall_api_test/](https://ceiling20.github.io/mall_api_test/)

## 数据驱动测试

品牌和商品用例均采用 `@pytest.mark.parametrize` + JSON 数据文件实现数据与逻辑分离。

```bash
# 运行所有参数化用例
pytest testcases/test_brand.py -v
```

新增测试场景只需在 `data/test_brand_data.json` 或 `data/test_product_data.json` 中添加条目。

## 数据库断言

接口返回数据会与 MySQL 数据库实际记录进行交叉比对：

- `utils/db_helper.py` 提供 `get_mysql_conn()` 直连数据库
- 验证 GET 接口返回的字段与 `mall.sql` 初始数据一致
- 验证 POST/PUT 接口写入的数据落库正确

## CI/CD

每次 push 或 PR 到 main 分支，GitHub Actions 自动执行：

1. 启动 MySQL / Redis / MongoDB / RabbitMQ 服务容器
2. 初始化数据库（导入 mall.sql）
3. 从 ghcr.io 拉取并启动 mall-admin（8080）+ mall-portal（8085）
4. 运行全部 pytest 用例
5. 生成 Allure 报告并部署至 GitHub Pages

工作流定义见 `.github/workflows/ci.yml`。

## 日志

`utils/logger.py` 同时输出到控制台和 `logs/test.log`，断言失败时可直接查日志定位。

---

**备注**：本地调试如遇中文校验消息不一致，检查 IDE 和终端的系统语言设置。
