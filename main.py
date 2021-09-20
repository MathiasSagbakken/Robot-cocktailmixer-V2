from kivy.app import App
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.clock import mainthread
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.vkeyboard import VKeyboard
from kivy.loader import Loader
from read_json import valid_cocktails
from measurement_conversion import metric
import json
from time import sleep
import threading
from kivy.core.text import LabelBase
from kivy.graphics import Rectangle, Color
from kivy.uix.textinput import TextInput
from kivy.config import Config
import requests
import re
from drink_order_config import drink_order
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.animation import Animation
from multiprocessing import Process
from kivy.uix.popup import Popup
import serial
import time
#from kivy.core.window import WindowBase
#serialcomm = serial.Serial('COM4', 9600)
#serialcomm.timeout = 1
Window.size = (800, 480)
#Window.fullscreen = True
ready = True
#WindowBase.request_keyboard()

LabelBase.register(name='loop',
                   fn_regular='QuarkcheesePersonaluse-0Wlpr.otf')

def dictstr(dict, dict2, dl):
    tekst = ""
    for i in dict:
        tekst += i["name"]+":   "+str(i["measure"])+"\n"
    tekst +="\n"+"("+dict2+")"
    msr=0
    for i in dl:
        if i["measure"] != "ignore":
            msr += i["measure"]
    tekst +="\n"+str((msr*3)/10)+" dl"
    return tekst

def recepie_names(dict, all_ing):
    ing_list = []
    new_list = []
    for ing in dict:
        ing_list.append(ing["name"])
    for j in range(len(all_ing)):
        r = [l for l, item in enumerate(ing_list) if re.search(r"\b%s\b" % str(all_ing[j]), item)]
        if len(r) > 0:
            new_list.append(all_ing[j])
    return new_list

def press_callback(obj):
    pass

def btn_active(obj):
    obj.opacity=0.5
def btn_deactive(obj):
    obj.opacity = 1

class actionbar_window(Screen):
    def __init__(self, **kwargs):
        super(actionbar_window, self).__init__(**kwargs)

class Menu_screen(Screen):
    def __init__(self, **kwargs):
        super(Menu_screen, self).__init__(**kwargs)

    def screen_transition(self, *args):
        self.manager.current = 'screen1'

class Ingredients_screen(Screen):
    def __init__(self, **kwargs):
        super(Ingredients_screen, self).__init__(**kwargs)

    def screen_transition(self, *args):
        self.manager.current = 'screen2'

class add_cocktail(Screen):
    def __init__(self, **kwargs):
        super(add_cocktail, self).__init__(**kwargs)

    def screen_transition(self, *args):
        self.manager.current = 'screen3'

class remove_cocktail(Screen):
    def __init__(self, **kwargs):
        super(remove_cocktail, self).__init__(**kwargs)

    def screen_transition(self, *args):
        self.manager.current = 'screen4'

class making_cocktail(Screen):
    def __init__(self, **kwargs):
        super(making_cocktail, self).__init__(**kwargs)

    def screen_transition(self, *args):
        self.manager.current = 'screen5'

#class WindowManager(ScreenManager):
#    def __init__(self, **kwargs):
#        super(WindowManager, self).__init__(**kwargs)

Builder.load_file("main_design.kv")
Builder.load_string('''
#:import C kivy.utils.get_color_from_hex
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    name: "setup"
    id : "rv"
    viewclass: 'CycleBars'
    SelectableRecycleBoxLayout:
        default_size: None, dp(200)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<MyButton>
	background_normal: ''
    canvas.before:
        Color:
            rgba: C("#20444F")
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: (234/255, 70/255, 159/255,1)
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height

''')

Builder.load_string('''
#:import C kivy.utils.get_color_from_hex
<CycleBars>:
    id: grid
    canvas.before:
        Color:
            rgba: C("#000000")
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: C("#20444F")
        Line:
            width: 2
            rectangle: self.x+10, self.y, self.width-20, self.height
''')


class Drinkbtn(ButtonBehavior,AsyncImage):
    pass

class ScreenButton(ButtonBehavior):
    pass

class Circle_animation(BoxLayout):
    pass

class CountDownLbl(Label):
    time_counter = NumericProperty(0)
    angle = NumericProperty(0)

    def start(self, value, *args):
        Animation.cancel_all(self)
        self.time_counter = value
        self.drawing = Animation(angle=360 * self.time_counter - 1,  duration=self.time_counter)
        self.drawing.bind(on_complete=self.finish)
        self.drawing.start(self)

    def finish(self, animation, incr_crude_clock):
        incr_crude_clock.text = "Your drink is up"

    def reset(self, *args):
        self.time_counter = 0
        self.angle = 0
        self.drawing = None

    def cancel_all(widget, *largs):
        if len(largs):
            for animation in list(Animation._instances):
                for x in largs:
                    animation.cancel_property(widget, x)
        else:
            for animation in set(Animation._instances):
                animation.cancel(widget)

