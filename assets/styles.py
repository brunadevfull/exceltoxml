"""
Application styling constants and utilities
"""

import tkinter as tk
from tkinter import ttk

class AppStyles:
    """Application styling configuration"""
    
    # Color scheme
    COLORS = {
        'primary': '#366092',
        'secondary': '#52796f',
        'success': '#28a745',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'bg_main': '#f0f0f0',
        'bg_sidebar': '#e9ecef',
        'text_primary': '#212529',
        'text_secondary': '#6c757d',
        'border': '#dee2e6'
    }
    
    # Fonts
    FONTS = {
        'title': ('Arial', 16, 'bold'),
        'subtitle': ('Arial', 12, 'bold'),
        'normal': ('Arial', 10),
        'small': ('Arial', 8),
        'button': ('Arial', 10, 'bold')
    }
    
    # Spacing
    SPACING = {
        'small': 5,
        'medium': 10,
        'large': 20,
        'xlarge': 30
    }
    
    @classmethod
    def configure_styles(cls, root):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Configure theme
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=cls.COLORS['primary'],
                       foreground='white',
                       font=cls.FONTS['button'],
                       padding=(10, 5))
        
        style.map('Primary.TButton',
                 background=[('active', cls.COLORS['primary']),
                           ('pressed', cls.COLORS['primary'])])
        
        # Configure success button
        style.configure('Success.TButton',
                       background=cls.COLORS['success'],
                       foreground='white',
                       font=cls.FONTS['button'],
                       padding=(10, 5))
        
        # Configure danger button
        style.configure('Danger.TButton',
                       background=cls.COLORS['danger'],
                       foreground='white',
                       font=cls.FONTS['button'],
                       padding=(10, 5))
        
        # Configure frame styles
        style.configure('Sidebar.TFrame',
                       background=cls.COLORS['bg_sidebar'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure label styles
        style.configure('Title.TLabel',
                       font=cls.FONTS['title'],
                       foreground=cls.COLORS['text_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=cls.FONTS['subtitle'],
                       foreground=cls.COLORS['text_secondary'])
        
        # Configure entry styles
        style.configure('TEntry',
                       fieldbackground='white',
                       borderwidth=1,
                       insertwidth=2)
        
        # Configure progressbar
        style.configure('TProgressbar',
                       background=cls.COLORS['primary'],
                       troughcolor=cls.COLORS['light'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['primary'],
                       darkcolor=cls.COLORS['primary'])
        
        return style
    
    @classmethod
    def get_status_color(cls, status):
        """Get color for status messages"""
        status_colors = {
            'success': cls.COLORS['success'],
            'error': cls.COLORS['danger'],
            'warning': cls.COLORS['warning'],
            'info': cls.COLORS['info']
        }
        return status_colors.get(status, cls.COLORS['text_primary'])
