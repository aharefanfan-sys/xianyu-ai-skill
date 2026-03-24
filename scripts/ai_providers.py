#!/usr/bin/env python3
"""
AI Provider 适配器
支持多种 AI 模型：MiniMax、DeepSeek、OpenAI、Claude
"""

import os
import json
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """AI Provider 基类"""
    
    @abstractmethod
    def generate(self, prompt, **kwargs):
        """生成文本"""
        pass
    
    @abstractmethod
    def get_name(self):
        """获取 Provider 名称"""
        pass


class MiniMaxProvider(AIProvider):
    """MiniMax AI Provider"""
    
    def __init__(self, api_key=None, model="MiniMax-M2-Stable"):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.model = model
        self.base_url = "https://api.minimax.chat/v1"
    
    def generate(self, prompt, **kwargs):
        try:
            from openai import OpenAI
        except ImportError:
            return {"error": "请安装 openai: pip install openai"}
        
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000)
        )
        
        return {"content": response.choices[0].message.content}
    
    def get_name(self):
        return "minimax"


class DeepSeekProvider(AIProvider):
    """DeepSeek AI Provider"""
    
    def __init__(self, api_key=None, model="deepseek-chat"):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"
    
    def generate(self, prompt, **kwargs):
        try:
            from openai import OpenAI
        except ImportError:
            return {"error": "请安装 openai: pip install openai"}
        
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000)
        )
        
        return {"content": response.choices[0].message.content}
    
    def get_name(self):
        return "deepseek"


class OpenAIProvider(AIProvider):
    """OpenAI Provider"""
    
    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
    
    def generate(self, prompt, **kwargs):
        try:
            from openai import OpenAI
        except ImportError:
            return {"error": "请安装 openai: pip install openai"}
        
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000)
        )
        
        return {"content": response.choices[0].message.content}
    
    def get_name(self):
        return "openai"


class ClaudeProvider(AIProvider):
    """Claude Provider (via OpenAI-compatible API or direct)"""
    
    def __init__(self, api_key=None, model="claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"
    
    def generate(self, prompt, **kwargs):
        try:
            import anthropic
        except ImportError:
            return {"error": "请安装 anthropic: pip install anthropic"}
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1000),
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {"content": response.content[0].text}
    
    def get_name(self):
        return "claude"


class AIFactory:
    """AI Provider 工厂"""
    
    PROVIDERS = {
        "minimax": MiniMaxProvider,
        "deepseek": DeepSeekProvider,
        "openai": OpenAIProvider,
        "claude": ClaudeProvider
    }
    
    @classmethod
    def create(cls, provider_name, **kwargs):
        """创建 AI Provider"""
        provider_class = cls.PROVIDERS.get(provider_name.lower())
        
        if not provider_class:
            raise ValueError(f"未知 Provider: {provider_name}")
        
        return provider_class(**kwargs)
    
    @classmethod
    def list_providers(cls):
        """列出所有可用的 Provider"""
        return list(cls.PROVIDERS.keys())


def main():
    """测试"""
    print("支持的 AI Provider:")
    for p in AIFactory.list_providers():
        print(f"  - {p}")


if __name__ == "__main__":
    main()