Builder.load_string("""
#:import C kivy.utils.get_color_from_hex
<Circle_animation>:
    orientation: "vertical"
    CountDownLbl:
        id: draw_label
        text: str(int(self.time_counter - self.angle // 360))
        font_size: 30
        canvas:
            Color:
                rgb: (234/255, 70/255, 159/255,1)
            Line:
                circle:self.center_x, self.center_y, 130, 0, self.angle % 360
                width: 5
""")

class CycleBars(GridLayout, RecycleDataViewBehavior):

    def __init__(self, **kwargs):
        super(CycleBars, self).__init__(**kwargs)
        self.text = ""
        self.size = (800,200)
        self.pos_hint = {'left': 1}
        self.cols = 3
        self.size_hint = (None, None)
        self.padding = 5,5
        self.border = (5,5,5,5)
        self.drink_order = []
        self.recepie = []
        self.ready = True
        self.popup = Popup(title='Make cocktail or cancel',
        content=DoubleButton(),
        size_hint=(None, None), size=(400, 200))
        self.popup.children[0].children[0].children[0].pos_hint={'center_x': 0.1, "center_y": .1}
        self.popup.children[0].children[0].children[0].children[0].bind(on_release=self.popup.dismiss)
        self.popup.children[0].children[0].children[0].children[1].bind(on_release=self.makeDrink)
        bilde = Drinkbtn(source="bilde_test.jpg")
        btn = Button(text ="Push Me !",
                   background_normal = "bilde_test.jpg",
                   color =(1, 1, 1, 1),
                   size =(self.height, self.height),
                   size_hint =(None, None))
        self.add_widget(bilde)
        l1= Label(text="Det var en gang....")
        l2 = Label(text="Det var en gang....")
        self.ids['lbl1'] = l1
        self.ids['lbl2'] = l2
        self.add_widget(l1)
        self.add_widget(l2)


    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.volume = data["measure"]
        self.jsondata = data["jsondata"]
        self.screen_list = data["screens"]
        self.children[0].text = data["l1"]
        self.children[1].text = data["l2"]
        self.children[2].source = data["img"]
        self.children[2].text = data["btntxt"]
        self.children[2].bind(on_release=press_callback)
        self.children[2].bind(on_press=self.img_feedback1)
        self.children[2].bind(on_release=self.img_feedback2)
        self.drink_order = data["ingredients"]
        self.recepie = data["recepie"]
        self.indexes, self.volume = drink_order(self.drink_order, self.recepie, self.jsondata)
        self.children[2].bind(on_release=self.popup.open)
        self.motorData = self.indexes+self.volume
        return super(CycleBars, self).refresh_view_attrs(
            rv, index, data)

    def img_feedback1(self, *args):
        self.opacity = .5
        threading.Timer(.5, self.img_feedback2).start()
    def img_feedback2(self, *args):
        self.opacity = 1

    def sendDataToArduino(self, *args):
        #serialcomm = serial.Serial('COM4', 9600)
        #serialcomm.timeout = 1
        letters = ""
        for s in self.motorData:
            letters += str(s)+","
        letters = letters[:-1]
        time.sleep(2)
        #serialcomm.write(letters.encode())
        #serialcomm.close()

    def makeDrink(self, *args):
        self.popup.dismiss()
        self.screen_list[1].screen_transition()
        teller = 0
        for i in self.volume:
            tid = i
            while tid > 0:
                teller += 1
                tid -= 1
        #teller = teller*8+3+8
        threading.Timer(0, self.sendDataToArduino).start()
        self.screen_list[1].children[0].children[0].start(teller)

        Clock.schedule_once(self.screen_list[0].screen_transition, teller+5)
        Clock.schedule_once(self.screen_list[1].children[0].children[0].cancel_all, teller+5)
        Clock.schedule_once(self.screen_list[1].children[0].children[0].reset, teller+5)
        #Clock.schedule_once(self.remove_animation, teller+6)


    def remove_animation(self, *args):
        self.screen_list[1].remove_widget(self.animasjon)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''




class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)+""} for x in range(5)]

class StaticButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(StaticButton, self).__init__(**kwargs)
        self.opacity = 0

