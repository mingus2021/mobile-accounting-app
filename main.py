#!/usr/bin/env python3
"""
Python记账本移动应用
基于Kivy框架，支持ISS云端同步和贴文密钥配置
"""

import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger
from kivy.config import Config

# 设置窗口大小（开发时使用）
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

# 导入应用模块
from app.core.config import ConfigManager
from app.core.iss_client import ISSClient
from app.core.storage import DataStorage
from app.ui.main_screen import MainScreen
from app.ui.add_transaction import AddTransactionScreen
from app.ui.statistics import StatisticsScreen
from app.ui.settings import SettingsScreen
from app.ui.key_config import KeyConfigScreen

class AccountingApp(App):
    """记账本主应用"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "记账本"
        self.icon = "assets/icons/app_icon.png"

        # 核心组件
        self.config_manager = ConfigManager()
        self.data_storage = DataStorage()
        self.iss_client = None

    def build(self):
        """构建应用界面"""
        Logger.info("AccountingApp: 开始构建应用界面")

        # 创建界面管理器
        sm = ScreenManager()

        # 添加所有界面
        sm.add_widget(KeyConfigScreen(name='key_config', app=self))
        sm.add_widget(MainScreen(name='main', app=self))
        sm.add_widget(AddTransactionScreen(name='add_transaction', app=self))
        sm.add_widget(StatisticsScreen(name='statistics', app=self))
        sm.add_widget(SettingsScreen(name='settings', app=self))

        # 检查配置状态
        if self.config_manager.is_configured():
            # 已配置，初始化ISS客户端并显示主界面
            config = self.config_manager.get_config()
            self.iss_client = ISSClient(
                endpoint=config['iss_endpoint'],
                tid=config['tid'],
                private_key_pem=config['private_key']
            )
            sm.current = 'main'
        else:
            # 未配置，显示配置界面
            sm.current = 'key_config'

        return sm
    
    def on_config_complete(self, config_data):
        """配置完成回调"""
        try:
            # 保存配置
            self.config_manager.save_config(config_data)

            # 初始化ISS客户端
            self.iss_client = ISSClient(
                endpoint=config_data['iss_endpoint'],
                tid=config_data['tid'],
                private_key_pem=config_data['private_key']
            )

            # 切换到主界面
            self.root.current = 'main'

            Logger.info("AccountingApp: 配置完成，切换到主界面")

        except Exception as e:
            Logger.error(f"AccountingApp: 配置保存失败: {e}")
    
    def on_config_complete(self, config_data):
        """配置完成回调"""
        try:
            # 保存配置
            self.config_manager.save_config(config_data)
            
            # 初始化ISS客户端
            self.iss_client = ISSClient(
                endpoint=config_data['iss_endpoint'],
                tid=config_data['tid'],
                private_key_pem=config_data['private_key']
            )
            
            # 设置主界面
            self.setup_main_screens()
            
            # 切换到主界面
            self.screen_manager.current = 'main'
            
            Logger.info("AccountingApp: 配置完成，切换到主界面")
            
        except Exception as e:
            Logger.error(f"AccountingApp: 配置保存失败: {e}")
            self.show_error_popup("配置失败", str(e))
    
    def show_error_popup(self, title, message):
        """显示错误弹窗"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 错误信息
        error_label = Label(
            text=message,
            text_size=(300, None),
            halign='center'
        )
        content.add_widget(error_label)
        
        # 确定按钮
        ok_button = Button(
            text='确定',
            size_hint=(1, 0.3)
        )
        content.add_widget(ok_button)
        
        # 创建弹窗
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_success_popup(self, title, message):
        """显示成功弹窗"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 成功信息
        success_label = Label(
            text=message,
            text_size=(300, None),
            halign='center'
        )
        content.add_widget(success_label)
        
        # 确定按钮
        ok_button = Button(
            text='确定',
            size_hint=(1, 0.3)
        )
        content.add_widget(ok_button)
        
        # 创建弹窗
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def sync_data(self):
        """同步数据到ISS"""
        if not self.iss_client:
            self.show_error_popup("同步失败", "ISS客户端未初始化")
            return
        
        try:
            # 获取本地数据
            transactions = self.data_storage.get_all_transactions()
            
            # 上传到ISS
            result = self.iss_client.upload_transactions(transactions)
            
            if result:
                self.show_success_popup("同步成功", "数据已成功同步到云端")
            else:
                self.show_error_popup("同步失败", "数据同步失败，请检查网络连接")
                
        except Exception as e:
            Logger.error(f"AccountingApp: 数据同步失败: {e}")
            self.show_error_popup("同步失败", str(e))
    
    def on_pause(self):
        """应用暂停时保存数据"""
        try:
            self.data_storage.save_all()
            Logger.info("AccountingApp: 应用暂停，数据已保存")
        except Exception as e:
            Logger.error(f"AccountingApp: 暂停时保存数据失败: {e}")
        return True
    
    def on_stop(self):
        """应用停止时清理资源"""
        try:
            if self.data_storage:
                self.data_storage.close()
            Logger.info("AccountingApp: 应用停止，资源已清理")
        except Exception as e:
            Logger.error(f"AccountingApp: 停止时清理资源失败: {e}")

def main():
    """应用入口"""
    # 设置日志级别
    Logger.setLevel('INFO')
    
    # 创建应用目录
    app_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(app_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 启动应用
    app = AccountingApp()
    app.run()

if __name__ == '__main__':
    main()
