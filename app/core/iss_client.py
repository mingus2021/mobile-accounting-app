#!/usr/bin/env python3
"""
ISS客户端模块
基于已验证的Python ISS实现，用于移动应用
"""

import json
import time
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from kivy.logger import Logger

class ISSClient:
    """ISS客户端，用于上传下载数据"""
    
    def __init__(self, endpoint, tid, private_key_pem):
        self.endpoint = endpoint
        self.tid = tid
        self.private_key_pem = private_key_pem
        self.private_key = None
        self._load_private_key()
    
    def _load_private_key(self):
        """加载私钥"""
        try:
            self.private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode('utf-8'),
                password=None
            )
            Logger.info(f"ISSClient: 私钥加载成功")
        except Exception as e:
            Logger.error(f"ISSClient: 私钥加载失败: {e}")
            raise Exception(f"私钥加载失败: {e}")
    
    def sign_data(self, data):
        """对数据进行ECDSA签名"""
        try:
            # 使用ECDSA + SHA256进行签名
            signature = self.private_key.sign(
                data.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            
            # 转换为十六进制字符串
            hex_signature = signature.hex().lower()
            
            Logger.debug(f"ISSClient: 签名数据: {data}")
            Logger.debug(f"ISSClient: 签名结果: {hex_signature}")
            
            return hex_signature
            
        except Exception as e:
            Logger.error(f"ISSClient: 签名失败: {e}")
            raise Exception(f"签名失败: {e}")
    
    def generate_auth_header(self, fid=''):
        """生成认证头"""
        timestamp = str(int(time.time()))
        sig_data = f"{self.tid}{fid}{timestamp}"
        signature = self.sign_data(sig_data)
        
        # 标准ISS认证头格式
        auth_header = f"tid={self.tid};sig={signature};t={timestamp}"
        
        Logger.debug(f"ISSClient: 认证头生成成功")
        return auth_header
    
    def upload_file(self, content, filename='data.json'):
        """上传文件到ISS"""
        try:
            url = f"{self.endpoint}/iss/v2/files"
            auth_header = self.generate_auth_header()
            
            # 准备文件数据
            files = {
                'file': (filename, content, 'application/json')
            }
            
            headers = {
                'Authorization': auth_header
            }
            
            Logger.info(f"ISSClient: 开始上传文件: {filename}")
            
            # 发送请求
            response = requests.post(url, files=files, headers=headers, timeout=30)
            
            Logger.info(f"ISSClient: 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                Logger.info(f"ISSClient: 上传成功: {result}")
                return result
            else:
                error_text = response.text
                Logger.error(f"ISSClient: 上传失败: {response.status_code} - {error_text}")
                raise Exception(f"HTTP {response.status_code}: {error_text}")
                
        except Exception as e:
            Logger.error(f"ISSClient: 上传异常: {e}")
            raise
    
    def download_file(self, fid):
        """从ISS下载文件"""
        try:
            url = f"{self.endpoint}/iss/v2/files/{fid}"
            auth_header = self.generate_auth_header(fid)
            
            headers = {
                'Authorization': auth_header
            }
            
            Logger.info(f"ISSClient: 开始下载文件: {fid}")
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=30)
            
            Logger.info(f"ISSClient: 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                Logger.info(f"ISSClient: 下载成功，内容长度: {len(content)}")
                return content
            else:
                error_text = response.text
                Logger.error(f"ISSClient: 下载失败: {response.status_code} - {error_text}")
                raise Exception(f"HTTP {response.status_code}: {error_text}")
                
        except Exception as e:
            Logger.error(f"ISSClient: 下载异常: {e}")
            raise
    
    def upload_transactions(self, transactions):
        """上传交易数据"""
        try:
            data = {
                'type': 'transactions',
                'timestamp': time.time(),
                'data': transactions
            }
            
            content = json.dumps(data, ensure_ascii=False, indent=2)
            filename = f'transactions_{int(time.time())}.json'
            
            result = self.upload_file(content, filename)
            return result
            
        except Exception as e:
            Logger.error(f"ISSClient: 上传交易数据失败: {e}")
            raise
    
    def download_transactions(self, fid):
        """下载交易数据"""
        try:
            content = self.download_file(fid)
            data = json.loads(content)
            
            if data.get('type') == 'transactions':
                return data.get('data', [])
            else:
                raise Exception("文件类型不匹配")
                
        except Exception as e:
            Logger.error(f"ISSClient: 下载交易数据失败: {e}")
            raise
    
    def test_connection(self):
        """测试ISS连接"""
        try:
            test_data = {
                'test': True,
                'timestamp': time.time(),
                'message': '连接测试'
            }
            
            content = json.dumps(test_data, ensure_ascii=False)
            filename = f'test_{int(time.time())}.json'
            
            result = self.upload_file(content, filename)
            Logger.info("ISSClient: 连接测试成功")
            return True
            
        except Exception as e:
            Logger.error(f"ISSClient: 连接测试失败: {e}")
            return False
