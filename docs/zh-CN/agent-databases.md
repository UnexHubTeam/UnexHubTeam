# Agent 数据库：PostgreSQL 与 MySQL

[English (primary)](../en/agent-databases.md) · [中文目录](README.md) · [模式 A 指南](agent-development-mode-a.md) · [模式 B 指南](agent-development-upload.md)

更新日期：2026-10-21

容器模式 A 与模式 B 均可为 Agent 的每位用户配置 PostgreSQL、MySQL，或同时配置两种数据库。UnexHub 在用户启动实例时准备数据库，并将连接信息注入容器环境变量，由应用**后端**读取。数据库配置统一通过 UnexHub 管理。

实际可用类型、版本和连接限制以 UnexHub 部署表单的实时目录为准。托管 SQL 独立于容器文件保存应用记录，不提供文件持久化，也不改变所选部署模式的模型访问要求。

## 本页目录

- [配置数据库要求](#database-configuration)
- [注入的环境变量](#database-environment)
- [首次创建、复用与版本变更](#database-lifecycle)
- [PostgreSQL 后端示例](#postgresql-example)
- [MySQL 后端示例](#mysql-example)
- [连接池、凭据与发布检查](#database-practices)

<a id="database-configuration"></a>
## 配置数据库要求

1. 打开 **Agent 部署配置**，选择**模式 A · 平台托管独立节点**或**模式 B · Cloudflare 容器**。
2. 在**最小资源要求**卡片中，找到算力规格设置下方的**数据库配置**。默认没有数据库；无需 SQL 的 Agent 可以保持为空。
3. 点击**添加数据库**，分别从两个下拉框选择类型和版本。当前支持 PostgreSQL 和 MySQL，每种类型最多一项；继续添加可同时使用两种数据库。Redis 和 MongoDB 尚未实现，保持禁用状态。
4. 核对页面展示的连接限制与 TLS 模式，保存运行配置。数据库要求会进入提交审核的版本快照。发布后修改数据库要求会下架并要求重新审核；普通用户启动读取已审核版本的快照，开发者自测读取工作配置。
5. 使用**新实例**测试。已经运行的实例仍使用原环境变量；修改要求后应先停止，再重新启动。

目录会展示数据库登录账号的默认最大连接数及 SSL/TLS 模式。启动时注入的 `CONNECTION_LIMIT` 是实际分配账号的上限，可能与之后变动的目录默认值不同。

目录不可用、数据库未就绪或没有可选版本时，请向 UnexHub 支持提供 Agent ID 和脱敏错误。连接信息由 UnexHub 在启动时提供，不要通过自定义环境变量填写密码。

<a id="database-environment"></a>
## 注入的环境变量

只为已选择的类型注入变量。例如仅配置 PostgreSQL 时，不会出现 `UNEX_DATABASE_MYSQL_*`。所有值均为环境变量字符串。`single` 与 `frontend-package` 拓扑注入后端容器；`split` 拓扑只给后端注入，不注入前端容器或前端构建。

| PostgreSQL 变量 | MySQL 变量 | 含义 |
| --- | --- | --- |
| `UNEX_DATABASE_POSTGRESQL_HOST` | `UNEX_DATABASE_MYSQL_HOST` | 连接主机，可能是已配置的连接池入口 |
| `UNEX_DATABASE_POSTGRESQL_PORT` | `UNEX_DATABASE_MYSQL_PORT` | 连接端口，驱动需要时转换为整数 |
| `UNEX_DATABASE_POSTGRESQL_DATABASE` | `UNEX_DATABASE_MYSQL_DATABASE` | 实际分配的物理数据库名，不要根据用户 ID 自行推算 |
| `UNEX_DATABASE_POSTGRESQL_USERNAME` | `UNEX_DATABASE_MYSQL_USERNAME` | 仅限当前数据库的登录账号 |
| `UNEX_DATABASE_POSTGRESQL_PASSWORD` | `UNEX_DATABASE_MYSQL_PASSWORD` | 该数据库账号的密码 |
| `UNEX_DATABASE_POSTGRESQL_URL` | `UNEX_DATABASE_MYSQL_URL` | 完整连接 URI，包含编码后的认证信息及 SSL 设置 |
| `UNEX_DATABASE_POSTGRESQL_SSL_MODE` | `UNEX_DATABASE_MYSQL_SSL_MODE` | 已配置的 TLS 模式：`disable`、`prefer`、`require`、`verify-ca` 或 `verify-full` |
| `UNEX_DATABASE_POSTGRESQL_CONNECTION_MODE` | `UNEX_DATABASE_MYSQL_CONNECTION_MODE` | `direct`（直连）或 `pooled`（连接池） |
| `UNEX_DATABASE_POSTGRESQL_CONNECTION_LIMIT` | `UNEX_DATABASE_MYSQL_CONNECTION_LIMIT` | 实际分配的数据库登录账号最大连接数 |

应用后端需要显式读取这些变量；注入不会自动配置 ORM。使用平台返回的主机、端口、库名和账号，不要假设默认端口或物理命名规则，并保留配置指定的 TLS 行为。部分 MySQL 客户端不能直接识别平台 URI 的 SSL 参数，因此下方示例使用独立字段和明确的 TLS 配置。

`UNEX_` 为保留前缀。不要通过**添加环境变量**手工填写上述名称。自定义环境变量以明文保存，只能放非敏感应用设置。数据库连接信息在创建容器时注入，不写入可编辑运行配置及实例、计费快照。

<a id="database-lifecycle"></a>
## 首次创建、复用与版本变更

- 首次使用时，UnexHub 为当前用户的当前 Agent 按所选类型分别准备独立数据库和专属登录账号。
- 数据库准备先于算力预扣及容器创建。准备失败不会进入这些步骤；如果先成功创建了一种数据库、另一种失败，已创建的部分会保留供重试。
- 同一**用户 × Agent × 数据库类型**重复启动、并发启动或更新镜像时复用原数据库；不同用户或不同 Agent 使用不同数据库和账号。新会话不会自动得到一个空库。
- 每个数据库有独立 SQL 登录账号。Agent 不会自动取得其他 Agent 数据库或其他用户数据的访问权限，未来 Agent 联动需要平台明确授权。
- 改选版本不会自动升级、迁移或重建已有数据库。所选版本与实际分配服务器版本不一致时会拒绝启动。迁移需与平台运维协调，应用表结构应兼容发布和回滚要求。
- 停止容器、移除数据库要求或删除 Agent 均不会自动删除远端数据库，不能将这些操作描述为数据已擦除；保留与数据库回收需要单独管理。

SQL 数据独立于容器磁盘持久保存。容器文件仍是临时数据，托管 SQL 不提供 D1/R2 文件工作区或文件上传下载代理。

## 运行后端示例

在 Agent 后端使用 Python 3.10+，将以下依赖加入项目，发布时锁定解析出的具体版本：

```bash
python -m pip install 'psycopg[binary]>=3.2,<4' 'PyMySQL[rsa]>=1.1,<1.2'
```

选择对应数据库后，在平台启动的测试容器内运行示例。示例会创建 `agent_example_notes` 表，并插入或更新 `id=1` 的记录，应使用可丢弃的测试 Agent/数据库。示例一次打开一个连接，使用参数化 SQL 写入并提交、读取验证，再关闭连接；连接凭据来自 UnexHub 注入的环境变量。

<a id="postgresql-example"></a>
## PostgreSQL 后端示例

[下载 `postgresql_example.py`](../../examples/agent-databases/postgresql_example.py)，在测试容器中执行 `python postgresql_example.py`。注入的 URI 已保留凭据转义和 `sslmode`。Psycopg 连接上下文在成功时提交、出错时回滚，并关闭连接。用法见 [Psycopg 官方说明](https://www.psycopg.org/psycopg3/docs/basic/usage.html)。

```python
"""Backend-only PostgreSQL example. Run in a disposable Agent test database."""

import os

import psycopg


def required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing {name}; enable the database and restart the instance")
    return value


def main():
    options = {"connect_timeout": 5}
    if os.environ.get("DATABASE_CA_FILE"):
        options["sslrootcert"] = os.environ["DATABASE_CA_FILE"]

    # The injected URL already includes encoded credentials and sslmode.
    with psycopg.connect(required("UNEX_DATABASE_POSTGRESQL_URL"), **options) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS agent_example_notes "
                "(id integer PRIMARY KEY, body text NOT NULL)"
            )
            cursor.execute(
                "INSERT INTO agent_example_notes (id, body) VALUES (%s, %s) "
                "ON CONFLICT (id) DO UPDATE SET body = EXCLUDED.body",
                (1, "Hello from this user's Agent"),
            )
            cursor.execute("SELECT body FROM agent_example_notes WHERE id = %s", (1,))
            if cursor.fetchone() != ("Hello from this user's Agent",):
                raise RuntimeError("Database read-back failed")
    # The context commits on success, rolls back on error, and closes the connection.
    print("PostgreSQL write/read succeeded.")


if __name__ == "__main__":
    try:
        main()
    except (psycopg.Error, OSError, ValueError, RuntimeError):
        # Raw driver exceptions can contain connection details. Sanitize user-facing errors.
        raise SystemExit(
            "PostgreSQL operation failed; check database configuration, TLS and connectivity."
        ) from None
```

需要用私有 CA 验证证书时，可在镜像中放入公开 CA 证书，并配置 `DATABASE_CA_FILE=/app/certs/database-ca.pem` 这样的非敏感应用设置。它是**应用自行选择的配置，不是平台注入变量**。`verify-full` 校验证书链及主机名；仅使用 `require` 不保证服务器身份验证。模式说明见 [PostgreSQL SSL 文档](https://www.postgresql.org/docs/current/libpq-ssl.html)。

<a id="mysql-example"></a>
## MySQL 后端示例

[下载 `mysql_example.py`](../../examples/agent-databases/mysql_example.py)，在测试容器中执行 `python mysql_example.py`。示例将注入的 SSL 模式转换为 `ssl.SSLContext`，不假设驱动能直接使用原始 URL。参数说明见 [PyMySQL 官方连接文档](https://pymysql.readthedocs.io/en/latest/modules/connections.html)。

```python
"""Backend-only MySQL example. Run in a disposable Agent test database."""

import os
import ssl

import pymysql


def required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing {name}; enable the database and restart the instance")
    return value


def mysql_tls(mode):
    if mode == "disable":
        return None
    if mode not in {"prefer", "require", "verify-ca", "verify-full"}:
        raise RuntimeError("Unsupported database TLS mode")
    context = ssl.create_default_context(cafile=os.environ.get("DATABASE_CA_FILE"))
    if mode in {"prefer", "require"}:
        # These configured modes do not verify server certificates.
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    elif mode == "verify-ca":
        context.check_hostname = False
    return context


def main():
    prefix = "UNEX_DATABASE_MYSQL_"
    mode = required(prefix + "SSL_MODE")
    with pymysql.connect(
        host=required(prefix + "HOST"),
        port=int(required(prefix + "PORT")),
        user=required(prefix + "USERNAME"),
        password=required(prefix + "PASSWORD"),
        database=required(prefix + "DATABASE"),
        charset="utf8mb4",
        connect_timeout=5,
        read_timeout=15,
        write_timeout=15,
        autocommit=False,
        local_infile=False,
        ssl=mysql_tls(mode),
        ssl_disabled=(mode == "disable"),
    ) as conn:
        # PyMySQL 1.1 can fall back when a server does not advertise TLS.
        # Fail closed when the configured mode requires TLS.
        if mode not in {"disable", "prefer"} and not getattr(conn, "_secure", False):
            raise RuntimeError("The database connection requires TLS")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS agent_example_notes "
                    "(id integer PRIMARY KEY, body text NOT NULL)"
                )
                cursor.execute(
                    "INSERT INTO agent_example_notes (id, body) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE body = %s",
                    (1, "Hello from this user's Agent", "Hello from this user's Agent"),
                )
                cursor.execute("SELECT body FROM agent_example_notes WHERE id = %s", (1,))
                if cursor.fetchone() != ("Hello from this user's Agent",):
                    raise RuntimeError("Database read-back failed")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    # MySQL DDL may commit independently; migrations need their own recovery strategy.
    print("MySQL write/read succeeded.")


if __name__ == "__main__":
    try:
        main()
    except (pymysql.Error, OSError, ValueError, RuntimeError):
        raise SystemExit(
            "MySQL operation failed; check database configuration, TLS and connectivity."
        ) from None
```

示例遵循已配置的模式：`disable` 关闭 TLS，`prefer` 在支持时尝试 TLS，`require` 要求加密，`verify-ca` 进一步校验证书链，`verify-full` 再校验主机名。本 MySQL 示例的 `prefer` 和 `require` 不校验证书。启用验证且使用私有 CA 时设置 `DATABASE_CA_FILE`；证书异常应由平台运维修复，不应降低已配置的模式。`_secure` 检查使用 PyMySQL 1.1 的属性，防止必需 TLS 时静默回退；更换或升级驱动时需重新验证。MySQL DDL 可能独立提交，表结构迁移需要自己的恢复方案。

<a id="database-practices"></a>
## 连接池、凭据与发布检查

生产后端应根据对应类型的 `CONNECTION_LIMIT` 限制连接池。计算使用该“用户 × Agent”数据库账号的**所有进程和容器**连接数，包括工作进程与迁移任务，并留出余量，不能让每个进程都占满上限。退出时关闭连接、设置超时，对容量不足限制重试。使用连接池入口时，先核对 `CONNECTION_MODE`，再选择依赖连接会话状态的 SQL 功能。

数据库密码与 URL 对容器及其依赖可读，应仅保留在后端进程中，避免记录原始驱动错误，不得通过配置接口、前端打包、浏览器存储、问题报告或页面 URL 暴露。

发布前验证写入读取、停止再启动后的数据保留、镜像更新后的复用，以及两个用户之间、两个 Agent 之间的隔离。对缺少变量、TLS 失败和连接数不足验证脱敏错误。同时完成所选部署模式的发布检查：[模式 A](agent-development-mode-a.md#section-10)或[模式 B](agent-development-upload.md#section-10)。
