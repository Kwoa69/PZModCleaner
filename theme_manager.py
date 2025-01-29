import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self):
        self.style = ttk.Style()
        
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#0078d7',
                'select_fg': '#ffffff',
                'button_bg': '#f0f0f0',
                'button_hover': '#e0e0e0',
                'button_pressed': '#d0d0d0',
                'entry_bg': '#ffffff',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#000000'
            },
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'select_bg': '#0078d7',
                'select_fg': '#ffffff',
                'button_bg': '#3d3d3d',
                'button_hover': '#4d4d4d',
                'button_pressed': '#5d5d5d',
                'entry_bg': '#3d3d3d',
                'listbox_bg': '#2d2d2d',
                'listbox_fg': '#ffffff'
            },
            'blue': {
                'bg': '#1e2433',
                'fg': '#ffffff',
                'select_bg': '#3b82f6',
                'select_fg': '#ffffff',
                'button_bg': '#2d3748',
                'button_hover': '#3d4a63',
                'button_pressed': '#4a5568',
                'entry_bg': '#2d3748',
                'listbox_bg': '#1e2433',
                'listbox_fg': '#ffffff'
            }
        }
        
        self.current_theme = 'light'
        self.setup_themes()
    
    def setup_themes(self):
        button_padding = [10, 5, 10, 5]
        
        for theme_name in self.themes:
            theme = self.themes[theme_name]
            capitalized_name = theme_name.capitalize()
            
            self.style.configure(
                f'{capitalized_name}.TButton',
                background=theme['button_bg'],
                foreground=theme['fg'],
                borderwidth=0,
                focuscolor=theme['select_bg'],
                lightcolor=theme['button_bg'],
                darkcolor=theme['button_bg'],
                relief="flat",
                padding=button_padding,
                font=('Helvetica', 9)
            )
            
            self.style.map(
                f'{capitalized_name}.TButton',
                background=[('active', theme['button_hover']),
                           ('pressed', theme['button_pressed'])],
                relief=[('pressed', 'sunken')]
            )
            
            self.style.configure(f'{capitalized_name}.TFrame', background=theme['bg'])
            self.style.configure(f'{capitalized_name}.TLabel', 
                               background=theme['bg'], 
                               foreground=theme['fg'])
            self.style.configure(f'{capitalized_name}.TEntry', 
                               fieldbackground=theme['entry_bg'])
        
        self.setup_action_buttons()
    
    def setup_action_buttons(self):
        delete_colors = {
            'light': {'bg': '#ffcdd2', 'hover': '#ef9a9a', 'pressed': '#e57373', 'fg': '#000000'},
            'dark': {'bg': '#ef5350', 'hover': '#e53935', 'pressed': '#d32f2f', 'fg': '#000000'},
            'blue': {'bg': '#ef5350', 'hover': '#e53935', 'pressed': '#d32f2f', 'fg': '#000000'}
        }
        
        for theme_name in self.themes:
            capitalized_name = theme_name.capitalize()
            colors = delete_colors[theme_name]
            
            self.style.configure(
                f'Delete.{capitalized_name}.TButton',
                background=colors['bg'],
                foreground=colors['fg'],
                borderwidth=0,
                relief="flat",
                padding=[10, 5, 10, 5],
                font=('Helvetica', 9, 'bold')
            )
            
            self.style.map(
                f'Delete.{capitalized_name}.TButton',
                background=[('active', colors['hover']),
                           ('pressed', colors['pressed'])]
            )

    def toggle_theme(self, root, listbox):
        themes_order = ['light', 'dark', 'blue']
        current_index = themes_order.index(self.current_theme)
        next_index = (current_index + 1) % len(themes_order)
        self.current_theme = themes_order[next_index]
        
        theme = self.themes[self.current_theme]
        
        for widget in root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style=f'{self.current_theme.capitalize()}.TFrame')
            elif isinstance(widget, ttk.Label):
                widget.configure(style=f'{self.current_theme.capitalize()}.TLabel')
            elif isinstance(widget, ttk.Button):
                if 'Delete' in str(widget.cget('style')):
                    widget.configure(style=f'Delete.{self.current_theme.capitalize()}.TButton')
                else:
                    widget.configure(style=f'{self.current_theme.capitalize()}.TButton')
            elif isinstance(widget, ttk.Entry):
                widget.configure(style=f'{self.current_theme.capitalize()}.TEntry')
            
            if hasattr(widget, 'winfo_children'):
                self._apply_theme_to_children(widget)
        
        listbox.configure(
            bg=theme['listbox_bg'],
            fg=theme['listbox_fg'],
            selectbackground=theme['select_bg'],
            selectforeground=theme['select_fg']
        )
        
        root.configure(bg=theme['bg'])
    
    def _apply_theme_to_children(self, widget):
        for child in widget.winfo_children():
            if isinstance(child, ttk.Frame):
                child.configure(style=f'{self.current_theme.capitalize()}.TFrame')
            elif isinstance(child, ttk.Label):
                child.configure(style=f'{self.current_theme.capitalize()}.TLabel')
            elif isinstance(child, ttk.Button):
                if 'Delete' in str(child.cget('style')):
                    child.configure(style=f'Delete.{self.current_theme.capitalize()}.TButton')
                else:
                    child.configure(style=f'{self.current_theme.capitalize()}.TButton')
            elif isinstance(child, ttk.Entry):
                child.configure(style=f'{self.current_theme.capitalize()}.TEntry')
            
            if hasattr(child, 'winfo_children'):
                self._apply_theme_to_children(child)
