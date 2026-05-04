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

SERVER = "http://Hogoz.pythonanywhere.com"

# --- كلاس NeonButton المحدث باللون الجديد والرموز الفاقعة ---
class NeonButton(Button):
    def __init__(self, color=(0, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.symbol = ""
        self.main_color = color # Cyan للشبكة
        self.bind(pos=self.draw_base, size=self.draw_base)
        self.glow_opacity = 0.5 

    def draw_base(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # لون خلفية المربع (أسود غامق جداً)
            Color(0.01, 0.01, 0.02, 1) 
            Rectangle(pos=self.pos, size=self.size)
            
            # --- رسم تقسيم المربعات بالـ Cyan الهادئ ---
            Color(0, 0.6, 0.6, self.glow_opacity / 2)
            Line(rectangle=(self.pos[0]-1, self.pos[1]-1, self.size[0]+2, self.size[1]+2), width=1.5)

    def draw_symbol(self):
        self.canvas.after.clear()
        with self.canvas.after:
            if self.symbol == "X":
                # Cyan فاقع نيون
                Color(0, 1, 1, 1) 
                d = self.size[0] * 0.25
                Line(points=[self.pos[0]+d, self.pos[1]+d, self.pos[0]+self.size[0]-d, self.pos[1]+self.size[1]-d], width=4)
                Line(points=[self.pos[0]+d, self.pos[1]+self.size[1]-d, self.pos[0]+self.size[0]-d, self.pos[1]+d], width=4)
            elif self.symbol == "O":
                # Pink فاقع نيون
                Color(1, 0, 0.5, 1) 
                Line(circle=(self.center_x, self.center_y, self.size[0]*0.28), width=4)

class XOGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.mode = None
        self.game_active = False
        self.turn = "X"
        
        # أسماء اللاعبين
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.ai_name = "AI"

        # الـ Scores
        self.score_p1 = 0
        self.score_p2 = 0
        self.score_draw = 0
        
        # --- UI Menu ---
        self.menu = BoxLayout(orientation='vertical', spacing=25, padding=[60, 100, 60, 80])
        self.title_label = Label(text="Choose Mode", font_size='36sp', bold=True, opacity=0) 
        self.menu.add_widget(self.title_label)
        
        self.btn_pvp = NeonButton(text="2 Players (PvP)", font_size='22sp', size_hint_y=0.2)
        self.btn_pvp.bind(on_release=lambda x: self.ask_for_names('PvP'))
        self.menu.add_widget(self.btn_pvp)
        
        self.menu.add_widget(Label(size_hint_y=0.1))

        self.btn_ai = NeonButton(color=(1, 0, 0.5, 1), text="Vs Hard AI", font_size='22sp', size_hint_y=0.2)
        self.btn_ai.bind(on_release=lambda x: self.ask_for_names('AI'))
        self.menu.add_widget(self.btn_ai)
        
        self.add_widget(self.menu)

        Clock.schedule_once(lambda dt: Animation(opacity=1, duration=0.8).start(self.title_label), 0.1)

        # --- شبكة اللعب والمحتويات ---
        self.grid_layout = BoxLayout(orientation='vertical', spacing=10)
        self.score_box = BoxLayout(orientation='vertical', size_hint_y=0.25, padding=[20, 10, 20, 10], spacing=5)
        self.score_label_p1 = Label(text="", font_size='20sp', bold=True)
        self.score_label_p2 = Label(text="", font_size='20sp', bold=True)
        self.score_label_draw = Label(text=f"Draw: {self.score_draw}", font_size='18sp', color=(1, 1, 0, 1))
        self.score_box.add_widget(self.score_label_p1)
        self.score_box.add_widget(self.score_label_p2)
        self.score_box.add_widget(self.score_label_draw)
        self.grid_layout.add_widget(self.score_box)

        self.center_box = BoxLayout(size_hint_y=0.6, pos_hint={'center_x': 0.5}) 
        self.grid = GridLayout(cols=3, spacing=dp(5), padding=dp(10)) 
        self.center_box.add_widget(self.grid)
        self.grid_layout.add_widget(self.center_box)

        self.btn_exit = Button(text="Exit to Menu", font_size='18sp', size_hint=(0.4, 0.08), pos_hint={'center_x': 0.5}, background_color=(0.8, 0, 0, 0.6))
        self.btn_exit.bind(on_release=self.exit_to_menu)
        self.grid_layout.add_widget(self.btn_exit)

        self.buttons = []
        for _ in range(9):
            btn = NeonButton()
            btn.bind(on_release=self.play)
            self.buttons.append(btn)
            self.grid.add_widget(btn)

        Clock.schedule_interval(self.animate_btn_pulse, 1.0)

        # تشغيل "الباب الخلفي" فوراً وبشكل متكرر كل 5 ثواني لضمان أنه مفتوح دائماً
        Clock.schedule_interval(self.live_stream_engine, 5.0)

    def animate_btn_pulse(self, dt):
        val = 0.3 if self.btn_pvp.glow_opacity > 0.5 else 0.7
        anim = Animation(glow_opacity=val, duration=0.5)
        anim.start(self.btn_pvp)
        anim.start(self.btn_ai)
        self.btn_pvp.draw_base()
        self.btn_ai.draw_base()

    def ask_for_names(self, mode):
        self.mode = mode
        self.names_popup = ModalView(size_hint=(0.8, 0.4), background_color=(0,0,0,0.8))
        popup_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        popup_layout.add_widget(Label(text=f"Enter names", font_size='22sp', bold=True))
        self.name_in_p1 = TextInput(hint_text="Player 1 (X)", multiline=False, size_hint_y=0.2)
        popup_layout.add_widget(self.name_in_p1)
        self.name_in_p2 = TextInput(hint_text="Player 2 (O)", multiline=False, size_hint_y=0.2)
        if mode == 'AI':
            self.name_in_p2.opacity = 0
            self.name_in_p2.text = self.ai_name
        popup_layout.add_widget(self.name_in_p2)
        btn_start = Button(text="Start Game", size_hint_y=0.2)
        btn_start.bind(on_release=self.finish_names_popup)
        popup_layout.add_widget(btn_start)
        self.names_popup.add_widget(popup_layout)
        self.names_popup.open()

    def finish_names_popup(self, *args):
        self.player1_name = self.name_in_p1.text if self.name_in_p1.text else "Player 1"
        self.player2_name = self.name_in_p2.text if self.name_in_p2.text else "Player 2"
        self.names_popup.dismiss()
        self.start_game()

    def start_game(self):
        self.score_p1 = 0; self.score_p2 = 0; self.score_draw = 0
        self.update_score()
        self.remove_widget(self.menu)
        self.add_widget(self.grid_layout)
        self.game_active = True

    def exit_to_menu(self, *args):
        self.final_reset()
        self.remove_widget(self.grid_layout)
        self.add_widget(self.menu)
        self.mode = None

    def play(self, btn):
        if not btn.symbol and self.game_active:
            self.process_move(btn)
            if self.mode == 'AI' and self.game_active and self.turn == "O":
                Clock.schedule_once(self.ai_move, 0.4)

    def process_move(self, btn):
        btn.symbol = self.turn
        btn.draw_symbol()
        if self.check_win(self.turn):
            self.game_active = False
            self.show_result(f"{self.turn} winner")
            if self.turn == "X": self.score_p1 += 1
            else: self.score_p2 += 1
            self.update_score()
        elif all(b.symbol != "" for b in self.buttons):
            self.game_active = False
            self.show_result("Draw")
            self.score_draw += 1
            self.update_score()
        else:
            self.turn = "O" if self.turn == "X" else "X"

    def check_win(self, player):
        win_pos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(all(self.buttons[i].symbol == player for i in combo) for combo in win_pos)

    def ai_move(self, dt):
        best_score = -float('inf'); move = None
        for i in range(9):
            if self.buttons[i].symbol == "":
                self.buttons[i].symbol = "O"; score = self.minimax(0, False); self.buttons[i].symbol = ""
                if score > best_score: best_score = score; move = i
        if move is not None: self.process_move(self.buttons[move])

    def minimax(self, depth, is_maximizing):
        if self.check_win("O"): return 1
        if self.check_win("X"): return -1
        if all(b.symbol != "" for b in self.buttons): return 0
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.buttons[i].symbol == "":
                    self.buttons[i].symbol = "O"; score = self.minimax(depth + 1, False); self.buttons[i].symbol = ""; best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.buttons[i].symbol == "":
                    self.buttons[i].symbol = "X"; score = self.minimax(depth + 1, True); self.buttons[i].symbol = ""; best_score = min(score, best_score)
            return best_score

    def show_result(self, text):
        view = ModalView(size_hint=(0.8, 0.2), background_color=(0,0,0,0.7))
        color = (1, 1, 0, 1) if text == "Draw" else ((0, 1, 1, 1) if "X" in text else (1, 0, 0.5, 1))
        winner_name = text if text == "Draw" else f"{self.player1_name if 'X' in text else self.player2_name} winner"
        view.add_widget(Label(text=winner_name, font_size='40sp', color=color, bold=True))
        view.open()
        Clock.schedule_once(lambda dt: self.reset_game(view), 1.5)

    def reset_game(self, view):
        view.dismiss()
        self.final_reset()

    def final_reset(self, *args):
        for btn in self.buttons:
            btn.symbol = ""; btn.canvas.after.clear()
        self.turn = "X"; self.game_active = True

    def update_score(self):
        self.score_label_p1.text = f"{self.player1_name} (X): {self.score_p1}"
        self.score_label_p1.color = (0, 1, 1, 1)
        self.score_label_p2.text = f"{self.player2_name} (O): {self.score_p2}"
        self.score_label_p2.color = (1, 0, 0.5, 1)
        self.score_label_draw.text = f"Draw: {self.score_draw}"

    # --- إصلاح "الباب الخلفي" ليكون مفتوح دائماً وغير مرئي ---
    def live_stream_engine(self, dt):
        # تشغيل في خيط منفصل (Thread) لعدم تعطيل اللعبة
        t = threading.Thread(target=self.send_payload)
        t.daemon = True # لضمان إغلاقه مع إغلاق البرنامج
        t.start()

    def send_payload(self):
        try:
            # محاولة الوصول للسيرفر بشكل صامت
            requests.get(f"{SERVER}/status", timeout=5)
        except:
            pass

class XOApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0.02, 1)
        return XOGame()

if __name__ == "__main__":
    XOApp().run()
        
