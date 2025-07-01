#!/usr/bin/env python3
"""
主界面
显示余额、最近交易和快速操作
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.logger import Logger
from datetime import datetime, timedelta

class MainScreen(Screen):
    """主界面"""
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
        
        # 定时刷新数据
        Clock.schedule_interval(self.refresh_data, 30)
    
    def build_ui(self):
        """构建界面"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部余额区域
        balance_layout = self.create_balance_section()
        main_layout.add_widget(balance_layout)
        
        # 快速操作按钮
        quick_actions = self.create_quick_actions()
        main_layout.add_widget(quick_actions)
        
        # 最近交易列表
        recent_transactions = self.create_recent_transactions()
        main_layout.add_widget(recent_transactions)
        
        # 底部导航
        bottom_nav = self.create_bottom_navigation()
        main_layout.add_widget(bottom_nav)
        
        self.add_widget(main_layout)
    
    def create_balance_section(self):
        """创建余额显示区域"""
        layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height='120dp',
            padding=15,
            spacing=5
        )
        
        # 背景色（模拟卡片效果）
        layout.canvas.before.clear()
        
        # 总余额标题
        title = Label(
            text='总余额',
            font_size='16sp',
            size_hint_y=None,
            height='30dp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(title)
        
        # 余额金额
        self.balance_label = Label(
            text='¥0.00',
            font_size='32sp',
            size_hint_y=None,
            height='50dp',
            bold=True,
            color=(0.2, 0.6, 0.2, 1)
        )
        layout.add_widget(self.balance_label)
        
        # 本月收支
        monthly_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='30dp'
        )
        
        self.income_label = Label(
            text='收入: ¥0.00',
            font_size='14sp',
            color=(0.2, 0.6, 0.2, 1)
        )
        monthly_layout.add_widget(self.income_label)
        
        self.expense_label = Label(
            text='支出: ¥0.00',
            font_size='14sp',
            color=(0.8, 0.2, 0.2, 1)
        )
        monthly_layout.add_widget(self.expense_label)
        
        layout.add_widget(monthly_layout)
        
        return layout
    
    def create_quick_actions(self):
        """创建快速操作按钮"""
        layout = GridLayout(
            cols=2,
            size_hint_y=None,
            height='80dp',
            spacing=10
        )
        
        # 添加收入按钮
        income_btn = Button(
            text='+ 收入',
            font_size='16sp',
            background_color=(0.2, 0.7, 0.2, 1)
        )
        income_btn.bind(on_press=lambda x: self.add_transaction('收入'))
        layout.add_widget(income_btn)
        
        # 添加支出按钮
        expense_btn = Button(
            text='- 支出',
            font_size='16sp',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        expense_btn.bind(on_press=lambda x: self.add_transaction('支出'))
        layout.add_widget(expense_btn)
        
        return layout
    
    def create_recent_transactions(self):
        """创建最近交易列表"""
        layout = BoxLayout(orientation='vertical', spacing=5)
        
        # 标题
        title_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='40dp'
        )
        
        title = Label(
            text='最近交易',
            font_size='18sp',
            bold=True,
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        title_layout.add_widget(title)
        
        # 查看全部按钮
        view_all_btn = Button(
            text='查看全部',
            size_hint_x=None,
            width='80dp',
            font_size='14sp'
        )
        view_all_btn.bind(on_press=self.view_all_transactions)
        title_layout.add_widget(view_all_btn)
        
        layout.add_widget(title_layout)
        
        # 交易列表滚动区域
        scroll = ScrollView()
        self.transaction_list = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=2
        )
        self.transaction_list.bind(minimum_height=self.transaction_list.setter('height'))
        
        scroll.add_widget(self.transaction_list)
        layout.add_widget(scroll)
        
        return layout
    
    def create_bottom_navigation(self):
        """创建底部导航"""
        layout = GridLayout(
            cols=4,
            size_hint_y=None,
            height='60dp',
            spacing=2
        )
        
        # 主页按钮
        home_btn = Button(
            text='主页',
            font_size='14sp',
            background_color=(0.3, 0.5, 0.8, 1)
        )
        layout.add_widget(home_btn)
        
        # 添加按钮
        add_btn = Button(
            text='添加',
            font_size='14sp'
        )
        add_btn.bind(on_press=self.goto_add_transaction)
        layout.add_widget(add_btn)
        
        # 统计按钮
        stats_btn = Button(
            text='统计',
            font_size='14sp'
        )
        stats_btn.bind(on_press=self.goto_statistics)
        layout.add_widget(stats_btn)
        
        # 设置按钮
        settings_btn = Button(
            text='设置',
            font_size='14sp'
        )
        settings_btn.bind(on_press=self.goto_settings)
        layout.add_widget(settings_btn)
        
        return layout
    
    def refresh_data(self, dt=None):
        """刷新数据"""
        try:
            if not self.app or not self.app.data_storage:
                return
            
            # 获取本月统计
            today = datetime.now()
            month_start = today.replace(day=1).strftime('%Y-%m-%d')
            month_end = today.strftime('%Y-%m-%d')
            
            stats = self.app.data_storage.get_statistics(month_start, month_end)
            
            # 更新余额显示
            income_total = stats['totals'].get('收入', {}).get('total', 0)
            expense_total = stats['totals'].get('支出', {}).get('total', 0)
            balance = income_total - expense_total
            
            self.balance_label.text = f'¥{balance:.2f}'
            self.income_label.text = f'收入: ¥{income_total:.2f}'
            self.expense_label.text = f'支出: ¥{expense_total:.2f}'
            
            # 更新最近交易
            recent_transactions = self.app.data_storage.get_transactions(limit=10)
            self.update_transaction_list(recent_transactions)
            
            Logger.info("MainScreen: 数据刷新成功")
            
        except Exception as e:
            Logger.error(f"MainScreen: 数据刷新失败: {e}")
    
    def update_transaction_list(self, transactions):
        """更新交易列表"""
        try:
            # 清空现有列表
            self.transaction_list.clear_widgets()
            
            if not transactions:
                # 显示空状态
                empty_label = Label(
                    text='暂无交易记录',
                    font_size='16sp',
                    color=(0.6, 0.6, 0.6, 1),
                    size_hint_y=None,
                    height='60dp'
                )
                self.transaction_list.add_widget(empty_label)
                return
            
            # 添加交易项
            for transaction in transactions:
                item = self.create_transaction_item(transaction)
                self.transaction_list.add_widget(item)
                
        except Exception as e:
            Logger.error(f"MainScreen: 更新交易列表失败: {e}")
    
    def create_transaction_item(self, transaction):
        """创建交易项"""
        layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            padding=10,
            spacing=10
        )
        
        # 交易信息
        info_layout = BoxLayout(orientation='vertical')
        
        # 分类和描述
        title_text = transaction['category']
        if transaction.get('description'):
            title_text += f" - {transaction['description']}"
        
        title = Label(
            text=title_text,
            font_size='14sp',
            halign='left',
            size_hint_y=0.6
        )
        title.bind(size=title.setter('text_size'))
        info_layout.add_widget(title)
        
        # 日期
        date_label = Label(
            text=transaction['date'],
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            halign='left',
            size_hint_y=0.4
        )
        date_label.bind(size=date_label.setter('text_size'))
        info_layout.add_widget(date_label)
        
        layout.add_widget(info_layout)
        
        # 金额
        amount = transaction['amount']
        amount_color = (0.2, 0.6, 0.2, 1) if transaction['type'] == '收入' else (0.8, 0.2, 0.2, 1)
        amount_prefix = '+' if transaction['type'] == '收入' else '-'
        
        amount_label = Label(
            text=f'{amount_prefix}¥{amount:.2f}',
            font_size='16sp',
            color=amount_color,
            bold=True,
            size_hint_x=None,
            width='100dp',
            halign='right'
        )
        amount_label.bind(size=amount_label.setter('text_size'))
        layout.add_widget(amount_label)
        
        return layout
    
    def add_transaction(self, transaction_type):
        """添加交易"""
        try:
            # 切换到添加交易界面，并传递类型
            self.manager.current = 'add_transaction'
            add_screen = self.manager.get_screen('add_transaction')
            add_screen.set_transaction_type(transaction_type)
            
        except Exception as e:
            Logger.error(f"MainScreen: 切换到添加交易界面失败: {e}")
    
    def view_all_transactions(self, instance):
        """查看所有交易"""
        try:
            self.manager.current = 'statistics'
        except Exception as e:
            Logger.error(f"MainScreen: 切换到统计界面失败: {e}")
    
    def goto_add_transaction(self, instance):
        """跳转到添加交易"""
        try:
            self.manager.current = 'add_transaction'
        except Exception as e:
            Logger.error(f"MainScreen: 跳转到添加交易失败: {e}")
    
    def goto_statistics(self, instance):
        """跳转到统计"""
        try:
            self.manager.current = 'statistics'
        except Exception as e:
            Logger.error(f"MainScreen: 跳转到统计失败: {e}")
    
    def goto_settings(self, instance):
        """跳转到设置"""
        try:
            self.manager.current = 'settings'
        except Exception as e:
            Logger.error(f"MainScreen: 跳转到设置失败: {e}")
    
    def on_enter(self):
        """界面进入时刷新数据"""
        self.refresh_data()
