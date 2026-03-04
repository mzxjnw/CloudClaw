# CloudClaw 本地智能助手
一个基于 FastAPI 开发的本地智能工具调用助手，支持文件操作、数值计算、IM 消息接入（企微/钉钉/飞书），内置权限控制和内容安全审计。

## 📋 项目结构
CloudClaw/├── backend/ # 后端核心代码│ ├── core/ # 核心模块（工具基类、执行器）│ ├── gateway/ # 第三方接口网关（预留）│ ├── modules/ # 业务模块（IM、工具）│ ├── security/ # 安全模块（加密、权限、审计）│ ├── storage/ # 数据存储（数据库）│ ├── infrastructure/ # 基础设施（日志、中间件）│ ├── api/ # API 路由（预留）│ ├── tests/ # 测试用例（预留）│ └── main.py # 后端启动入口├── index.html # 简单前端页面└── README.md # 项目说明
## 🚀 快速启动
### 1. 环境准备
- 安装 Python 3.8+
- 安装依赖：
  ```bash
  pip install fastapi uvicorn cryptography sqlalchemy
 启动后端服务
cd backend
python main.py
服务启动后访问：http://localhost:8000
健康检查：http://localhost:8000/health
3. 访问前端页面
直接双击打开 index.html 文件即可。
🔧 核心功能
✅ 文件操作：读取 / 写入本地文本文件（带权限控制）
✅ 基础计算：数值加减乘除、字符串拼接、列表筛选
✅ 安全审计：内置敏感词检测、权限校验
✅ IM 适配：支持企微 / 钉钉 / 飞书消息解析和回复（模拟实现）
✅ 数据加密：本地敏感数据加密存储
📝 注意事项
首次启动会自动创建数据库文件和加密密钥文件（位于 backend/data/ 目录）
离线模式下仅做本地敏感词检测，不调用云端接口
普通用户仅拥有文件读取权限，管理员可写入文件