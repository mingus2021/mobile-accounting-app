#!/usr/bin/env python3
"""
数据存储模块
本地数据存储和ISS同步
"""

import os
import json
import sqlite3
import time
from datetime import datetime, timedelta
from kivy.logger import Logger

class DataStorage:
    """数据存储管理器"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.db_file = os.path.join(self.data_dir, 'transactions.db')
        self.mapping_file = os.path.join(self.data_dir, 'mapping.json')
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化数据库
        self.init_database()
        
        # 加载映射信息
        self.mapping = self.load_mapping()
    
    def init_database(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # 创建交易表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    synced INTEGER DEFAULT 0,
                    fid TEXT
                )
            ''')
            
            # 创建分类表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL,
                    color TEXT,
                    icon TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建同步记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sync_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fid TEXT NOT NULL,
                    sync_type TEXT NOT NULL,
                    sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            Logger.info("DataStorage: 数据库初始化成功")
            
        except Exception as e:
            Logger.error(f"DataStorage: 数据库初始化失败: {e}")
            raise
    
    def add_transaction(self, transaction):
        """添加交易记录"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (date, type, category, amount, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                transaction['date'],
                transaction['type'],
                transaction['category'],
                transaction['amount'],
                transaction.get('description', '')
            ))
            
            transaction_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            Logger.info(f"DataStorage: 添加交易记录成功，ID: {transaction_id}")
            return transaction_id
            
        except Exception as e:
            Logger.error(f"DataStorage: 添加交易记录失败: {e}")
            raise
    
    def get_transactions(self, start_date=None, end_date=None, limit=None):
        """获取交易记录"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            query = "SELECT * FROM transactions WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date DESC, created_at DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为字典列表
            columns = [desc[0] for desc in cursor.description]
            transactions = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            
            Logger.info(f"DataStorage: 获取交易记录成功，数量: {len(transactions)}")
            return transactions
            
        except Exception as e:
            Logger.error(f"DataStorage: 获取交易记录失败: {e}")
            raise
    
    def get_statistics(self, start_date=None, end_date=None):
        """获取统计信息"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # 基础查询条件
            where_clause = "WHERE 1=1"
            params = []
            
            if start_date:
                where_clause += " AND date >= ?"
                params.append(start_date)
            
            if end_date:
                where_clause += " AND date <= ?"
                params.append(end_date)
            
            # 总收入和支出
            cursor.execute(f'''
                SELECT 
                    type,
                    SUM(amount) as total,
                    COUNT(*) as count
                FROM transactions 
                {where_clause}
                GROUP BY type
            ''', params)
            
            totals = {row[0]: {'total': row[1], 'count': row[2]} for row in cursor.fetchall()}
            
            # 分类统计
            cursor.execute(f'''
                SELECT 
                    type,
                    category,
                    SUM(amount) as total,
                    COUNT(*) as count
                FROM transactions 
                {where_clause}
                GROUP BY type, category
                ORDER BY total DESC
            ''', params)
            
            categories = {}
            for row in cursor.fetchall():
                type_name = row[0]
                if type_name not in categories:
                    categories[type_name] = []
                categories[type_name].append({
                    'category': row[1],
                    'total': row[2],
                    'count': row[3]
                })
            
            conn.close()
            
            statistics = {
                'totals': totals,
                'categories': categories,
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
            
            Logger.info("DataStorage: 获取统计信息成功")
            return statistics
            
        except Exception as e:
            Logger.error(f"DataStorage: 获取统计信息失败: {e}")
            raise
    
    def sync_with_iss(self, iss_client):
        """与ISS同步数据"""
        try:
            # 获取未同步的交易
            unsynced_transactions = self.get_unsynced_transactions()
            
            if not unsynced_transactions:
                Logger.info("DataStorage: 没有需要同步的数据")
                return True
            
            # 准备同步数据
            sync_data = {
                'type': 'transactions',
                'timestamp': time.time(),
                'app_version': '1.0.0',
                'data': unsynced_transactions
            }
            
            # 上传到ISS
            content = json.dumps(sync_data, ensure_ascii=False, indent=2)
            filename = f'sync_{int(time.time())}.json'
            
            result = iss_client.upload_file(content, filename)
            
            if result and 'fid' in result:
                # 更新同步状态
                self.mark_transactions_synced(unsynced_transactions, result['fid'])
                
                # 保存映射信息
                self.save_mapping(result['fid'], filename)
                
                Logger.info(f"DataStorage: 数据同步成功，FID: {result['fid']}")
                return True
            else:
                Logger.error("DataStorage: 数据同步失败，无效的响应")
                return False
                
        except Exception as e:
            Logger.error(f"DataStorage: 数据同步失败: {e}")
            return False
    
    def get_unsynced_transactions(self):
        """获取未同步的交易"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM transactions WHERE synced = 0")
            rows = cursor.fetchall()
            
            columns = [desc[0] for desc in cursor.description]
            transactions = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            
            return transactions
            
        except Exception as e:
            Logger.error(f"DataStorage: 获取未同步交易失败: {e}")
            return []
    
    def mark_transactions_synced(self, transactions, fid):
        """标记交易为已同步"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            transaction_ids = [t['id'] for t in transactions]
            placeholders = ','.join(['?'] * len(transaction_ids))
            
            cursor.execute(f'''
                UPDATE transactions 
                SET synced = 1, fid = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id IN ({placeholders})
            ''', [fid] + transaction_ids)
            
            conn.commit()
            conn.close()
            
            Logger.info(f"DataStorage: 标记 {len(transactions)} 条交易为已同步")
            
        except Exception as e:
            Logger.error(f"DataStorage: 标记交易同步状态失败: {e}")
            raise
    
    def load_mapping(self):
        """加载映射信息"""
        try:
            if os.path.exists(self.mapping_file):
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    mapping = json.load(f)
                Logger.info("DataStorage: 映射信息加载成功")
                return mapping
            else:
                return {}
        except Exception as e:
            Logger.error(f"DataStorage: 映射信息加载失败: {e}")
            return {}
    
    def save_mapping(self, fid, filename):
        """保存映射信息"""
        try:
            self.mapping[fid] = {
                'filename': filename,
                'timestamp': time.time(),
                'date': datetime.now().isoformat()
            }
            
            with open(self.mapping_file, 'w', encoding='utf-8') as f:
                json.dump(self.mapping, f, ensure_ascii=False, indent=2)
            
            Logger.info(f"DataStorage: 映射信息保存成功，FID: {fid}")
            
        except Exception as e:
            Logger.error(f"DataStorage: 映射信息保存失败: {e}")
            raise
    
    def get_default_categories(self):
        """获取默认分类"""
        return {
            '收入': ['工资', '奖金', '投资收益', '兼职收入', '礼金', '退款', '其他收入'],
            '支出': ['餐饮', '交通', '购物', '娱乐', '医疗', '住房', '教育', '通讯', '保险', '其他支出']
        }
    
    def init_default_categories(self):
        """初始化默认分类"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            default_categories = self.get_default_categories()
            
            for type_name, categories in default_categories.items():
                for category in categories:
                    cursor.execute('''
                        INSERT OR IGNORE INTO categories (name, type)
                        VALUES (?, ?)
                    ''', (category, type_name))
            
            conn.commit()
            conn.close()
            
            Logger.info("DataStorage: 默认分类初始化成功")
            
        except Exception as e:
            Logger.error(f"DataStorage: 默认分类初始化失败: {e}")
    
    def close(self):
        """关闭数据存储"""
        try:
            # 保存映射信息
            if hasattr(self, 'mapping'):
                with open(self.mapping_file, 'w', encoding='utf-8') as f:
                    json.dump(self.mapping, f, ensure_ascii=False, indent=2)
            
            Logger.info("DataStorage: 数据存储关闭成功")
            
        except Exception as e:
            Logger.error(f"DataStorage: 数据存储关闭失败: {e}")
