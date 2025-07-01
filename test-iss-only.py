#!/usr/bin/env python3
"""
最小化ISS测试版本
仅测试ISS上传下载功能，不依赖Kivy
"""

import json
import time
import os
import sys

# 检查依赖
try:
    import requests
    import cryptography
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    print("✅ 核心依赖检查通过")
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请运行: pip install requests cryptography")
    input("按回车键退出...")
    sys.exit(1)

class SimpleISSClient:
    """简化的ISS客户端"""
    
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
            print(f"✅ 私钥加载成功")
        except Exception as e:
            raise Exception(f"私钥加载失败: {e}")
    
    def sign_data(self, data):
        """对数据进行ECDSA签名"""
        try:
            signature = self.private_key.sign(
                data.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            hex_signature = signature.hex().lower()
            print(f"🔐 签名生成成功: {len(hex_signature)} 字符")
            return hex_signature
        except Exception as e:
            raise Exception(f"签名失败: {e}")
    
    def generate_auth_header(self, fid=''):
        """生成认证头"""
        timestamp = str(int(time.time()))
        sig_data = f"{self.tid}{fid}{timestamp}"
        signature = self.sign_data(sig_data)
        auth_header = f"tid={self.tid};sig={signature};t={timestamp}"
        print(f"🔑 认证头生成成功")
        return auth_header
    
    def upload_file(self, content, filename='test.json'):
        """上传文件到ISS"""
        try:
            url = f"{self.endpoint}/iss/v2/files"
            auth_header = self.generate_auth_header()
            
            files = {
                'file': (filename, content, 'application/json')
            }
            
            headers = {
                'Authorization': auth_header
            }
            
            print(f"📡 开始上传: {filename}")
            print(f"📊 内容大小: {len(content)} 字节")
            
            response = requests.post(url, files=files, headers=headers, timeout=30)
            
            print(f"📈 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 上传成功!")
                print(f"📄 文件ID: {result.get('fid', 'N/A')}")
                return result
            else:
                error_text = response.text
                print(f"❌ 上传失败: {response.status_code}")
                print(f"📄 错误详情: {error_text}")
                return None
                
        except Exception as e:
            print(f"❌ 上传异常: {e}")
            return None
    
    def test_connection(self):
        """测试连接"""
        try:
            test_data = {
                'test': True,
                'timestamp': time.time(),
                'message': 'Python ISS连接测试',
                'version': '1.0.0'
            }
            
            content = json.dumps(test_data, ensure_ascii=False, indent=2)
            filename = f'test_{int(time.time())}.json'
            
            result = self.upload_file(content, filename)
            return result is not None
            
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False

def parse_config_from_text(text):
    """从文本解析配置"""
    config = {}
    
    # 提取ISS端点
    import re
    endpoint_match = re.search(r'(?:endpoint|服务器|地址)[:：]\s*([^\s\n]+)', text, re.IGNORECASE)
    if endpoint_match:
        config['iss_endpoint'] = endpoint_match.group(1)
    
    # 提取TID
    tid_match = re.search(r'(?:tid|用户ID)[:：]\s*([^\s\n]+)', text, re.IGNORECASE)
    if tid_match:
        config['tid'] = tid_match.group(1)
    
    # 提取私钥
    key_match = re.search(r'-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----', text, re.DOTALL)
    if key_match:
        config['private_key'] = key_match.group()
    
    return config

def main():
    """主函数"""
    print("=" * 60)
    print("🐍 Python移动记账应用 - ISS测试版")
    print("=" * 60)
    print()
    
    # 默认配置
    default_config = {
        'iss_endpoint': 'http://219.237.197.44:9099',
        'tid': 't8l6vbu06gaua00pzfvz96tdu4r01z7a',
        'private_key': '''-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgmbpMrOTX8mJ/wrvW
d2XfDcxli75P6D4GgJmeqcChqyehRANCAARb+5Q37dOA+u2A2WCqyoXgohMaefCl
QmLBqcoh87BsYytwpj1mW+RNkiKXekIvJqQxwJF6l1P21+dmJXCtcVSl
-----END PRIVATE KEY-----'''
    }
    
    print("选择配置方式:")
    print("1. 使用默认配置（推荐）")
    print("2. 粘贴贴文配置")
    print("3. 手动输入配置")
    print()
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "2":
        print("\n请粘贴包含配置信息的贴文内容:")
        print("（粘贴完成后按回车）")
        config_text = input()
        
        config = parse_config_from_text(config_text)
        
        if not all(key in config for key in ['iss_endpoint', 'tid', 'private_key']):
            print("❌ 配置解析失败，使用默认配置")
            config = default_config
        else:
            print("✅ 配置解析成功")
    
    elif choice == "3":
        print("\n手动输入配置:")
        config = {}
        config['iss_endpoint'] = input("ISS端点: ").strip() or default_config['iss_endpoint']
        config['tid'] = input("TID: ").strip() or default_config['tid']
        print("私钥 (多行输入，空行结束):")
        key_lines = []
        while True:
            line = input()
            if not line:
                break
            key_lines.append(line)
        config['private_key'] = '\n'.join(key_lines) or default_config['private_key']
    
    else:
        print("✅ 使用默认配置")
        config = default_config
    
    print("\n" + "=" * 60)
    print("🔧 配置信息:")
    print(f"📡 ISS端点: {config['iss_endpoint']}")
    print(f"🆔 TID: {config['tid']}")
    print(f"🔑 私钥: {'已设置' if config['private_key'] else '未设置'}")
    print("=" * 60)
    print()
    
    try:
        # 创建ISS客户端
        client = SimpleISSClient(
            config['iss_endpoint'],
            config['tid'],
            config['private_key']
        )
        
        # 测试连接
        print("🧪 开始测试ISS连接...")
        print()
        
        success = client.test_connection()
        
        print()
        print("=" * 60)
        if success:
            print("🎉 ISS测试成功!")
            print("✅ Python ISS客户端工作正常")
            print("✅ 密钥配置正确")
            print("✅ 网络连接正常")
            print()
            print("💡 现在可以继续开发完整的移动应用了!")
        else:
            print("❌ ISS测试失败")
            print("请检查:")
            print("• 网络连接")
            print("• ISS服务器状态")
            print("• 配置信息正确性")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
    
    print()
    input("按回车键退出...")

if __name__ == "__main__":
    main()
