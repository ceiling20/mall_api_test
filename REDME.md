#接口自动化测试项目
基于pytest + requests 的接口测试项目，测试JSONPlaceholder开放API

##项目结构
api_test/
├── conftest.py          # pytest fixture 配置
├── testcases/           # 测试用例
│   ├── test_posts.py    # 正常接口测试
│   └── test_exceptions.py # 异常场景测试
├── utils/
│   └── config.py        # 基础配置
└── report/              # 测试报告输出

##运行方式
```bash
# 安装依赖
pip install pytest requests pytest-html

# 运行测试
pytest testcases/ -v

#生成html报告
pytest testcases/ -v --html=report/report.html