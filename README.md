# 闲鱼 AI 商品发布助手

闲鱼 AI 商品发布助手是一个基于 MiniMax 大模型的智能文案生成系统，帮助租赁商家自动生成符合闲鱼流量规则的商品文案。

## 功能特性

- 📥 **设备信息输入**：支持输入设备类型、品牌型号、配置、租金等信息
- 🧠 **爆款文案学习**：上传爆款文案，AI 自动分析特征并保存
- 🖼️ **爆款图片学习**：上传爆款商品图片，AI 分析拍摄风格和构图
- ✨ **智能文案生成**：基于学习到的特征，生成高转化率商品文案
- 📤 **闲鱼 API 发布**：集成闲鱼开放平台 API，支持自动发布
- 🔄 **反馈迭代优化**：根据用户反馈持续优化文案效果

## 目录结构

```
.opencode/skills/xianyu-ai/
├── SKILL.md                     # Skill 定义
├── prompts/                     # 提示词模板
│   ├── generate_copy.md         # 文案生成提示词
│   ├── analyze_copy.md          # 文案分析提示词
│   └── analyze_image.md         # 图片分析提示词
├── scripts/                     # 核心脚本
│   ├── generator.py             # AI 生成器
│   ├── analyzer.py              # 文案分析器
│   ├── image_analyzer.py        # 图片分析器
│   ├── library.py               # 文案库管理
│   ├── config.py                # 配置管理
│   ├── publisher.py             # 闲鱼发布
│   └── traffic_rules.json       # 流量规则
├── data/                        # 数据目录
│   ├── config.json              # 运行时配置
│   ├── copy_library.json        # 爆款文案库
│   └── images/                  # 爆款图片存储
└── README.md                    # 本文档
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- openai 库

```bash
pip install openai
```

### 2. 配置 API Key

**方式一：环境变量**

```bash
export MINIMAX_API_KEY="your-api-key"
```

**方式二：配置文件**

编辑 `data/config.json`，填写 API Key：

```json
{
  "api": {
    "key": "your-api-key"
  }
}
```

### 3. 使用示例

#### 生成文案

```python
from scripts.generator import AIGenerator
from scripts.library import CopyLibrary

# 初始化
generator = AIGenerator()
library = CopyLibrary()

# 获取参考样本
samples = library.get_similar_samples("数码相机", count=3)

# 设备信息
device_info = {
    "device_type": "相机",
    "brand_model": "Canon EOS R5",
    "specs": "4500万像素，8K视频",
    "daily_rent": "150",
    "deposit": "2000"
}

# 生成文案
result = generator.generate_copy(device_info, samples)
print(result)
```

#### 上传爆款文案

```python
from scripts.analyzer import CopyAnalyzer
from scripts.library import CopyLibrary

analyzer = CopyAnalyzer()
library = CopyLibrary()

# 分析文案
analysis = analyzer.analyze(
    title="Canon EOS R5 日租99 押金499 性价比之王",
    description="..."
)

# 添加到文案库
sample_id = library.add_sample(
    category="数码相机",
    title="Canon EOS R5 日租99 押金499 性价比之王",
    description="...",
    features=analysis.get("tags", []),
    source="manual",
    likes=328
)
```

#### 上传爆款图片

```python
from scripts.image_analyzer import ImageAnalyzer
from scripts.library import CopyLibrary

analyzer = ImageAnalyzer()
library = CopyLibrary()

# 分析图片
result = analyzer.save_and_analyze("path/to/image.jpg")

# 关联到文案
analyzer.analyze_and_link_to_copy(
    image_path="path/to/image.jpg",
    copy_id="sample-id",
    library_manager=library
)
```

## 流量规则

系统集成了闲鱼官方流量规则，包括：

### ✅ 鼓励内容

- 标题包含：日租、押金、包邮、7天无理由、24小时发货、质保
- 正文突出：服务保障、性价比、专业

### ❌ 禁止内容

- 站外引流（微信、QQ、vx、私聊）
- 虚假价格（0.01元等）
- 堆砌无关关键词

详见 `scripts/traffic_rules.json`

## 数据管理

### 文案库操作

```python
from scripts.library import CopyLibrary

library = CopyLibrary()

# 获取统计
stats = library.get_stats()

# 获取样本
samples = library.get_samples(category="数码相机")

# 导出数据
library.export_data("backup.json")

# 导入数据
library.import_data("backup.json")
```

### 图片管理

爆款图片存储在 `data/images/` 目录，按时间戳命名。

## 注意事项

1. API Key 安全：请勿将包含 Key 的配置文件提交到版本控制
2. 图片格式：支持 JPG/PNG，建议 800x800 以上
3. 定期备份：建议定期备份文案库 `data/copy_library.json`

## 后期功能规划

- [ ] 自动抓取同类目热门商品
- [ ] 热门关键词提取
- [ ] 多平台支持（转转、咸鱼同城）
- [ ] 数据统计和效果分析

## 许可证

MIT
