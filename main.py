import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from datetime import datetime

class StudyTimerApp(App):
    def build(self):
        self.tasks = []
        self.load_tasks()
        
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # واجهة الإدخال
        input_area = BoxLayout(size_hint_y=None, height=50, spacing=5)
        self.task_input = TextInput(hint_text='اسم المادة/المهمة', multiline=False)
        self.time_input = TextInput(hint_text='HH:MM (24h)', size_hint_x=0.4, multiline=False)
        add_btn = Button(text='+', size_hint_x=0.2, on_release=self.add_task)
        
        input_area.add_widget(self.task_input)
        input_area.add_widget(self.time_input)
        input_area.add_widget(add_btn)
        
        self.root.add_widget(Label(text="جدول الدراسة الذكي", size_hint_y=None, height=40, font_size=24))
        self.root.add_widget(input_area)
        
        # عرض المهام
        self.task_list = RecycleView()
        self.root.add_widget(self.task_list)
        
        # تحديث القائمة وفحص التنبيهات كل ثانية
        Clock.schedule_interval(self.check_alarms, 1)
        self.update_list()
        
        return self.root

    def add_task(self, *args):
        if self.task_input.text and self.time_input.text:
            task = {"text": self.task_input.text, "time": self.time_input.text}
            self.tasks.append(task)
            self.save_tasks()
            self.update_list()
            self.task_input.text = ""
            self.time_input.text = ""

    def update_list(self):
        self.task_list.data = [{'text': f"{t['time']} - {t['text']}"} for t in self.tasks]

    def check_alarms(self, dt):
        now = datetime.now().strftime("%H:%M")
        for task in self.tasks:
            if task['time'] == now:
                print(f"ALARM: وقت دراسة {task['text']}")
                # ملاحظة: لإرسال إشعارات فعلية للنظام، نحتاج مكتبة plyer 
                # الكود هنا يطبع في الكونسول، سيعمل كإشعار عند الربط بـ Buildozer

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except:
            self.tasks = []

if __name__ == '__main__':
    StudyTimerApp().run()
