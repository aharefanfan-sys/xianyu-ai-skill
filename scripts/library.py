#!/usr/bin/env python3
"""
闲鱼 AI 助手 - 文案库管理模块
"""

import os
import json
import uuid
import shutil
from pathlib import Path
from datetime import datetime
from copy import deepcopy


class CopyLibrary:
    """爆款文案库管理器"""
    
    DEFAULT_LIBRARY = {
        "version": "2.0",
        "updated": None,
        "categories": {}
    }
    
    def __init__(self, library_path=None):
        """
        初始化文案库
        
        Args:
            library_path: 文案库文件路径
        """
        if library_path is None:
            library_path = Path(__file__).parent.parent / "data" / "copy_library.json"
        
        self.library_path = Path(library_path)
        self.library = self._load()
    
    def _load(self):
        """加载文案库"""
        if self.library_path.exists():
            with open(self.library_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return deepcopy(self.DEFAULT_LIBRARY)
    
    def _save(self):
        """保存文案库"""
        self.library["updated"] = datetime.now().isoformat()
        
        self.library_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.library_path, "w", encoding="utf-8") as f:
            json.dump(self.library, f, ensure_ascii=False, indent=2)
    
    def add_sample(self, category, title, description, features=None, 
                   source="manual", likes=0, images=None, image_features=None):
        """
        添加爆款文案样本
        
        Args:
            category: 分类（如"数码相机"）
            title: 标题
            description: 描述
            features: 特征标签列表
            source: 来源（manual/manual_crawl）
            likes: 点赞数
            images: 图片路径列表
            image_features: 图片特征字典
        
        Returns:
            str: 样本 ID
        """
        if category not in self.library["categories"]:
            self.library["categories"][category] = {
                "count": 0,
                "samples": []
            }
        
        sample_id = str(uuid.uuid4())[:8]
        
        sample = {
            "id": sample_id,
            "title": title,
            "description": description,
            "features": features or [],
            "source": source,
            "likes": likes,
            "effect_score": 0.5,  # 默认中等
            "created": datetime.now().isoformat(),
            "images": images or [],
            "image_features": image_features or {}
        }
        
        self.library["categories"][category]["samples"].append(sample)
        self.library["categories"][category]["count"] += 1
        
        self._save()
        
        return sample_id
    
    def add_image_to_sample(self, sample_id, image_path, image_features):
        """
        为样本添加图片
        
        Args:
            sample_id: 样本 ID
            image_path: 图片路径
            image_features: 图片特征
        
        Returns:
            bool: 是否成功
        """
        for category in self.library["categories"].values():
            for sample in category["samples"]:
                if sample["id"] == sample_id:
                    if "images" not in sample:
                        sample["images"] = []
                    if "image_features" not in sample:
                        sample["image_features"] = {}
                    
                    sample["images"].append(image_path)
                    sample["image_features"] = image_features
                    
                    self._save()
                    return True
        
        return False
    
    def get_samples(self, category=None, limit=5):
        """
        获取样本列表
        
        Args:
            category: 分类（可选）
            limit: 返回数量限制
        
        Returns:
            list: 样本列表
        """
        if category:
            return self.library["categories"].get(category, {}).get("samples", [])[:limit]
        else:
            # 返回所有分类的样本
            result = []
            for cat_samples in self.library["categories"].values():
                result.extend(cat_samples["samples"][:limit])
            return result[:limit]
    
    def get_similar_samples(self, category, count=3):
        """
        获取相似样本（用于 Few-shot Learning）
        
        Args:
            category: 分类
            count: 返回数量
        
        Returns:
            list: 相似样本列表
        """
        samples = self.library["categories"].get(category, {}).get("samples", [])
        
        # 按效果评分和点赞数排序
        sorted_samples = sorted(
            samples,
            key=lambda x: (x.get("effect_score", 0.5), x.get("likes", 0)),
            reverse=True
        )
        
        return sorted_samples[:count]
    
    def update_effect_score(self, sample_id, rating):
        """
        更新样本效果评分
        
        Args:
            sample_id: 样本 ID
            rating: 评分 (good/neutral/bad)
        
        Returns:
            bool: 是否成功
        """
        score_map = {"good": 0.1, "neutral": 0, "bad": -0.1}
        delta = score_map.get(rating, 0)
        
        for category in self.library["categories"].values():
            for sample in category["samples"]:
                if sample["id"] == sample_id:
                    current_score = sample.get("effect_score", 0.5)
                    sample["effect_score"] = max(0, min(1, current_score + delta))
                    sample["last_rating"] = rating
                    sample["last_rated_at"] = datetime.now().isoformat()
                    
                    self._save()
                    return True
        
        return False
    
    def get_categories(self):
        """获取所有分类"""
        return list(self.library["categories"].keys())
    
    def get_stats(self):
        """获取统计信息"""
        total = 0
        categories = {}
        
        for name, data in self.library["categories"].items():
            categories[name] = data["count"]
            total += data["count"]
        
        return {
            "total": total,
            "categories": categories,
            "version": self.library["version"],
            "updated": self.library["updated"]
        }
    
    def export_data(self, export_path):
        """导出文案库"""
        export_path = Path(export_path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(self.library, f, ensure_ascii=False, indent=2)
        
        return str(export_path)
    
    def import_data(self, import_path):
        """导入文案库"""
        import_path = Path(import_path)
        
        if not import_path.exists():
            return {"error": f"文件不存在: {import_path}"}
        
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.library = data
            self._save()
            
            return {"success": True, "stats": self.get_stats()}
        except json.JSONDecodeError as e:
            return {"error": f"JSON 解析失败: {e}"}


def main():
    """测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="文案库管理")
    parser.add_argument("--action", type=str, choices=["add", "list", "stats"], 
                       default="stats", help="操作")
    parser.add_argument("--category", type=str, help="分类")
    parser.add_argument("--title", type=str, help="标题")
    parser.add_argument("--description", type=str, help="描述")
    
    args = parser.parse_args()
    
    library = CopyLibrary()
    
    if args.action == "add":
        sample_id = library.add_sample(
            category=args.category or "数码相机",
            title=args.title or "测试标题",
            description=args.description or "测试描述"
        )
        print(json.dumps({"success": True, "sample_id": sample_id}))
    
    elif args.action == "list":
        samples = library.get_samples(args.category)
        print(json.dumps(samples, ensure_ascii=False, indent=2))
    
    elif args.action == "stats":
        print(json.dumps(library.get_stats(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
