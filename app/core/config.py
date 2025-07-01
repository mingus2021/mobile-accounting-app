#!/usr/bin/env python3
"""
配置管理模块
支持通过贴文/消息配置密钥
"""

import os
import json
import re
from kivy.logger import Logger

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config_file = os.path.join('data', 'config.json')
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                Logger.info("ConfigManager: 配置加载成功")
            else:
                self.config = {}
                Logger.info("ConfigManager: 配置文件不存在，使用默认配置")
        except Exception as e:
            Logger.error(f"ConfigManager: 配置加载失败: {e}")
            self.config = {}
    
    def save_config(self, config_data):
        """保存配置"""
        try:
            # 确保数据目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # 更新配置
            self.config.update(config_data)
            
            # 保存到文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            Logger.info("ConfigManager: 配置保存成功")
            
        except Exception as e:
            Logger.error(f"ConfigManager: 配置保存失败: {e}")
            raise
    
    def get_config(self):
        """获取配置"""
        return self.config.copy()
    
    def is_configured(self):
        """检查是否已配置"""
        required_keys = ['iss_endpoint', 'tid', 'private_key']
        return all(key in self.config and self.config[key] for key in required_keys)
    
    def parse_post_config(self, post_text):
        """解析贴文配置
        
        支持的格式：
        1. JSON格式
        2. 键值对格式
        3. 混合格式
        """
        try:
            # 尝试解析JSON格式
            json_match = re.search(r'\{.*\}', post_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                config = json.loads(json_text)
                return self.validate_config(config)
            
            # 解析键值对格式
            config = {}
            
            # 提取ISS端点
            endpoint_match = re.search(r'(?:endpoint|服务器|地址)[:：]\s*([^\s\n]+)', post_text, re.IGNORECASE)
            if endpoint_match:
                config['iss_endpoint'] = endpoint_match.group(1)
            
            # 提取TID
            tid_match = re.search(r'(?:tid|用户ID)[:：]\s*([^\s\n]+)', post_text, re.IGNORECASE)
            if tid_match:
                config['tid'] = tid_match.group(1)
            
            # 提取私钥
            key_match = re.search(r'-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----', post_text, re.DOTALL)
            if key_match:
                config['private_key'] = key_match.group()
            
            # 提取应用名称
            name_match = re.search(r'(?:name|应用名称|名称)[:：]\s*([^\n]+)', post_text, re.IGNORECASE)
            if name_match:
                config['app_name'] = name_match.group(1).strip()
            
            return self.validate_config(config)
            
        except Exception as e:
            Logger.error(f"ConfigManager: 贴文解析失败: {e}")
            raise Exception(f"贴文解析失败: {e}")
    
    def validate_config(self, config):
        """验证配置"""
        required_keys = ['iss_endpoint', 'tid', 'private_key']
        
        # 检查必需字段
        for key in required_keys:
            if key not in config or not config[key]:
                raise Exception(f"缺少必需字段: {key}")
        
        # 验证端点格式
        endpoint = config['iss_endpoint']
        if not (endpoint.startswith('http://') or endpoint.startswith('https://')):
            raise Exception("ISS端点必须以http://或https://开头")
        
        # 验证TID格式
        tid = config['tid']
        if len(tid) < 10:
            raise Exception("TID长度不足")
        
        # 验证私钥格式
        private_key = config['private_key']
        if not ('-----BEGIN PRIVATE KEY-----' in private_key and '-----END PRIVATE KEY-----' in private_key):
            raise Exception("私钥格式不正确")
        
        # 设置默认值
        config.setdefault('app_name', '我的记账本')
        config.setdefault('sync_enabled', True)
        
        Logger.info("ConfigManager: 配置验证成功")
        return config
    
    def export_config(self):
        """导出配置（用于备份）"""
        try:
            export_data = self.config.copy()
            # 移除敏感信息
            if 'private_key' in export_data:
                export_data['private_key'] = '***已隐藏***'
            
            return json.dumps(export_data, ensure_ascii=False, indent=2)
            
        except Exception as e:
            Logger.error(f"ConfigManager: 配置导出失败: {e}")
            raise
    
    def reset_config(self):
        """重置配置"""
        try:
            self.config = {}
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            Logger.info("ConfigManager: 配置重置成功")
        except Exception as e:
            Logger.error(f"ConfigManager: 配置重置失败: {e}")
            raise

# 配置示例
EXAMPLE_POST_CONFIG = """
记账本配置信息：

endpoint: http://219.237.197.44:9099
tid: t8l6vbu06gaua00pzfvz96tdu4r01z7a
name: 我的记账本

-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgmbpMrOTX8mJ/wrvW
d2XfDcxli75P6D4GgJmeqcChqyehRANCAARb+5Q37dOA+u2A2WCqyoXgohMaefCl
QmLBqcoh87BsYytwpj1mW+RNkiKXekIvJqQxwJF6l1P21+dmJXCtcVSl
-----END PRIVATE KEY-----
"""

EXAMPLE_JSON_CONFIG = """{
  "iss_endpoint": "http://219.237.197.44:9099",
  "tid": "t8l6vbu06gaua00pzfvz96tdu4r01z7a",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgmbpMrOTX8mJ/wrvW\\nd2XfDcxli75P6D4GgJmeqcChqyehRANCAARb+5Q37dOA+u2A2WCqyoXgohMaefCl\\nQmLBqcoh87BsYytwpj1mW+RNkiKXekIvJqQxwJF6l1P21+dmJXCtcVSl\\n-----END PRIVATE KEY-----",
  "app_name": "我的记账本",
  "sync_enabled": true
}"""
