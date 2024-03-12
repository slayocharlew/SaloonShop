from datetime import datetime

from kivymd.toast import toast


class FireBase:
    def saloon_info(self, opening, closing):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Info").child(self.year()).child(
                    self.month_date())
                ref.set(
                    {
                        "opening_time": opening,
                        "closing_time": closing,
                        "available_time": self.available_time(opening, closing)
                    }
                )

    def hairstyle_info(self, name, price, time):

        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("HairStyle").child(name)
                ref.set(
                    {
                        "name": name,
                        "price": price,
                        "time": time
                    }
                )
                toast("Hairstyle Added")

    def get_hairstyle(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("HairStyle")
                ref.get()

                hairstyle = ref.get()

                return hairstyle

    def remove_hair(self, name):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("HairStyle").child(name)
                ref.delete()

    def fetch_request(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Bookings")

                bookings = ref.get()

                return bookings

    def today_work(self, phone):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Bookings").child(phone)
                bookings = ref.get()

                ref = db.reference('Saloon').child("Eva_beauty").child("Today_work").child(phone)
                ref.set(bookings)

                self.update_status(phone)

    def update_status(self, phone):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Bookings").child(phone)
                ref.update({
                    "status": "Accepted"
                })

    def work(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Today_work")

                work = ref.get()

                return work

    def available_time(self, opening, closing):
        available = []
        opening = self.time_convert(opening)
        closing = self.time_convert(closing)
        for i in range(opening, closing):
            available.append(i)

        return available

    def time_convert(self, time):
        new_time = time.split(":")
        time = new_time[0]
        if time[0] == "0":
            time = time.replace("0", "")

        return int(time)

    def year(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return y

    def month_date(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return f"{m}_{d}"
