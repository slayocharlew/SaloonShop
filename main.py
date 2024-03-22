import re

from kivy.base import EventLoop

import network
from beem import sms as SM
from kivy.clock import mainthread
from kivy.properties import NumericProperty, StringProperty, Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivy import utils

from database import FireBase as FB

if utils.platform != 'android':
    Window.size = (412, 732)

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250


class Emergency(MDBoxLayout):
    pass


class TNumberField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text + substring) > 1:
            return

        if len(self.text + substring) == 1 and substring == "0":
            return

        if not substring.isdigit():
            return

        return super(TNumberField, self).insert_text(substring, from_undo=from_undo)


class PNumberField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text + substring) == 0 and substring != "0":
            return

        if not substring.isdigit():
            return

        return super(PNumberField, self).insert_text(substring, from_undo=from_undo)


class Tab(MDBoxLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    size_x, size_y = Window.size

    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    start_time = StringProperty("Opening Time")
    closing_time = StringProperty("Closing Time")

    def on_start(self):
        self.keyboard_hooker()
        self.caller()
        self.notifi()
        self.orders()

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    def caller(self):
        self.schedule_display()
        self.add()
        self.display_hair_style()

    def save_start_time(self, instance, value):
        self.start_time = str(value)
        self.time()

    def save_close_time(self, instance, value):
        self.closing_time = str(value)
        self.time()

    def show_time_starting(self):
        time_dialog = MDTimePicker()
        time_dialog.open()
        time_dialog.bind(on_save=self.save_start_time)

    def show_time_closing(self):
        time_dialog = MDTimePicker()
        time_dialog.open()
        time_dialog.bind(on_save=self.save_close_time)

    def hairstyle(self, name, price, time):
        FB.hairstyle_info(FB(), name, price, time)

    def time(self):
        if self.closing_time != "Closing Time" and self.start_time != "Opening Time":
            FB.saloon_info(FB(), self.start_time, self.closing_time)

    def add_hair_style(self, data):
        self.root.ids.hair.data = {}
        if not data:
            self.root.ids.hair.data.append(
                {
                    "viewclass": "BusInfo",
                    "name": "No Cars Yet!",
                    "route": "",
                    "lcn": "",
                    "price": "",
                    "seats": ""
                }
            )
        else:
            for i, y in data.items():
                self.root.ids.hair.data.append(
                    {
                        "viewclass": "Emergency",
                        "name": i,
                        "icon": "face-woman-shimmer",
                        "phone": y["time"],
                        "fsize": "16",
                        "isize": "30sp",
                        "call": "delete",
                    }
                )

    def send_message(self, phone, name, time, hair):
        if network.ping_net():
            SM.send_sms(phone, name, time, hair)

        else:
            toast("No internet connection")

    def display_hair_style(self):
        self.root.ids.hair.data = {}
        data = FB.get_hairstyle(FB())
        if not data:
            self.root.ids.hair.data.append(
                {
                    "viewclass": "BusInfo",
                    "name": "No Cars Yet!",
                    "route": "",
                    "lcn": "",
                    "price": "",
                    "seats": ""
                }
            )
        else:
            for i, y in data.items():
                self.root.ids.hair.data.append(
                    {
                        "viewclass": "Emergency",
                        "name": i,
                        "icon": "face-woman-shimmer",
                        "phone": y["time"],
                        "fsize": "16",
                        "isize": "30sp",
                        "call": "delete",
                    }
                )

    @mainthread
    def delete_hair(self, name):
        FB.remove_hair(FB(), name)

    def stream_handler(self, message):
        if True:
            print("hello")

            self.add_hair_style(FB.get_hairstyle(FB()))

    def notifi(self):
        try:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            self.my_order = db.reference('Saloon').child("Eva_beauty").child("HairStyle").listen(
                self.stream_handler)

        except:
            print("you did good!")

    def today_schedule(self, phone):
        FB.today_work(FB(), phone)

    def add_sch(self, data):
        self.root.ids.order.data = {}
        for i, y in data.items():
            self.root.ids.order.data.append(
                {
                    "viewclass": "Saloon",
                    "icon": "google-maps",
                    "name": y["name"],
                    "phone": y["phone"],
                    "price": y["price"],
                    "time_in": y["time_in"],
                    "time_out": y["time_out"],
                    "hair_style": y["hair_style"],
                    "status": y["status"]
                }
            )

    def add(self, ):
        self.root.ids.order.data = {}
        data = FB.fetch_request(FB())
        for i, y in data.items():
            self.root.ids.order.data.append(
                {
                    "viewclass": "Saloon",
                    "icon": "google-maps",
                    "name": y["name"],
                    "phone": y["phone"],
                    "price": y["price"],
                    "time_in": y["time_in"],
                    "time_out": y["time_out"],
                    "hair_style": y["hair_style"],
                    "status": y["status"]
                }
            )

    def stream_order(self, message):
        if True:
            print("Booked!")
            try:
                self.add_sch(FB.fetch_request(FB()))
                self.works()
            except:
                pass

    def orders(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
        initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
        self.my_stream = db.reference('Saloon').child("Eva_beauty").child("Bookings").listen(
            self.stream_order)

    def add_work(self, data):
        self.root.ids.work.data = {}
        for i, y in data.items():
            self.root.ids.work.data.append(
                {
                    "viewclass": "Saloon_work",
                    "icon": "google-maps",
                    "name": y["name"],
                    "phone": y["phone"],
                    "price": y["price"],
                    "time_in": y["time_in"],
                    "time_out": y["time_out"],
                    "hair_style": y["hair_style"],
                    "status": y["status"]
                }
            )

    def schedule_display(self):
        self.root.ids.work.data = {}
        data = FB.work(FB())
        for i, y in data.items():
            self.root.ids.work.data.append(
                {
                    "viewclass": "Saloon_work",
                    "icon": "google-maps",
                    "name": y["name"],
                    "phone": y["phone"],
                    "price": y["price"],
                    "time_in": y["time_in"],
                    "time_out": y["time_out"],
                    "hair_style": y["hair_style"],
                    "status": y["status"]
                }
            )

    def stream_work(self, message):
        if True:
            print("working!")
            try:
                self.add_work(FB.work(FB()))
            except:
                pass

    def works(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
        initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
        self.my_stream = db.reference('Saloon').child("Eva_beauty").child("Today_work").listen(
            self.stream_work)

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)

    def build(self):
        pass


MainApp().run()
