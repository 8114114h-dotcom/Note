import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from datetime import datetime
from plyer import notification # مكتبة الإشعارات

class StudyTimerApp(App):
    def build(self):
        self.tasks = []
        self.load_tasks()
        
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # واجهة الإدخال
        input_area = BoxLayout(size_hint_y=None, height=120, orientation='vertical', spacing=5)
        self.task_input = TextInput(hint_text='اسم المادة (مثال: فيزياء)', multiline=False)
        self.time_input = TextInput(hint_text='الوقت (مثال: 18:30)', multiline=False)
        add_btn = Button(text='إضافة للمهامات', background_color=(0, 0.7, 0, 1), on_release=self.add_task)
        
        input_area.add_widget(self.task_input)
        input_area.add_widget(self.time_input)
        input_area.add_widget(add_btn)
        
        self.root.add_widget(Label(text="منظم دراستي", size_hint_y=None, height=50, font_size=28))
        self.root.add_widget(input_area)
        
        self.task_list = RecycleView()
        self.root.add_widget(self.task_list)
        
        Clock.schedule_interval(self.check_alarms, 10) # فحص كل 10 ثوانٍ
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
        self.task_list.data = [{'text': f"⏰ {t['time']} - {t['text']}"} for t in self.tasks]

    def check_alarms(self, dt):
        now = datetime.now().strftime("%H:%M")
        for task in self.tasks:
            if task['time'] == now:
                notification.notify(
                    title="حان وقت الدراسة!",
                    message=f"لديك الآن: {task['text']}",
                    app_name="StudyPlanner",
                    timeout=20 # مدة ظهور الإشعار
                )

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except: self.tasks = []

if __name__ == '__main__':
    StudyTimerApp().run()
