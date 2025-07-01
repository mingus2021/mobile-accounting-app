#!/usr/bin/env python3
"""
密钥配置界面
支持通过贴文/消息配置密钥
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.logger import Logger
from app.core.config import EXAMPLE_POST_CONFIG, EXAMPLE_JSON_CONFIG

class KeyConfigScreen(Screen):
    """密钥配置界面"""
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        """构建界面"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(
            text='记账本配置',
            font_size='24sp',
            size_hint_y=None,
            height='50dp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # 说明文字
        description = Label(
            text='请粘贴包含配置信息的贴文或消息内容',
            font_size='16sp',
            size_hint_y=None,
            height='40dp'
        )
        main_layout.add_widget(description)
        
        # 配置输入区域
        input_label = Label(
            text='配置内容:',
            font_size='16sp',
            size_hint_y=None,
            height='30dp',
            halign='left'
        )
        input_label.bind(size=input_label.setter('text_size'))
        main_layout.add_widget(input_label)
        
        # 滚动文本输入
        scroll = ScrollView(size_hint=(1, 0.4))
        self.config_input = TextInput(
            multiline=True,
            hint_text='在此粘贴配置信息...',
            font_size='14sp'
        )
        scroll.add_widget(self.config_input)
        main_layout.add_widget(scroll)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=10)
        
        # 示例按钮
        example_btn = Button(
            text='查看示例',
            size_hint_x=0.3
        )
        example_btn.bind(on_press=self.show_example)
        button_layout.add_widget(example_btn)
        
        # 解析按钮
        parse_btn = Button(
            text='解析配置',
            size_hint_x=0.35
        )
        parse_btn.bind(on_press=self.parse_config)
        button_layout.add_widget(parse_btn)
        
        # 手动配置按钮
        manual_btn = Button(
            text='手动配置',
            size_hint_x=0.35
        )
        manual_btn.bind(on_press=self.show_manual_config)
        button_layout.add_widget(manual_btn)
        
        main_layout.add_widget(button_layout)
        
        # 状态显示
        self.status_label = Label(
            text='等待配置...',
            font_size='14sp',
            size_hint_y=None,
            height='30dp',
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(self.status_label)
        
        self.add_widget(main_layout)
    
    def show_example(self, instance):
        """显示配置示例"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='配置示例',
            font_size='18sp',
            size_hint_y=None,
            height='40dp',
            bold=True
        )
        content.add_widget(title)
        
        # 示例选择
        example_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)
        
        post_btn = Button(text='贴文格式')
        post_btn.bind(on_press=lambda x: self.show_example_text(EXAMPLE_POST_CONFIG))
        example_layout.add_widget(post_btn)
        
        json_btn = Button(text='JSON格式')
        json_btn.bind(on_press=lambda x: self.show_example_text(EXAMPLE_JSON_CONFIG))
        example_layout.add_widget(json_btn)
        
        content.add_widget(example_layout)
        
        # 示例文本
        scroll = ScrollView()
        self.example_text = TextInput(
            text=EXAMPLE_POST_CONFIG,
            multiline=True,
            readonly=True,
            font_size='12sp'
        )
        scroll.add_widget(self.example_text)
        content.add_widget(scroll)
        
        # 关闭按钮
        close_btn = Button(
            text='关闭',
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(close_btn)
        
        # 创建弹窗
        popup = Popup(
            title='配置示例',
            content=content,
            size_hint=(0.9, 0.8)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_example_text(self, text):
        """显示示例文本"""
        self.example_text.text = text
    
    def parse_config(self, instance):
        """解析配置"""
        config_text = self.config_input.text.strip()
        
        if not config_text:
            self.show_error("请输入配置内容")
            return
        
        try:
            self.status_label.text = "正在解析配置..."
            
            # 解析配置
            config_data = self.app.config_manager.parse_post_config(config_text)
            
            # 显示解析结果
            self.show_config_preview(config_data)
            
        except Exception as e:
            Logger.error(f"KeyConfigScreen: 配置解析失败: {e}")
            self.show_error(f"配置解析失败: {e}")
            self.status_label.text = "配置解析失败"
    
    def show_config_preview(self, config_data):
        """显示配置预览"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='配置预览',
            font_size='18sp',
            size_hint_y=None,
            height='40dp',
            bold=True
        )
        content.add_widget(title)
        
        # 配置信息
        info_text = f"""
应用名称: {config_data.get('app_name', '未设置')}
ISS端点: {config_data.get('iss_endpoint', '未设置')}
用户ID: {config_data.get('tid', '未设置')}
私钥: {'已设置' if config_data.get('private_key') else '未设置'}
同步启用: {'是' if config_data.get('sync_enabled', True) else '否'}
        """.strip()
        
        info_label = Label(
            text=info_text,
            font_size='14sp',
            halign='left'
        )
        info_label.bind(size=info_label.setter('text_size'))
        content.add_widget(info_label)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=10)
        
        cancel_btn = Button(text='取消')
        button_layout.add_widget(cancel_btn)
        
        confirm_btn = Button(text='确认使用')
        button_layout.add_widget(confirm_btn)
        
        content.add_widget(button_layout)
        
        # 创建弹窗
        popup = Popup(
            title='配置预览',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        cancel_btn.bind(on_press=popup.dismiss)
        confirm_btn.bind(on_press=lambda x: self.confirm_config(config_data, popup))
        
        popup.open()
    
    def confirm_config(self, config_data, popup):
        """确认配置"""
        try:
            popup.dismiss()
            self.status_label.text = "正在保存配置..."
            
            # 通知应用配置完成
            self.app.on_config_complete(config_data)
            
            self.status_label.text = "配置完成！"
            
        except Exception as e:
            Logger.error(f"KeyConfigScreen: 配置保存失败: {e}")
            self.show_error(f"配置保存失败: {e}")
            self.status_label.text = "配置保存失败"
    
    def show_manual_config(self, instance):
        """显示手动配置界面"""
        # TODO: 实现手动配置界面
        self.show_info("手动配置功能开发中...")
    
    def show_error(self, message):
        """显示错误信息"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        error_label = Label(
            text=message,
            font_size='16sp'
        )
        content.add_widget(error_label)
        
        ok_btn = Button(
            text='确定',
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='错误',
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_info(self, message):
        """显示信息"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        info_label = Label(
            text=message,
            font_size='16sp'
        )
        content.add_widget(info_label)
        
        ok_btn = Button(
            text='确定',
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='信息',
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
