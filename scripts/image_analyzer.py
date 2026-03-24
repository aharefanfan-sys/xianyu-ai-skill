#!/usr/bin/env python3
"""
闲鱼 AI 助手 - 图片分析模块
"""

import os
import json
import sys
import base64
import shutil
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from generator import AIGenerator


class ImageAnalyzer:
    """商品图片分析器"""
    
    SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".webp"]
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    
    def __init__(self, api_key=None, storage_dir=None):
        """
        初始化图片分析器
        
        Args:
            api_key: MiniMax API Key
            storage_dir: 图片存储目录
        """
        self.generator = AIGenerator(api_key=api_key)
        
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "data" / "images"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze(self, image_path):
        """
        分析图片特征
        
        Args:
            image_path: 图片路径
        
        Returns:
            dict: 图片特征
        """
        image_path = Path(image_path)
        
        # 验证图片
        if not image_path.exists():
            return {"error": f"图片不存在: {image_path}"}
        
        if image_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            return {"error": f"不支持的图片格式: {image_path.suffix}"}
        
        if image_path.stat().st_size > self.MAX_SIZE:
            return {"error": f"图片过大: {image_path.stat().st_size / 1024 / 1024:.2f}MB"}
        
        # 调用 AI 分析
        result = self.generator.analyze_image(str(image_path))
        
        # 添加元数据
        result["analyzed_at"] = datetime.now().isoformat()
        result["original_path"] = str(image_path)
        result["file_size"] = image_path.stat().st_size
        result["file_name"] = image_path.name
        
        return result
    
    def save_and_analyze(self, source_path, dest_name=None):
        """
        保存图片并分析
        
        Args:
            source_path: 源图片路径
            dest_name: 目标文件名
        
        Returns:
            dict: 分析结果和存储路径
        """
        source_path = Path(source_path)
        
        if not source_path.exists():
            return {"error": f"源图片不存在: {source_path}"}
        
        # 生成目标文件名
        if dest_name is None:
            dest_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{source_path.name}"
        
        dest_path = self.storage_dir / dest_name
        
        # 复制图片
        shutil.copy2(source_path, dest_path)
        
        # 分析图片
        result = self.analyze(dest_path)
        
        # 添加存储路径
        result["stored_path"] = str(dest_path)
        
        return result
    
    def analyze_and_link_to_copy(self, image_path, copy_id, library_manager):
        """
        分析图片并关联到文案
        
        Args:
            image_path: 图片路径
            copy_id: 文案 ID
            library_manager: 文案库管理器
        
        Returns:
            dict: 分析结果
        """
        # 分析图片
        analysis = self.analyze(image_path)
        
        if "error" in analysis:
            return analysis
        
        # 更新文案库
        library_manager.add_image_to_sample(
            sample_id=copy_id,
            image_path=analysis["stored_path"],
            image_features=analysis
        )
        
        return analysis


def main():
    """测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="图片分析器")
    parser.add_argument("--api-key", type=str, help="MiniMax API Key")
    parser.add_argument("--image", type=str, required=True, help="图片路径")
    
    args = parser.parse_args()
    
    analyzer = ImageAnalyzer(api_key=args.api_key)
    result = analyzer.analyze(args.image)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
