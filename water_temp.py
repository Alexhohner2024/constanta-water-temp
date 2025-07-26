import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import re
import threading
import time
from datetime import datetime

class WaterTempApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Температура воды - Констанца")
        self.root.geometry("300x250")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)
        
        # Переменные для хранения данных
        self.last_temp = None
        self.last_update_time = None
        
        self.setup_ui()
        self.auto_refresh()
        
    def setup_ui(self):
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)
        
        # Заголовок
        title_label = tk.Label(main_frame, 
                              text="🌊 Температура воды", 
                              font=('Segoe UI', 14, 'bold'), 
                              fg='#ffffff', 
                              bg='#1e1e1e')
        title_label.pack(pady=(0, 5))
        
        # Локация
        location_label = tk.Label(main_frame, 
                                 text="Констанца, Черное море", 
                                 font=('Segoe UI', 9), 
                                 fg='#a0a0a0', 
                                 bg='#1e1e1e')
        location_label.pack(pady=(0, 15))
        
        # Температура
        temp_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='flat', bd=1)
        temp_frame.pack(fill='x', pady=(0, 10))
        
        self.temp_label = tk.Label(temp_frame, 
                                  text="Загрузка...", 
                                  font=('Segoe UI', 20, 'bold'), 
                                  fg='#4CAF50', 
                                  bg='#2d2d2d')
        self.temp_label.pack(pady=15)
        
        # Статус и время обновления
        self.status_label = tk.Label(main_frame, 
                                    text="Получение данных...", 
                                    font=('Segoe UI', 8), 
                                    fg='#888888', 
                                    bg='#1e1e1e')
        self.status_label.pack(pady=(0, 5))
        
        self.time_label = tk.Label(main_frame, 
                                  text="", 
                                  font=('Segoe UI', 8), 
                                  fg='#666666', 
                                  bg='#1e1e1e')
        self.time_label.pack(pady=(0, 10))
        
        # Кнопка обновления
        refresh_btn = tk.Button(main_frame, 
                               text="🔄 Обновить", 
                               command=self.manual_refresh,
                               bg='#007ACC', 
                               fg='white', 
                               font=('Segoe UI', 11, 'bold'), 
                               relief='flat', 
                               padx=30, 
                               pady=10,
                               cursor='hand2')
        refresh_btn.pack()
        
        # Hover эффект для кнопки
        def on_enter(e):
            refresh_btn.config(bg='#005A9E')
        def on_leave(e):
            refresh_btn.config(bg='#007ACC')
            
        refresh_btn.bind("<Enter>", on_enter)
        refresh_btn.bind("<Leave>", on_leave)
        
    def get_water_temperature(self):
        try:
            url = "https://ro.seatemperature.net/current/romania/constanta"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            
            # Поиск температуры в тексте страницы
            patterns = [
                r'date actualizate acum \d+ de minute(\d+\.?\d*)°C',
                r'(\d+\.?\d*)\s*°C.*?ieri:',
                r'Astăzi temperatura apei în Constanța este (\d+\.?\d*)°C',
                r'temperatura apei în Constanța chiar acum.*?(\d+\.?\d*)°C'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    return float(match.group(1))
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None
        except Exception as e:
            print(f"Общая ошибка: {e}")
            return None
    
    def update_display(self, temp, error=False):
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if temp is not None:
            self.last_temp = temp
            self.last_update_time = current_time
            self.temp_label.config(text=f"{temp}°C", fg='#4CAF50')
            self.status_label.config(text="✅ Данные получены", fg='#4CAF50')
            self.time_label.config(text=f"Обновлено: {current_time}")
            
        elif error and self.last_temp is not None:
            # Показываем последнюю температуру с предупреждением
            self.temp_label.config(text=f"{self.last_temp}°C", fg='#FF9800')
            self.status_label.config(text="⚠️ Ошибка подключения", fg='#FF5722')
            self.time_label.config(text=f"Последние данные: {self.last_update_time}")
            
        else:
            self.temp_label.config(text="Нет данных", fg='#FF5722')
            self.status_label.config(text="❌ Не удалось получить данные", fg='#FF5722')
            self.time_label.config(text="")
    
    def refresh_temp(self, manual=False):
        def fetch():
            if manual:
                self.root.after(0, lambda: self.temp_label.config(text="Загрузка..."))
                self.root.after(0, lambda: self.status_label.config(text="Получение данных...", fg='#888888'))
            
            temp = self.get_water_temperature()
            
            if temp is not None:
                self.root.after(0, lambda: self.update_display(temp))
            else:
                self.root.after(0, lambda: self.update_display(None, error=True))
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def manual_refresh(self):
        self.refresh_temp(manual=True)
    
    def auto_refresh(self):
        self.refresh_temp()
        # Автообновление каждый час (3600000 мс)
        self.root.after(3600000, self.auto_refresh)

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterTempApp(root)
    root.mainloop()
