import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class HelpWindow:
    def __init__(self, parent):
        self.help_window = tk.Toplevel(parent)
        self.help_window.title("Aide - Workshop Manager")
        self.help_window.geometry("800x700")
        
        icon_path = os.path.join(os.path.dirname(__file__), "images", "icon.ico")
        if os.path.exists(icon_path):
            self.help_window.iconbitmap(icon_path)
        
        main_frame = ttk.Frame(self.help_window, padding="20", style='Light.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, 
                              text="Guide de première connexion",
                              font=('Helvetica', 14, 'bold'), style='Light.TLabel')
        title_label.pack(pady=(0, 20))
        
        help_text = ("Pour une première connexion au serveur il est recommandé de :\n\n"
                    "- Tout supprimer via PZ Mod Cleaner\n"
                    "- Se désabonner de tout les articles")
        
        text_label = ttk.Label(main_frame, text=help_text, 
                              font=('Helvetica', 11), style='Light.TLabel',
                              justify=tk.LEFT,
                              wraplength=750)
        text_label.pack(pady=(0, 20))
        
        top_image_frame = ttk.Frame(main_frame, style='Light.TFrame')
        top_image_frame.pack(fill=tk.X, pady=(0, 20))
        
        bottom_image_frame = ttk.Frame(main_frame, style='Light.TFrame')
        bottom_image_frame.pack(fill=tk.BOTH, expand=True)
        
        try:
            img3_path = os.path.join(os.path.dirname(__file__), "images", "img3.png")
            if os.path.exists(img3_path):
                img3 = Image.open(img3_path)
                original_width, original_height = img3.size
                target_width = 600
                ratio = target_width / original_width
                target_height = int(original_height * ratio)
                img3 = img3.resize((target_width, target_height), Image.Resampling.LANCZOS)
                photo3 = ImageTk.PhotoImage(img3)
                
                img3_frame = ttk.Frame(top_image_frame, style='Light.TFrame')
                img3_frame.pack(expand=True)
                img3_label = ttk.Label(img3_frame, image=photo3, style='Light.TLabel')
                img3_label.image = photo3
                img3_label.pack()
                ttk.Label(img3_frame, text="Erreur typique", font=('Helvetica', 10, 'bold'), style='Light.TLabel').pack()
            
            img1_path = os.path.join(os.path.dirname(__file__), "images", "img1.png")
            if os.path.exists(img1_path):
                img1 = Image.open(img1_path)
                img1 = img1.resize((350, 200), Image.Resampling.LANCZOS)
                photo1 = ImageTk.PhotoImage(img1)
                
                img1_frame = ttk.Frame(bottom_image_frame, style='Light.TFrame')
                img1_frame.pack(side=tk.LEFT, padx=10, expand=True)
                img1_label = ttk.Label(img1_frame, image=photo1, style='Light.TLabel')
                img1_label.image = photo1
                img1_label.pack()
                ttk.Label(img1_frame, text="Acticles abonnés", font=('Helvetica', 10, 'bold'), style='Light.TLabel').pack()
            
            img2_path = os.path.join(os.path.dirname(__file__), "images", "img2.png")
            if os.path.exists(img2_path):
                img2 = Image.open(img2_path)
                img2 = img2.resize((350, 200), Image.Resampling.LANCZOS)
                photo2 = ImageTk.PhotoImage(img2)
                
                img2_frame = ttk.Frame(bottom_image_frame, style='Light.TFrame')
                img2_frame.pack(side=tk.LEFT, padx=10, expand=True)
                img2_label = ttk.Label(img2_frame, image=photo2, style='Light.TLabel')
                img2_label.image = photo2
                img2_label.pack()
                ttk.Label(img2_frame, text="Se désabonner de tout", font=('Helvetica', 10, 'bold'), style='Light.TLabel').pack()
                
        except Exception as e:
            error_label = ttk.Label(bottom_image_frame, 
                                  text=f"Erreur lors du chargement des images : {str(e)}", 
                                  font=('Helvetica', 10), style='Light.TLabel',
                                  foreground='red')
            error_label.pack(pady=20)
