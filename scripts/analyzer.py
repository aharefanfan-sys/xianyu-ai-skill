#!/usr/bin/env python3
"""
闲鱼 AI 助手 - 文案分析模块
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from generator import AIGenerator


class CopyAnalyzer:
    """爆款文案分析器"""
    
    def __init__(self, api_key=None):
        """初始化分析器"""
        self.generator = AIGenerator(api_key=api_key)
    
    def analyze(self, title, description):
        """
        分析文案特征
        
        Args:
            title: 商品标题
            description: 商品描述
        
        Returns:
            dict: 分析结果
        """
        result = self.generator.analyze_copy(title, description)
        
        # 添加时间戳
        result["analyzed_at"] = datetime.now().isoformat()
        
        return result
    
    def extract_features(self, title, description):
        """
        提取文案特征（简化版）
        
        Args:
            title: 商品标题
            description: 商品描述
        
        Returns:
            dict: 特征字典
        """
        result = self.analyze(title, description)
        
        # 返回关键特征
        return {
            "title_keywords": result.get("title_features", {}).get("keywords", []),
            "description_style": result.get("description_features", {}).get("style", ""),
            "tags": result.get("tags", []),
            "success_factors": result.get("success_factors", ""),
            "full_analysis": result
        }


def main():
    """测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="文案分析器")
    parser.add_argument("--api-key", type=str, help="MiniMax API Key")
    parser.add_argument("--title", type=str, required=True, help="商品标题")
    parser.add_argument("--description", type=str, required=True, help="商品描述")
    
    args = parser.parse_args()
    
    analyzer = CopyAnalyzer(api_key=args.api_key)
    result = analyzer.analyze(args.title, args.description)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
