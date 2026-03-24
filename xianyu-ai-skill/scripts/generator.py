#!/usr/bin/env python3
"""
闲鱼 AI 助手 - MiniMax API 调用模块
"""

import os
import json
import sys
import re
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print(json.dumps({"error": "请安装 openai 库: pip install openai"}))
    sys.exit(1)


class AIGenerator:
    """AI 文案生成器"""
    
    def __init__(self, api_key=None, model="MiniMax-M2-Stable"):
        """
        初始化 AI 生成器
        
        Args:
            api_key: MiniMax API Key
            model: 使用的模型
        """
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        if not self.api_key:
            raise ValueError("未设置 API Key，请设置 MINIMAX_API_KEY 环境变量或传入 api_key")
        
        self.model = model
        self.base_url = "https://api.minimax.chat/v1"
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def generate_copy(self, device_info, samples=None, image_features=None, prompt_path=None):
        """
        生成商品文案
        
        Args:
            device_info: 设备信息字典
                - device_type: 设备类型
                - brand_model: 品牌型号
                - specs: 配置详情
                - daily_rent: 日租金
                - deposit: 押金
            samples: 参考爆款文案列表
            image_features: 参考图片特征
            prompt_path: 提示词模板路径
        
        Returns:
            dict: 生成结果
        """
        # 加载提示词模板
        if prompt_path is None:
            prompt_path = Path(__file__).parent.parent / "prompts" / "generate_copy.md"
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # 填充设备信息
        prompt = template.format(
            device_type=device_info.get("device_type", ""),
            brand_model=device_info.get("brand_model", ""),
            specs=device_info.get("specs", ""),
            daily_rent=device_info.get("daily_rent", ""),
            deposit=device_info.get("deposit", ""),
            samples=self._format_samples(samples) if samples else "无参考案例",
            image_features=self._format_image_features(image_features) if image_features else "无参考图片"
        )
        
        # 调用 API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        
        # 解析 JSON 结果
        return self._parse_response(content)
    
    def analyze_copy(self, title, description, prompt_path=None):
        """
        分析文案特征
        
        Args:
            title: 商品标题
            description: 商品描述
            prompt_path: 提示词模板路径
        
        Returns:
            dict: 分析结果
        """
        if prompt_path is None:
            prompt_path = Path(__file__).parent.parent / "prompts" / "analyze_copy.md"
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        prompt = template.format(title=title, description=description)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800
        )
        
        content = response.choices[0].message.content
        
        return self._parse_response(content)
    
    def analyze_image(self, image_path, prompt_path=None):
        """
        分析图片特征
        
        Args:
            image_path: 图片路径
            prompt_path: 提示词模板路径
        
        Returns:
            dict: 图片特征
        """
        if prompt_path is None:
            prompt_path = Path(__file__).parent.parent / "prompts" / "analyze_image.md"
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        prompt = template.format(image_path=image_path)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        
        return self._parse_response(content)
    
    def _format_samples(self, samples):
        """格式化参考案例"""
        if not samples:
            return "无"
        
        result = []
        for i, sample in enumerate(samples[:3], 1):
            result.append(f"\n案例{i}:\n标题: {sample.get('title', '')}\n描述: {sample.get('description', '')}")
        
        return "\n".join(result)
    
    def _format_image_features(self, features):
        """格式化图片特征"""
        if not features:
            return "无"
        
        return f"参考图片风格: {features.get('style', '')}, 角度: {features.get('angle', '')}, 背景: {features.get('background', '')}"
    
    def _parse_response(self, content):
        """解析 API 响应"""
        try:
            # 尝试提取 JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"raw": content}
        except json.JSONDecodeError:
            return {"raw": content, "error": "JSON 解析失败"}


def main():
    """测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 文案生成器")
    parser.add_argument("--api-key", type=str, help="MiniMax API Key")
    parser.add_argument("--test", action="store_true", help="运行测试")
    
    args = parser.parse_args()
    
    if args.test:
        # 测试生成
        generator = AIGenerator(api_key=args.api_key)
        
        device_info = {
            "device_type": "相机",
            "brand_model": "Canon EOS R5",
            "specs": "4500万像素，8K视频",
            "daily_rent": "150",
            "deposit": "2000"
        }
        
        result = generator.generate_copy(device_info)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
