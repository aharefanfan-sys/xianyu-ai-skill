#!/usr/bin/env python3
"""
闲鱼 AI 助手 - 闲鱼发布模块
"""

import os
import json
import time
import hashlib
import requests
from datetime import datetime


class IdlePublisher:
    """闲鱼商品发布器"""
    
    def __init__(self, app_key=None, app_secret=None, config_path=None):
        """
        初始化发布器
        
        Args:
            app_key: 闲鱼 App Key
            app_secret: 闲鱼 App Secret
            config_path: 配置文件路径
        """
        self.app_key = app_key or os.environ.get("IDLE_APP_KEY")
        self.app_secret = app_secret or os.environ.get("IDLE_APP_SECRET")
        
        self.base_url = "https://eco.taobao.com/router/rest"
        self.sandbox_url = "http://gw.api.taobao.com/router/rest"
        
        self._is_sandbox = False
        
        if not self.app_key or not self.app_secret:
            print("警告: 未配置闲鱼 API 凭证，发布功能不可用")
    
    def enable_sandbox(self):
        """启用沙箱环境"""
        self._is_sandbox = True
        self.base_url = self.sandbox_url
    
    def disable_sandbox(self):
        """禁用沙箱环境"""
        self._is_sandbox = False
        self.base_url = "https://eco.taobao.com/router/rest"
    
    def _generate_sign(self, params):
        """生成签名"""
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = self.app_secret + "".join([f"{k}{v}" for k, v in sorted_params]) + self.app_secret
        return hashlib.md5(sign_str.encode()).hexdigest().upper()
    
    def _make_request(self, method, params):
        """发送请求"""
        if not self.app_key or not self.app_secret:
            return {"error": "未配置 API 凭证"}
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        base_params = {
            "app_key": self.app_key,
            "method": method,
            "timestamp": timestamp,
            "format": "json",
            "v": "2.0",
            "sign_method": "md5"
        }
        
        params.update(base_params)
        params["sign"] = self._generate_sign(params)
        
        try:
            response = requests.post(self.base_url, params=params, timeout=30)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def upload_image(self, image_path):
        """
        上传图片
        
        Args:
            image_path: 图片路径
        
        Returns:
            dict: 上传结果
        """
        method = "alibaba.idle.isv.media.upload"
        
        try:
            with open(image_path, "rb") as f:
                files = {"image": f.read()}
                data = {"method": method}
                
                response = requests.post(
                    self.base_url,
                    data=data,
                    files=files,
                    timeout=60
                )
            
            return response.json()
        except FileNotFoundError:
            return {"error": f"图片不存在: {image_path}"}
        except Exception as e:
            return {"error": str(e)}
    
    def publish_item(self, title, description, price, images=None, category_id=None):
        """
        发布商品
        
        Args:
            title: 商品标题
            description: 商品描述
            price: 商品价格
            images: 图片 URL 列表（可选）
            category_id: 类目 ID（可选）
        
        Returns:
            dict: 发布结果
        """
        method = "alibaba.idle.isv.item.publish"
        
        params = {
            "title": title,
            "description": description,
            "price": str(price),
            "quantity": 1
        }
        
        if category_id:
            params["category_id"] = category_id
        
        if images:
            params["images"] = ",".join(images)
        
        return self._make_request(method, params)
    
    def edit_item(self, item_id, title=None, description=None, price=None):
        """
        编辑商品
        
        Args:
            item_id: 商品 ID
            title: 新标题（可选）
            description: 新描述（可选）
            price: 新价格（可选）
        
        Returns:
            dict: 编辑结果
        """
        method = "alibaba.idle.isv.item.edit"
        
        params = {"item_id": item_id}
        
        if title:
            params["title"] = title
        if description:
            params["description"] = description
        if price:
            params["price"] = str(price)
        
        return self._make_request(method, params)
    
    def get_item(self, item_id):
        """
        获取商品信息
        
        Args:
            item_id: 商品 ID
        
        Returns:
            dict: 商品信息
        """
        method = "alibaba.idle.item.user.publishitems"
        return self._make_request(method, {"item_id": item_id})
    
    def list_items(self, page_no=1, page_size=20):
        """
        获取商品列表
        
        Args:
            page_no: 页码
            page_size: 每页数量
        
        Returns:
            dict: 商品列表
        """
        method = "alibaba.idle.item.user.publishitems"
        return self._make_request(method, {
            "page_no": page_no,
            "page_size": page_size
        })


def main():
    """测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="闲鱼发布器")
    parser.add_argument("--test", action="store_true", help="运行测试")
    
    args = parser.parse_args()
    
    if args.test:
        publisher = IdlePublisher()
        
        if not publisher.app_key:
            print("未配置 API 凭证，跳过测试")
        else:
            print("闲鱼发布器已初始化")
            print(f"App Key: {publisher.app_key[:10]}...")


if __name__ == "__main__":
    main()
