# GitRepoProject

## 项目简介

GitRepoProject 是一个基于 FastAPI 的后端项目，目标是把 GitHub 仓库信息同步到本地 MySQL 数据库中。

当前流程如下：

1. 输入 GitHub 用户名
2. 读取仓库数据
3. 将输入数据与本地数据库中的记录进行比对
4. 新增本地不存在的仓库
5. 更新已经存在但内容发生变化的仓库
6. 对最新数据中不存在的仓库做删除标记

## 技术栈

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- Requests
- Uvicorn

## 文件结构

```text
GitRepoProject/
|-- .gitignore
|-- README.md
|-- READMECN.md
|-- requirements.txt
`-- app/
    |-- main.py
    |-- core/
    |   `-- db_table.py
    |-- mock_data/
    |   `-- gitRepo_mock_data.py
    |-- repositories/
    |   `-- repositories.py
    |-- schema/
    |   |-- database.py
    |   `-- model.py
    `-- service/
        |-- dataSync_service.py
        `-- github_service.py
```

## 主要文件说明

- `app/main.py`
  FastAPI 入口文件，负责创建数据表、管理数据库连接，并暴露同步接口。

- `app/service/dataSync_service.py`
  核心同步逻辑，负责把输入仓库数据和本地数据库数据做比对。

- `app/service/github_service.py`
  GitHub API 抓取工具函数，负责读取仓库数据。

- `app/repositories/repositories.py`
  数据访问层，负责读取和更新 `github_repos` 表数据。

- `app/core/db_table.py`
  SQLAlchemy 数据表模型定义。

- `app/schema/database.py`
  数据库引擎和 Session 配置。

- `app/mock_data/gitRepo_mock_data.py`
  本地同步验证时使用的 mock 仓库数据。

## API 接口

### 同步接口

```text
GET /repo_name?github_user=<username>
```

接口行为：

- 查询该 GitHub 用户当前在本地数据库中的记录
- 读取仓库数据
- 以 `repo_full_name` 作为比对键
- 对新仓库执行新增
- 对 stars、forks、description、language 等变化执行更新
- 对新数据中不存在的仓库标记 `is_deleted = True`

## 数据表设计

### `github_repos`

主要字段：

- `id`
- `github_user`
- `repo_name`
- `repo_full_name`
- `description`
- `language`
- `forks`
- `repo_url`
- `stars`
- `is_deleted`
- `updated_at`

## 启动方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备 MySQL

当前项目使用的数据库配置定义在：

- `app/schema/database.py`

当前连接字符串为：

```text
mysql+pymysql://root:tomato123@localhost/test_db
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload
```

### 4. 打开接口文档

```text
http://127.0.0.1:8000/docs
```

## 说明

- 这个项目当前重点是本地同步和差分更新逻辑。
- 仓库删除采用软删除方式，通过 `is_deleted` 字段进行标记。
