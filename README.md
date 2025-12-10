# MyFastApi

一个基于FastAPI的数据库测试项目，用于连接和测试SQL Server数据库。

## 功能特性

- 使用FastAPI框架构建RESTful API
- 连接SQL Server数据库
- 提供数据库测试工具
- 支持数据库操作和查询

## 安装说明

### 克隆项目

```bash
git clone https://github.com/yourusername/MyFastApi.git
cd MyFastApi
```

### 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 安装依赖

#### 生产环境

```bash
pip install -r requirements.txt
```

#### 开发环境

```bash
pip install -r requirements-dev.txt
```

### 安装项目

```bash
pip install -e .
```

## 使用方法

### 运行API服务

```bash
uvicorn routes.app:app --reload
```

### 数据库测试

```bash
# 列出所有数据库
python dbtest/list_databases.py

# 测试数据库连接
python dbtest/test_db_connection.py

# 检查表结构
python dbtest/check_tables.py
```

## 项目结构

```
MyFastApi/
├── dbtest/           # 数据库测试脚本
├── models/           # 数据模型
├── routes/           # API路由
├── static/           # 静态文件
├── requirements.txt  # 生产环境依赖
├── requirements-dev.txt  # 开发环境依赖
├── setup.py          # 项目安装配置
└── README.md         # 项目说明
```

## 许可证

MIT License
