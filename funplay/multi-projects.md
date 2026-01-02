# Multi-Project Google Cloud Management with Multi-Terminal

## 📋 项目概述

这个项目提供了在多终端环境中管理多个 Google Cloud 项目的解决方案。通过 Docker 容器化的 Google Cloud SDK，你可以在不同的终端窗口中同时访问和管理不同的 GCP 项目。

## 🎯 主要特性

- ✅ **多项目并行管理**：在不同终端中同时操作不同 GCP 项目
- ✅ **环境隔离**：每个终端有独立的认证和配置
- ✅ **快速切换**：无需重复认证，快速在不同项目间切换
- ✅ **持久化配置**：容器重启后配置不丢失
- ✅ **统一工具链**：所有终端使用相同版本的 Google Cloud SDK

## 📁 项目结构

```
gcloud-multi-terminal/
├── README.md                    # 本文档
├── docker-compose.yml           # 多终端 Docker Compose 配置
├── Dockerfile                   # 自定义 Google Cloud SDK 镜像
├── configs/                     # 配置文件目录
│   ├── project-a/              # 项目A配置
│   │   ├── .config/           # GCloud 配置目录
│   │   ├── credentials.json   # 服务账号密钥
│   │   └── gcloud.env         # 环境变量
│   ├── project-b/              # 项目B配置
│   └── shared/                 # 共享配置
├── scripts/                     # 工具脚本
│   ├── setup-projects.sh       # 项目初始化脚本
│   ├── start-terminal.sh       # 启动终端脚本
│   └── switch-project.sh       # 项目切换脚本
├── terminals/                   # 终端配置文件
│   ├── terminal-a/            # 终端A工作区
│   ├── terminal-b/            # 终端B工作区
│   └── workspace/             # 共享工作区
└── docs/                       # 文档
    ├── gcloud-cheatsheet.md    # GCloud 命令速查
    └── troubleshooting.md      # 故障排除
```

## 🚀 快速开始

### 先决条件

1. **Docker** 和 **Docker Compose**
   ```bash
   # 验证安装
   docker --version
   docker-compose --version
   ```

2. **终端工具**（至少2个）
   - macOS: iTerm2, Terminal, Warp
   - Windows: Windows Terminal, PowerShell, Cmder
   - Linux: GNOME Terminal, Konsole, Terminator

3. **Google Cloud 服务账号密钥**
   - 为每个项目创建服务账号
   - 下载 JSON 格式的密钥文件

### 安装步骤

#### 1. 克隆/创建项目
```bash
mkdir gcloud-multi-terminal
cd gcloud-multi-terminal
```

#### 2. 创建配置文件
```bash
# 创建配置目录
mkdir -p configs/project-a/.config/gcloud
mkdir -p configs/project-b/.config/gcloud
mkdir -p terminals/{terminal-a,terminal-b,workspace}
mkdir scripts
```

#### 3. 准备服务账号密钥
将你的服务账号密钥文件放到对应目录：
```bash
# 项目A
cp ~/Downloads/project-a-key.json configs/project-a/credentials.json

# 项目B
cp ~/Downloads/project-b-key.json configs/project-b/credentials.json
```

#### 4. 创建 Docker Compose 配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  # 终端A - 项目A
  terminal-project-a:
    image: google/cloud-sdk:latest
    container_name: gcloud-project-a
    hostname: project-a-terminal
    volumes:
      - ./configs/project-a/.config/gcloud:/root/.config/gcloud
      - ./configs/project-a/credentials.json:/secrets/key.json:ro
      - ./terminals/terminal-a:/workspace
      - ./terminals/shared:/shared
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/secrets/key.json
      - CLOUDSDK_CORE_PROJECT=your-project-a-id
      - CLOUDSDK_COMPUTE_ZONE=us-central1-a
      - TERM=xterm-256color
    stdin_open: true
    tty: true
    command: /bin/bash
    networks:
      - gcloud-network

  # 终端B - 项目B
  terminal-project-b:
    image: google/cloud-sdk:latest
    container_name: gcloud-project-b
    hostname: project-b-terminal
    volumes:
      - ./configs/project-b/.config/gcloud:/root/.config/gcloud
      - ./configs/project-b/credentials.json:/secrets/key.json:ro
      - ./terminals/terminal-b:/workspace
      - ./terminals/shared:/shared
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/secrets/key.json
      - CLOUDSDK_CORE_PROJECT=your-project-b-id
      - CLOUDSDK_COMPUTE_ZONE=us-east1-b
      - TERM=xterm-256color
    stdin_open: true
    tty: true
    command: /bin/bash
    networks:
      - gcloud-network

  # 可选：共享工作区
  terminal-shared:
    image: google/cloud-sdk:latest
    container_name: gcloud-shared
    hostname: shared-terminal
    volumes:
      - ./terminals/workspace:/workspace
      - ./terminals/shared:/shared
    stdin_open: true
    tty: true
    command: /bin/bash
    networks:
      - gcloud-network

