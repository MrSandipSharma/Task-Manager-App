from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

kv = """
<TaskDetails>:
    orientation: "vertical"
    radius: 15
    spacing: 12
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: TaskName
        hint_text: "Write Your Task here!"
        line_anim: True
        text_color_normal: 1,1,1,1
        text_color_focus: 1,1,1,1
        line_color_normal: 1,1,1,1
        hint_text_color_normal: 1,1,1,1
        hint_text_color_focus: 1,1,1,1
        line_color_focus: 1,1,1,1

    MDTextField:
        id: TaskDesc
        hint_text: "Write Description here!"
        line_anim: True
        text_color_normal: 1,1,1,1
        text_color_focus: 1,1,1,1
        line_color_normal: 1,1,1,1
        hint_text_color_normal: 1,1,1,1
        hint_text_color_focus: 1,1,1,1
        line_color_focus: 1,1,1,1


<Task>:
    size_hint_y: None
    height: content.height
    MDCardSwipeLayerBox:
        padding: "8dp"
        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y":.5}
            icon_size: 50
            theme_icon_color: "Custom"
            icon_color: 1,0,0,1
            on_press: app.removeItem(root, content.text)

    MDCardSwipeFrontBox:
        TwoLineListItem:
            id: content
            text: root.text
            font_style: "H4"
            secondary_text: root.secondary_text
            _no_ripple_effect: True

            MDIconButton:
                icon: "checkbox-marked-circle-outline"
                pos_hint: {"center_x": .9, "center_y": .5}
                # md_bg_color: 69/255,55/255,86/255,1
                icon_size: 35
                on_press: app.doneTask(root, content.text, content.secondary_text)

MDScreenManager:
    MDScreen:
        name: "Home"
        MDBoxLayout:
            orientation: "vertical"
            MDTopAppBar:
                title: "Astro Task Manager"
                md_bg_color: 69/255,55/255,86/255,1
                size_hint: 1, .15
                elevation: 0
                left_action_items: [["menu"]]
                right_action_items: [["checkbox-marked-circle-outline", lambda x: app.ChangeScreen()]]
    
            MDScrollView:
                MDList:
                    spacing: 5
                    id: item
        
        MDFloatLayout:
            MDIconButton:
                icon: "plus"
                pos_hint: {"center_x":.9, "center_y": .08}
                md_bg_color: 69/255,55/255,86/255,1
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1
                icon_size: 35
                on_press: app.AddItem()

    MDScreen:
        name: "Complete"
        MDBoxLayout:
            orientation: "vertical"
            MDTopAppBar:
                title: "Completed Tasks"
                md_bg_color: 69/255,55/255,86/255,1
                elevation: 0
                size_hint: 1, .13
                left_action_items: [["arrow-left", lambda x: app.BackMenu()]]

            MDScrollView:
                MDList:
                    spacing: 5
                    id: itemComplete
        

"""

class Task(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()

class TaskDetails(MDBoxLayout):
    pass

class ToDoList(MDApp):
    dialog = None
    back_button_press_counter1=NumericProperty(0)
    back_button_press_counter = ObjectProperty()
    def build(self):
        Window.bind(on_keyboard=self._key_handler)
        return Builder.load_string(kv)

    def _key_handler(self, instance, key, *args):
        if key is 27:
            if self.root.current == 'Home':
                if self.back_button_press_counter1==1:
                    self.stop()
                else:
                    Snackbar(text="Press again to exit", duration=.5).open()
                    self.back_button_press_counter1+=1
                return True
            elif self.root.current == 'Complete':
                self.root.current = 'Home'
                self.root.transition.direction = "down"
                return True

    def new(self, Name):
        self.root.ids.item.add_widget(Task(text= Name))

    def removeItem(self, instance, Task):
        self.root.ids.item.remove_widget(instance)
        self.root.ids.itemComplete.remove_widget(instance)
        toast(f"{Task} Task Deleted..")

    def AddItem(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='[color=ffffff]Add New Task[/color]',
                type= "custom",
                radius=[20, 7, 20, 7],
                md_bg_color= (69/255,55/255,86/255,1),
                content_cls=TaskDetails(),
                buttons=[
                    MDRaisedButton(
                        text= "CANCEL",
                        md_bg_color= (1,0,0,1),
                        on_press= self.CancelNewTask
                        ),
                    MDRaisedButton(
                        text= "Add Task",
                        on_press= self.AddNewTask
                        ),
                ],
            )
        self.dialog.open()

    def AddNewTask(self, l):
        Name = self.dialog.content_cls.ids.TaskName.text
        Desc = self.dialog.content_cls.ids.TaskDesc.text
        if Name == "" or Desc == "":
            toast('Something went wrong..')
            self.dialog.content_cls.ids.TaskName.text = ""
            self.dialog.content_cls.ids.TaskDesc.text = ""
            self.dialog.dismiss()
        else:
            self.root.ids.item.add_widget(Task(text= f"{Name}",
                                        secondary_text= f"{Desc}"))
            self.dialog.content_cls.ids.TaskName.text = ""
            self.dialog.content_cls.ids.TaskDesc.text = ""
            toast('New Task Added Successfully')
            self.dialog.dismiss()

    def CancelNewTask(self, l):
        self.dialog.dismiss()

    def ChangeScreen(self):
        self.root.current = "Complete"
        self.root.transition.direction = "up"

    def BackMenu(self):
        self.root.current = "Home"
        self.root.transition.direction = "down"

    def doneTask(self, instance, Name, Desc):
        if self.root.current == "Home":
            self.root.ids.item.remove_widget(instance)
            self.root.ids.itemComplete.add_widget(Task(text= f"{Name}",
                                            secondary_text= f"{Desc}"))
            toast(f"{Name} Task Complete..")
        else:
            self.root.ids.itemComplete.remove_widget(instance)
            self.root.ids.item.add_widget(Task(text= f"{Name}",
                                            secondary_text= f"{Desc}"))
            toast(f"{Name} again Task Added..")


ToDoList().run()