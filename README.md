#接口自动化测试项目
基于pytest + requests 的接口测试项目，测试JSONPlaceholder开放API

##项目结构
api_test/
├── conftest.py          # pytest fixture 配置(base_url,api_client)
├── testcases/           # 测试用例
│   ├── test_posts.py    # 正常接口测试(Get/Post/Put/Delete)
│   └── test_exceptions.py # 异常场景测试
├── utils/(工具层)
│   └── config.py        # 基础配置(BASE_URL,TIMEOUT)
│   └── logger.py        # 日志工具
├── report/              # 测试报告输出
├── requirements.txt     # 项目依赖
└── pytest.ini           # pytest 运行配置

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
