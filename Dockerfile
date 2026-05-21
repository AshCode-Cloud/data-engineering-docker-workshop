# 使用 Python 3.13 轻量版
FROM python:3.13-slim

# 安装 uv 环境管理工具
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置容器工作目录
WORKDIR /app

# 拷贝环境配置（假设这些文件在根目录）
COPY pipeline/pyproject.toml pipeline/uv.lock ./

# 同步环境依赖
RUN uv sync --frozen --no-dev

# 关键：拷贝 pipeline 文件夹下的脚本到容器
COPY pipeline/ingest_data.py .

# 运行脚本
ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]