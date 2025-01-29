import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import webbrowser
import psutil
from theme_manager import ThemeManager
from help_window import HelpWindow

class WorkshopManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Legendoid'Z - PZ Mod Cleaner")
        self.root.geometry("800x600")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.theme_manager = ThemeManager()
        
        icon_path = os.path.join(os.path.dirname(__file__), "images", "icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        self.default_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\108600"
        self.current_path = self.default_path
        
        self.all_mods = []
        self.filtered_mods = []
        
        self.create_gui()
        self.check_folder()
        self.check_game_running()

    def create_gui(self):
        main_frame = ttk.Frame(self.root, padding="10", style='Light.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        top_button_frame = ttk.Frame(main_frame, style='Light.TFrame')
        top_button_frame.grid(row=0, column=0, pady=5, sticky=tk.W)
        
        ttk.Button(top_button_frame, text="📁 Changer de dossier", 
                  command=self.browse_folder, 
                  style='Light.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_button_frame, text="🌐 Workshop Steam", 
                  command=lambda: webbrowser.open('https://steamcommunity.com/app/108600/workshop/'),
                  style='Light.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_button_frame, text="❔ Aide",
                  command=lambda: HelpWindow(self.root),
                  style='Light.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_button_frame, text="🎨 Thème",
                  command=lambda: self.theme_manager.toggle_theme(self.root, self.folder_listbox),
                  style='Light.TButton').pack(side=tk.LEFT, padx=5)
        
        info_frame = ttk.Frame(main_frame, style='Light.TFrame')
        info_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.path_label = ttk.Label(info_frame, text=self.current_path, wraplength=500, style='Light.TLabel')
        self.path_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.counter_label = ttk.Label(info_frame, text="Mods : 0", font=('Helvetica', 10, 'bold'), style='Light.TLabel')
        self.counter_label.pack(side=tk.LEFT)
        
        search_frame = ttk.Frame(main_frame, style='Light.TFrame')
        search_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(search_frame, text="Rechercher :", style='Light.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_mods)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40, style='Light.TEntry')
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.steam_button = ttk.Button(search_frame, text="Ouvrir page Steam du mod", 
                                     command=self.open_steam_page, style='Light.TButton')
        self.steam_button.pack(side=tk.RIGHT, padx=5)
        
        self.folder_listbox = tk.Listbox(main_frame, selectmode=tk.EXTENDED, width=70, height=15, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.folder_listbox.yview)
        self.folder_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.folder_listbox.grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S))
        
        button_frame = ttk.Frame(main_frame, style='Light.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="🗑️ Supprimer la sélection", 
                  command=self.delete_selected,
                  style='Delete.Light.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🗑️ Tout supprimer",
                  command=self.delete_all,
                  style='Delete.Light.TButton').pack(side=tk.LEFT, padx=5)

    def filter_mods(self, *args):
        search_text = self.search_var.get().lower()
        self.folder_listbox.delete(0, tk.END)
        
        self.filtered_mods = [mod for mod in self.all_mods 
                            if search_text in mod['display_text'].lower()]
        
        for mod in self.filtered_mods:
            self.folder_listbox.insert(tk.END, mod['display_text'])
        
        self.counter_label.config(text=f"Mods : {len(self.filtered_mods)} / {len(self.all_mods)}")

    def open_steam_page(self):
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un mod")
            return
            
        mod_text = self.folder_listbox.get(selection[0])
        mod_id = mod_text.split()[0].strip()
        
        webbrowser.open(f'https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}')

    def check_game_running(self):
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] == 'ProjectZomboid64.exe':
                    messagebox.showwarning(
                        "Attention",
                        "Project Zomboid est en cours d'exécution.\n"
                        "Veuillez fermer le jeu avant de supprimer des mods."
                    )
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def check_folder(self):
        if not os.path.exists(self.current_path):
            response = messagebox.askyesno(
                "Dossier non trouvé",
                "Le dossier Steam Workshop n'a pas été trouvé à l'emplacement par défaut.\n"
                "Voulez-vous que je recherche le dossier sur le disque C: ?"
            )
            
            if response:
                found_path = self.find_workshop_folder("C:\\")
                if found_path:
                    self.current_path = found_path
                    self.path_label.config(text=self.current_path)
                    self.refresh_folder_list()
                else:
                    other_drives = self.get_available_drives()
                    other_drives.remove("C:\\")
                    
                    if other_drives and messagebox.askyesno(
                        "Continuer la recherche",
                        "Le dossier n'a pas été trouvé sur le disque C:.\n"
                        "Voulez-vous chercher sur les autres disques ?"
                    ):
                        for drive in other_drives:
                            found_path = self.find_workshop_folder(drive)
                            if found_path:
                                self.current_path = found_path
                                self.path_label.config(text=self.current_path)
                                self.refresh_folder_list()
                                break
                    
                    if not found_path:
                        if messagebox.askyesno(
                            "Dossier non trouvé",
                            "Le dossier n'a pas été trouvé automatiquement.\n"
                            "Voulez-vous sélectionner le dossier manuellement ?"
                        ):
                            self.browse_folder()
            else:
                self.browse_folder()
        else:
            self.refresh_folder_list()

    def get_available_drives(self):
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives

    def find_workshop_folder(self, start_path):
        target_folder = "108600"
        
        for root, dirs, _ in os.walk(start_path):
            if target_folder in dirs:
                workshop_path = os.path.join(root, target_folder)
                if "steamapps\\workshop\\content" in workshop_path:
                    return workshop_path
        return None

    def browse_folder(self):
        new_path = filedialog.askdirectory(title="Sélectionner le dossier Workshop")
        if new_path:
            self.current_path = new_path
            self.path_label.config(text=self.current_path)
            self.refresh_folder_list()

    def get_mod_name(self, folder_path):
        try:
            mods_path = os.path.join(folder_path, "mods")
            if os.path.exists(mods_path):
                for item in os.listdir(mods_path):
                    if os.path.isdir(os.path.join(mods_path, item)):
                        return item
        except Exception:
            pass
        return None

    def refresh_folder_list(self):
        self.folder_listbox.delete(0, tk.END)
        self.all_mods = []
        try:
            folders = [f for f in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, f))]
            
            for folder in folders:
                folder_path = os.path.join(self.current_path, folder)
                mod_name = self.get_mod_name(folder_path)
                display_text = f"{folder:<15}    |    {mod_name}" if mod_name else folder
                
                self.all_mods.append({
                    'id': folder,
                    'name': mod_name,
                    'display_text': display_text
                })
            
            self.filter_mods()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le contenu du dossier:\n{str(e)}")

    def delete_selected(self):
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un mod à supprimer")
            return
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer les mods sélectionnés ?"):
            for index in reversed(selection):
                folder_name = self.filtered_mods[index]['id']
                folder_path = os.path.join(self.current_path, folder_name)
                try:
                    shutil.rmtree(folder_path)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de supprimer {folder_name}:\n{str(e)}")
            
            self.refresh_folder_list()

    def delete_all(self):
        if not os.path.exists(self.current_path):
            messagebox.showerror("Erreur", "Le dossier Workshop n'existe pas")
            return
        
        if messagebox.askyesno("Confirmation", 
                              "Êtes-vous sûr de vouloir supprimer TOUS les mods ?\n"
                              "Cette action est irréversible!"):
            try:
                folders = [f for f in os.listdir(self.current_path) 
                          if os.path.isdir(os.path.join(self.current_path, f))]
                
                for folder in folders:
                    folder_path = os.path.join(self.current_path, folder)
                    try:
                        shutil.rmtree(folder_path)
                    except Exception as e:
                        messagebox.showerror("Erreur", f"Impossible de supprimer {folder}:\n{str(e)}")
                
                self.refresh_folder_list()
                messagebox.showinfo("Succès", "Tous les mods ont été supprimés")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue:\n{str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = WorkshopManager(root)
    root.mainloop()