networks:
  gcloud-network:
    driver: bridge
```

#### 5. 创建启动脚本
```bash
# scripts/start-terminals.sh
#!/bin/bash

echo "启动多项目 Google Cloud 终端..."

# 启动所有终端容器
docker-compose up -d

echo -e "\n✅ 终端已启动:"
echo "======================================"
echo "1. 项目A终端:"
echo "   docker exec -it gcloud-project-a bash"
echo "   项目ID: your-project-a-id"
echo "   工作区: terminals/terminal-a"
echo ""
echo "2. 项目B终端:"
echo "   docker exec -it gcloud-project-b bash"
echo "   项目ID: your-project-b-id"
echo "   工作区: terminals/terminal-b"
echo ""
echo "3. 共享终端:"
echo "   docker exec -it gcloud-shared bash"
echo "   工作区: terminals/workspace"
echo "======================================"
echo -e "\n使用以下命令进入不同终端:"
echo "  ./scripts/connect-project-a.sh"
echo "  ./scripts/connect-project-b.sh"
echo "  ./scripts/connect-shared.sh"
```

#### 6. 创建连接脚本
```bash
# scripts/connect-project-a.sh
#!/bin/bash
echo "连接到 项目A 终端..."
docker exec -it gcloud-project-a bash
```

```bash
# scripts/connect-project-b.sh
#!/bin/bash
echo "连接到 项目B 终端..."
docker exec -it gcloud-project-b bash
```

```bash
# scripts/connect-shared.sh
#!/bin/bash
echo "连接到 共享终端..."
docker exec -it gcloud-shared bash
```

#### 7. 设置权限
```bash
chmod +x scripts/*.sh
```

## 💻 使用方法

### 基本工作流

1. **启动所有终端**：
   ```bash
   ./scripts/start-terminals.sh
   ```

2. **在终端A中连接项目A**：
   ```bash
   ./scripts/connect-project-a.sh
   ```
   在容器内验证：
   ```bash
   gcloud config list
   gcloud projects list
   ```

3. **在终端B中连接项目B**：
   打开新的终端窗口：
   ```bash
   ./scripts/connect-project-b.sh
   ```

4. **同时在两个终端中操作**：
   - 终端A：操作项目A的资源
   - 终端B：操作项目B的资源
   - 互不干扰

### 示例场景

**场景1：同时在两个项目中创建 Compute Engine 实例**

在终端A（项目A）：
```bash
# 终端A
gcloud compute instances create instance-a \
  --zone=us-central1-a \
  --machine-type=e2-medium
```

在终端B（项目B）：
```bash
# 终端B
gcloud compute instances create instance-b \
  --zone=us-east1-b \
  --machine-type=e2-small
```

**场景2：监控两个项目的资源**

在终端A查看项目A：
```bash
gcloud compute instances list
gcloud container clusters list
```

在终端B查看项目B：
```bash
gcloud compute instances list
gcloud sql instances list
```

## 🔧 高级配置

### 自定义 Docker 镜像
```dockerfile
# Dockerfile.custom-gcloud
FROM google/cloud-sdk:latest

# 安装额外工具
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    htop \
    tree \
    jq \
    curl \
    wget \
    git \
    kubectl \
    terraform

# 设置别名
RUN echo "alias ll='ls -la'" >> ~/.bashrc && \
    echo "alias k='kubectl'" >> ~/.bashrc

# 创建工作目录
WORKDIR /workspace
```

### 多区域配置
```yaml
# docker-compose.regions.yml
services:
  terminal-us:
    environment:
      - CLOUDSDK_COMPUTE_ZONE=us-central1-a
      - CLOUDSDK_COMPUTE_REGION=us-central1
      
  terminal-eu:
    environment:
      - CLOUDSDK_COMPUTE_ZONE=europe-west1-b
      - CLOUDSDK_COMPUTE_REGION=europe-west1
      
  terminal-asia:
    environment:
      - CLOUDSDK_COMPUTE_ZONE=asia-northeast1-a
      - CLOUDSDK_COMPUTE_REGION=asia-northeast1
```

### 项目切换脚本
```bash
# scripts/switch-project.sh
#!/bin/bash

PROJECT_ID=$1
TERMINAL_NAME=$2

if [ -z "$PROJECT_ID" ]; then
    echo "使用方法: $0 <project-id> [terminal-name]"
    exit 1
fi

TERMINAL_NAME=${TERMINAL_NAME:-"gcloud-shared"}

echo "切换项目到: $PROJECT_ID"

# 在容器内切换
docker exec $TERMINAL_NAME bash -c "
  gcloud config set project $PROJECT_ID
  echo '当前项目:'
  gcloud config get-value project
"
```

## 📊 管理命令参考

### 容器管理
```bash
# 启动所有终端
docker-compose up -d

# 查看状态
docker-compose ps

# 停止所有终端
docker-compose down

# 重启特定终端
docker-compose restart terminal-project-a

# 查看日志
docker-compose logs terminal-project-a
```

### 项目验证
```bash
# 验证认证
gcloud auth list

# 验证当前项目
gcloud config get-value project

# 验证可用项目
gcloud projects list

# 测试权限
gcloud iam service-accounts list
```

## 🎨 多终端工具推荐

### 推荐的终端工具组合

1. **iTerm2 + tmux** (macOS)
   ```bash
   # 安装 tmux
   brew install tmux
   
   # 水平分屏
   tmux split-window -h
   
   # 垂直分屏
   tmux split-window -v
   ```

2. **Windows Terminal + PowerShell**
   - 支持多标签页
   - 可自定义配置文件

3. **Terminator** (Linux)
   ```bash
   sudo apt install terminator
   # 支持网格布局
   ```

### 屏幕布局示例
```
┌──────────────────────────────────────┐
│        终端工具 (iTerm2/Terminator)   │
├──────────────┬───────────────────────┤
│  终端A       │       终端B           │
│  项目A       │       项目B           │
│  us-central1 │       us-east1        │
├──────────────┴───────────────────────┤
│           共享终端/监控               │
└──────────────────────────────────────┘
```

## 🔍 故障排除

### 常见问题

1. **认证失败**
   ```bash
   # 重新激活服务账号
   docker exec terminal-name gcloud auth activate-service-account \
     --key-file=/secrets/key.json
   ```

2. **项目不可见**
   ```bash
   # 检查权限
   docker exec terminal-name gcloud projects list --filter="projectId:your-project-id"
   
   # 可能需要添加 billing
   gcloud beta billing projects link your-project-id \
     --billing-account=XXXXXX-XXXXXX-XXXXXX
   ```

3. **网络问题**
   ```bash
   # 测试连接
   docker exec terminal-name curl -I https://cloud.google.com
   
   # 如果需要代理
   export https_proxy=http://proxy:port
   ```

### 日志查看
```bash
# 查看容器日志
docker-compose logs -f terminal-project-a

# 查看 GCloud 详细日志
gcloud --log-http info
```

## 📈 扩展功能

### 添加更多项目
```bash
# 1. 创建新项目配置目录
mkdir -p configs/project-c/.config/gcloud

# 2. 添加密钥
cp new-key.json configs/project-c/credentials.json

# 3. 更新 docker-compose.yml
# 添加新的服务定义
```

### 集成其他工具
```yaml
# 在 Docker Compose 中添加
services:
  terraform-project-a:
    image: hashicorp/terraform:latest
    volumes:
      - ./terraform/project-a:/workspace
      - ./configs/project-a/credentials.json:/key.json
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/key.json
    command: terraform init
```

### 自动化脚本
```bash
# scripts/deploy-all.sh
#!/bin/bash
# 在所有项目中执行相同操作

PROJECTS=("project-a" "project-b" "project-c")

for project in "${PROJECTS[@]}"; do
  echo "在 $project 中部署..."
  docker exec gcloud-$project bash -c "
    gcloud app deploy app.yaml --quiet
  "
done
```

## 📚 学习资源

- https://cloud.google.com/sdk/docs
- https://docs.docker.com/compose/
- https://cloud.google.com/architecture/managing-multiple-projects

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📄 许可证

MIT License

---

**提示**：定期更新你的服务账号密钥，并确保密钥文件安全保存。