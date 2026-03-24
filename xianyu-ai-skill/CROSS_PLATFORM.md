# 跨平台使用指南

本文档说明如何在不同 AI 平台上安装和使用「闲鱼 AI 助手」Skill。

## 目录

- [OpenCode](#opencode)
- [Claude](#claude)
- [OpenClaw](#openclaw)

---

## OpenCode

### 安装方式

#### 方式一：项目内安装
```bash
cd your-project
python .opencode/skills/xianyu-ai/install.py opencode
```

#### 方式二：全局安装
```bash
python .opencode/skills/xianyu-ai/install.py --global opencode
```

### 使用方法
```
用户：帮我发一个租赁相机到闲鱼
助手：[自动识别并启动 xianyu-ai Skill]
```

---

## Claude

### 安装方式

#### 1. 克隆或复制 Skill 文件
```bash
# 方式一：复制到项目
cp -r .opencode/skills/xianyu-ai .claude/skills/xianyu-ai

# 方式二：使用安装脚本
python .claude/skills/xianyu-ai/install.py claude
```

#### 2. 创建 Claude 兼容的 SKILL.md

Claude 使用相同的格式，无需额外配置。

### 使用方法
```
用户：帮我发一个租赁相机到闲鱼
助手：[自动识别并启动 xianyu-ai Skill]
```

### Claude 特定配置

在 `data/config.json` 中配置：
```json
{
  "api": {
    "provider": "claude",
    "model": "claude-3-5-sonnet-20241022",
    "key": "your-claude-api-key"
  }
}
```

---

## OpenClaw

### 安装方式

#### 1. 复制 Skill 文件
```bash
mkdir -p skills/xianyu-ai
cp -r .opencode/skills/xianyu-ai/* skills/xianyu-ai/
```

#### 2. 配置 OpenClaw

在 `openclaw.json` 或配置文件中添加：
```json
{
  "skills": {
    "xianyu-ai": {
      "enabled": true,
      "path": "skills/xianyu-ai"
    }
  }
}
```

### 使用方法

OpenClaw 支持多种调用方式：

#### 方式一：对话触发
```
用户：/xianyu-ai 帮我发一个租赁相机到闲鱼
```

#### 方式二：自然语言
```
用户：帮我发一个租赁相机到闲鱼
助手：[自动调用 xianyu-ai Skill]
```

---

## AI Provider 切换

Skill 支持多种 AI 模型，可以在配置文件中切换：

### 配置文件：`data/config.json`

```json
{
  "api": {
    "provider": "minimax",
    "model": "MiniMax-M2-Stable",
    "key": "your-api-key"
  }
}
```

### 支持的 Provider

| Provider | 模型 | 说明 |
|----------|------|------|
| `minimax` | MiniMax-M2-Stable | 默认，推荐 |
| `deepseek` | deepseek-chat | 性价比高 |
| `openai` | gpt-4o | 国际版 |
| `claude` | claude-3-5-sonnet | 高质量 |

---

## 打包分发

### 创建分发包
```bash
python install.py --package
```

生成文件：`dist/xianyu-ai-skill.zip`

### 解压安装
```bash
# 解压到项目
unzip xianyu-ai-skill.zip -d your-project/

# 安装
cd your-project
python .opencode/skills/xianyu-ai/install.py opencode
```

---

## 常见问题

### Q: 不同平台的 Skill 格式一样吗？

A: 核心都是 `SKILL.md` 文件，格式基本相同。主要区别是目录位置：
- OpenCode: `.opencode/skills/*/SKILL.md`
- Claude: `.claude/skills/*/SKILL.md`
- OpenClaw: `skills/*/SKILL.md`

### Q: API Key 可以跨平台共用吗？

A: 可以。所有平台都支持环境变量：
```bash
export MINIMAX_API_KEY="your-key"
```

### Q: 文案库可以跨平台共用吗？

A: 可以。`data/copy_library.json` 是平台无关的，存放在 Skill 目录内。

---

## 许可证

MIT License