class DoubleButton(BoxLayout):
    def __init__(self, **kwargs):
        super(DoubleButton, self).__init__(**kwargs)
        self.cols = 2
        self.padding = 75
        self.spacing = 30
        Button1 = MyButton()
        Button2 = MyButton()
        lbl1 = Label(text="Make Cocktail")
        lbl2 = Label(text="Cancel")
        Button1.add_widget(lbl1)
        Button2.add_widget(lbl2)
        Button1.bind(on_press=btn_active)
        Button1.bind(on_release=btn_deactive)
        Button2.bind(on_press=btn_active)
        Button2.bind(on_release=btn_deactive)
        self.add_widget(Button1)
        self.add_widget(Button2)
        self.opacity = 1
        self.size_hint = (None, None)
        self.size = (200,100)
        self.font_size ="18sp"


class MyButton(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.opacity = 1
        self.size_hint = (None, None)
        self.size = (100,50)
        self.text = "Add"
        self.font_size ="20sp"

    def on_press(self):
        pass

    def on_release(self):
        pass

#kv = Builder.load_file('design.kv')

class SampleApp(App):
    def build(self):

        self.teller = []
        self.str1 = []
        f = open('cocktail_data.json',)
        self.json_data = json.load(f)
        self.liste = []
        self.liste = ["Vodka", "Ginger beer", "Lime", "Cranberry juice", "Triple sec", "Orange juice", "Lemon", "salt"]
        layout1 = RelativeLayout(size = (800,480), size_hint=(None, None))
        layout2 = RelativeLayout(size = (800,480), size_hint=(None, None))
        layout3 = RelativeLayout(size = (800,480), size_hint=(None, None))
        layout4 = RelativeLayout(size = (800,480), size_hint=(None, None))
        layout5 = RelativeLayout(size = (800,480), size_hint=(None, None))

        bar = actionbar_window()
        root = bar.ids.sm
        self.scrn1 = Menu_screen(name='screen1')
        self.scrn2 = Ingredients_screen(name='screen2')
        scrn3 = add_cocktail(name='screen3')
        self.scrn4 = remove_cocktail(name='screen4')
        self.scrn5 = making_cocktail(name='screen5')

        self.animasjon = Circle_animation()
        layout5.add_widget(StaticButton(size = (800,480), size_hint=(None, None)))
        self.scrn5.add_widget(layout5)
        self.scrn5.add_widget(self.animasjon)

        btn = MyButton()
        self.scroll = RV(size = (800,390), size_hint=(None, None))
        keyboard = VKeyboard(on_key_up=self.key_up, pos_hint = {'bottom': 1, "center_x": 0.5}, size = (800,280))
        keyboard_add = VKeyboard(on_key_up=self.key_up_add, pos_hint = {'bottom': 1, "center_x": 0.5}, size = (800,230))
        keyboard_remove = VKeyboard(on_key_up=self.key_up_remove, pos_hint = {'bottom': 1, "center_x": 0.5}, size = (800,230))
        self.label = Label(text="Input is displayed here", font_size="20sp", pos_hint = {'center_y': 0.85, "center_x": 0.5}, color=(1,1,1,0.3))
        self.ing_lbl = Label(text="", font_size="20sp", pos_hint = {'center_y': 0.75, "center_x": 0.5})
        self.add_drinkbtn = MyButton()
        self.add_drinkbtn.add_widget(Label(text="Add Cocktail"))
        self.add_drinkbtn.pos_hint={'center_y': 0.75, "center_x": 0.8}
        self.add_drinkbtn.bind(on_press=btn_active)
        self.add_drinkbtn.bind(on_release=btn_deactive)
        self.add_drinkbtn.bind(on_release=self.json_insert)


        self.remove_btn = MyButton()
        self.remove_btn.add_widget(Label(text="Remove Cocktail"))
        self.remove_btn.pos_hint={'center_y': 0.75, "center_x": 0.8}
        self.remove_btn.bind(on_press=btn_active)
        self.remove_btn.bind(on_release=btn_deactive)
        self.remove_btn.bind(on_release=self.json_remove)

        change1 = bar.ids.action
        bar.ids.action.children[0].children[3].bind(on_release=self.scrn1.screen_transition)
        bar.ids.action.children[0].children[2].bind(on_release=self.scrn2.screen_transition)
        bar.ids.action.children[0].children[2].bind(on_release=self.repopulate)
        bar.ids.action.children[0].children[1].bind(on_release=scrn3.screen_transition)
        bar.ids.action.children[0].children[0].bind(on_release=self.scrn4.screen_transition)
        self.ingredient_btn = MyButton()
        self.ingredient_btn.add_widget(Label(text="Add"))
        self.ingredient_btn.pos_hint = {'center_y': 0.81, "center_x": 0.92}
        self.ingredient_btn.bind(on_release=self.add_keyword)
        self.ingredient_btn.bind(on_press=btn_active)
        self.ingredient_btn.bind(on_release=btn_deactive)
        self.clear_btn = MyButton()
        self.clear_btn.add_widget(Label(text="Clear"))
        self.clear_btn.pos_hint = {'center_y': 0.67, "center_x": 0.92}
        self.clear_btn.bind(on_release=self.clear_ing)
        self.clear_btn.bind(on_press=btn_active)
        self.clear_btn.bind(on_release=btn_deactive)
        menu_title = Label(font_size = 48, text="[font=loop]The Prancing Pony[/font]", color=(234/255, 70/255, 159/255,1),
        pos_hint={'center_y': 0.86, "center_x": 0.5}, markup = True, underline = True)

        self.ing_input = TextInput(text="",font_size = 20, size_hint = (None, None), height = 120, width = 400, pos=(20,250))
        self.remove_input = TextInput(text="",font_size = 20, size_hint = (None, None), height = 120, width = 400, pos=(20,250))
        instruct = Label(text="ingredient,ingredient,2,4,glasstype,name of drink-- number given in cl", font_size="20sp", pos_hint = {'center_y': 0.85, "center_x": 0.4})
        instruct2 = Label(text="Name of cocktail", font_size="20sp", pos_hint = {'center_y': 0.85, "center_x": 0.12})

        layout1.add_widget(self.label)
        layout1.add_widget(self.ing_lbl)
        #layout1.add_widget(update_btn)
        layout1.add_widget(self.ingredient_btn)
        layout1.add_widget(self.clear_btn)
        layout1.add_widget(keyboard)
        layout2.add_widget(self.scroll)
        layout2.add_widget(menu_title)
        layout3.add_widget(self.ing_input)
        layout3.add_widget(keyboard_add)
        layout3.add_widget(instruct)
        layout3.add_widget(self.add_drinkbtn)
        layout4.add_widget(self.remove_input)
        layout4.add_widget(self.remove_btn)
        layout4.add_widget(keyboard_remove)
        layout4.add_widget(instruct2)


        self.scrn1.add_widget(layout1)
        self.scrn2.add_widget(layout2)
        scrn3.add_widget(layout3)
        self.scrn4.add_widget(layout4)
        root.add_widget(self.scrn1)
        root.add_widget(self.scrn2)
        root.add_widget(scrn3)
        root.add_widget(self.scrn4)
        root.add_widget(self.scrn5)



        self.scroll.data = [{'l1': str(x)+" You are spescial",'l2': str(x)+" You are NOT spescial", 'img': "mohjito.jpg", 'btntxt': str(x)} for x in range(0)]
        self.scroll.refresh_from_data()


        return bar

    def key_up(self, keyboard, keycode, *args):
        if keycode == "backspace":
            self.label.text = self.label.text[:-1]
            return
        elif keycode == "spacebar":
            self.label.text = self.label.text+" "
            return
        elif keycode == "enter" or keycode == "shift" or keycode == "tab" or keycode == "escape" or keycode == "layout" or keycode == "capslock":
            return
        elif keycode == None:
            keycode = "z"
        elif keycode == '':
            keycode = "-"
        elif isinstance(keycode,tuple):
            keycode = keycode[1]
        if self.label.text == "Input is displayed here":
            self.label.text = str(keycode)
            self.label.color = (1,1,1,1)
        else:
            self.label.text = self.label.text+str(keycode)

    def repopulate(self, *args):
        vld_drinks = valid_cocktails(self.liste)
        self.scroll.data = [None] * len(vld_drinks)
        metrics = metric(vld_drinks)
        for i in range(len(vld_drinks)):
            measure_list = []
            input = []
            input.append(vld_drinks[i])
            drink = metric(input)
            for j in drink[0]:
                if j["measure"] != "ignore":
                    measure_list.append(j["measure"])
            self.scroll.data[i] = {'l1': dictstr(self.json_data[vld_drinks[i]]["ingredients"],self.json_data[vld_drinks[i]]["glass"],metrics[i]),
            'l2': self.json_data[vld_drinks[i]]["name"], 'img': self.json_data[vld_drinks[i]]["imageUrl"], 'btntxt': str(i), 'ingredients': self.liste,
            'recepie': recepie_names(self.json_data[vld_drinks[i]]["ingredients"], self.liste), "screens": [self.scrn2, self.scrn5], "measure": measure_list, "jsondata": self.json_data[vld_drinks[i]]}


    def add_keyword(self, *args):
        str1 = ""
        if self.label.text != "Input is displayed here" and self.label.text != "":
            self.liste.append(self.label.text)
            self.teller.append(self.label.text)
            for i in self.teller:
                str1 += i
            if len(str1)>45:
                self.ing_lbl.text = self.ing_lbl.text+"\n"+" | "+self.label.text
                self.teller = []
                self.teller.append(self.label.text)
                str1 = ""
            else:
                self.ing_lbl.text = self.ing_lbl.text+" | "+self.label.text
            self.label.text = "Input is displayed here"
            self.label.color = (1,1,1,0.3)


    def clear_ing(self, *args):
        self.liste = []
        self.ing_lbl.text = ""


    def key_up_add(self, keyboard, keycode, *args):
        if keycode == "backspace":
            self.ing_input.text = self.ing_input.text[:-1]
            return
        elif keycode == "spacebar":
            self.ing_input.text = self.ing_input.text+" "
            return
        elif keycode == "enter" or keycode == "shift" or keycode == "tab" or keycode == "escape" or keycode == "layout" or keycode == "capslock":
            return
        elif keycode == None:
            keycode = "z"
        elif keycode == '':
            keycode = "-"
        elif isinstance(keycode,tuple):
            keycode = keycode[1]
        self.ing_input.text = self.ing_input.text+str(keycode)

    def key_up_remove(self, keyboard, keycode, *args):
        if keycode == "backspace":
            self.remove_input.text = self.remove_input.text[:-1]
            return
        elif keycode == "spacebar":
            self.remove_input.text = self.remove_input.text+" "
            return
        elif keycode == "enter" or keycode == "shift" or keycode == "tab" or keycode == "escape" or keycode == "layout" or keycode == "capslock":
            return
        elif keycode == None:
            keycode = "z"
        elif keycode == '':
            keycode = "-"
        elif isinstance(keycode,tuple):
            keycode = keycode[1]
        self.remove_input.text = self.remove_input.text+str(keycode)


    def json_insert(self, *args):
        try:
            info = self.ing_input.text
            template = {
                "id": 0,
                "name": "",
                "category": "",
                "alcoholType": "ALCOHOLIC",
                "glass": "",
                "instructions": "Mix it",
                "imageUrl": "stock.jpg",
                "ingredients": ""
            }
            duplicate = False
            ind = 0
            info_liste = info.split(",")
            for i in range(len(self.json_data)):
                if info_liste[-1].title() == self.json_data[i]["name"]:
                    duplicate = True
                    ind = i
                    return

            if not duplicate:
                format = info_liste[-1].split(" ")
                format = [drinks.capitalize() for drinks in format]
                formated_name = ""
                for i in format:
                    formated_name += i+" "
                formated_name = formated_name[:-1]
                template["name"] = formated_name
                template["glass"] = info_liste[-2]
                template["imageUrl"] = "stock.jpg"
                info_liste.pop(-1)
                info_liste.pop(-1)
                ing_dict = {"name": "", "measure": ""}
                list_len = int(len(info_liste)/2)
                ing_list = [None]*list_len
                for i in range(list_len):
                    ing_dict["name"] = info_liste[i].capitalize()
                    ing_dict["measure"] = str(info_liste[i+list_len])+" cl"
                    ing_list[i] = ing_dict
                    ing_dict = {"name": "", "measure": ""}
                template["ingredients"] = ing_list
            else:
                return

            with open("cocktail_data.json",encoding='utf-8') as thefile:
                data = json.load(thefile)
            data.append(template)
            with open("cocktail_data.json",'w',encoding='utf-8') as thefile:
                json.dump(data, thefile)
            f = open('cocktail_data.json',)
            self.json_data = json.load(f)

        except Exception as e:
            print(e)

    def json_remove(self, *args):
        unwanted_drink = str(self.remove_input.text)
        format = unwanted_drink.split(" ")
        format = [drinks.capitalize() for drinks in format]
        unwanted_drink = ""
        for i in format:
            unwanted_drink += i+" "
        unwanted_drink = unwanted_drink[:-1]
        with open("cocktail_data.json",encoding='utf-8') as thefile:
            data = json.load(thefile)
        for i in range(len(data)):
            if data[i-1]["name"] == unwanted_drink:
                data.pop(i-1)
        with open("cocktail_data.json",'w',encoding='utf-8') as thefile:
            json.dump(data, thefile)
        f = open('cocktail_data.json',)
        self.json_data = json.load(f)

SampleApp().run()
