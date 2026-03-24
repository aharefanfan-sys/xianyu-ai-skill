#!/usr/bin/env python3
"""
闲鱼 AI 助手 - 配置管理模块
"""

import os
import json
from pathlib import Path


class Config:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        "version": "2.0",
        "api": {
            "provider": "minimax",
            "model": "MiniMax-M2-Stable",
            "base_url": "https://api.minimax.chat/v1",
            "temperature": 0.7,
            "max_tokens": 1000
        },
        "library": {
            "path": "data/copy_library.json",
            "auto_backup": True
        },
        "images": {
            "storage_dir": "data/images",
            "max_size_mb": 5,
            "supported_formats": [".jpg", ".jpeg", ".png", ".webp"]
        },
        "traffic_rules": {
            "enabled": True,
            "path": "scripts/traffic_rules.json"
        },
        "output": {
            "format": "json",
            "show_warnings": True
        }
    }
    
    def __init__(self, config_path=None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "data" / "config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load()
    
    def _load(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                return self._merge_config(user_config)
        else:
            return self._create_default()
    
    def _merge_config(self, user_config):
        """合并用户配置和默认配置"""
        config = self.DEFAULT_CONFIG.copy()
        
        for key, value in user_config.items():
            if isinstance(value, dict) and key in config:
                config[key].update(value)
            else:
                config[key] = value
        
        return config
    
    def _create_default(self):
        """创建默认配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        
        return self.DEFAULT_CONFIG
    
    def save(self):
        """保存配置"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def set(self, key, value):
        """设置配置项"""
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save()
    
    def get_api_key(self):
        """获取 API Key（优先环境变量）"""
        return os.environ.get("MINIMAX_API_KEY") or self.get("api.key")
    
    def set_api_key(self, api_key):
        """设置 API Key"""
        self.set("api.key", api_key)
    
    def get_model(self):
        """获取模型名称"""
        return self.get("api.model", "MiniMax-M2-Stable")
    
    def get_library_path(self):
        """获取文案库路径"""
        path = self.get("library.path")
        if not Path(path).is_absolute():
            return Path(__file__).parent.parent / path
        return Path(path)
    
    def get_image_storage_dir(self):
        """获取图片存储目录"""
        path = self.get("images.storage_dir")
        if not Path(path).is_absolute():
            return Path(__file__).parent.parent / path
        return Path(path)
    
    @classmethod
    def get_api_key_from_env(cls):
        """从环境变量获取 API Key"""
        return os.environ.get("MINIMAX_API_KEY")


def main():
    """测试函数"""
    config = Config()
    print(json.dumps(config.config, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
