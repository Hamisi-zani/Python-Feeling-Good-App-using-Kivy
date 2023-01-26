from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
import json, glob
from datetime import datetime
from pathlib import Path
import random
from kivy.core.window import Window

# designate our .kv design file
Builder.load_file('design.kv')

class LoginScreen(Screen):
        def sign_up(self):
            self.manager.current = "sign_up_screen"

        def go_home_page(self,uname, pword ):
            #read json file
            with open("users.json") as file:
                users = json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.current = "home_page_screen"
            else:
                self.ids.login_wrong.text = "Wrong username or password"



class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user (self,uname, pword ):
        with open("users.json") as file:
            users = json.load(file)
            

        users [uname] = {'username' : uname, 'password': pword,
                'created': datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}
#create a new file and ovewrite the old users dictionary with new users
        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_log_in(self):
        #change direction of screen while going back to login
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_screen"

class HomePageScreen(Screen):
    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes\*txt")
       

        available_feelings = [Path(filename).stem for filename in
         available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Oops...Try another feeling"  
            


        #self.manager.transition.direction = 'right'  
        #self.manager.current = "Login_screen"




class MainApp(App):
    def build(self):
        #Window.clearcolor = (240/255,240/255,240/255,1)
        return RootWidget()
     
if __name__ == '__main__':
    MainApp().run()