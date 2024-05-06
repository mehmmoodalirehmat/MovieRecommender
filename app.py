import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar, Listbox, simpledialog
import pandas as pd
from tkinter import messagebox as ms
from tkinter import *
import webbrowser
import urllib.parse
from PIL import Image, ImageTk # for image processing
import sqlite3 # to store the data



class Application:
    __instance = None
    def __init__(self):
        if Application.__instance is not None:
            raise Exception("Singleton instance already exists")
        else:
            self.root = Tk() #creating the gui window
            # title of gui
            self.root.title('DiaMonitor')
            # setting the window size and position
            self.root.geometry('925x600+300+200')
            # making the window resizeable for better gui experience
            #self.root.resizable(False, False)

            # Global variables to manage the functionalities
            self.success_user_name = ''
            self.signin_frame = None
            self.login_image = None
            self.image_label = None
            self.signin_heading_label = None
            self.signin_user_entry = None
            self.signin_user_line = None
            self.signin_pwd_entry = None
            self.signin_pwd_line = None
            self.signin_button = None
            # admin username and password
            self.admin_username = "louis"
            self.admin_password = "123"
            self.admin_login = False
            self.signin_dont_have_account_label = None
            self.signin_frame_signup_button = None
            # creating the objects for the classes
            self.view_controller = ViewController()
            self.database = GlucoseManagementModel()
            self.view_controller.add_movie_data()
            self.main_window = None
            self.selectionWindow = None

            # Signin view creation
            self.signin_screen = SigninView(self.root)
            # configuring the commands of signup link at signin screen
            self.signin_screen.signin_frame_signup_button.configure(command=self.create_account_frame)
            self.signin_screen.signin_frame_signup_button.update()
            self.signin_screen.signin_button.configure(command=self.signin)
            self.signin_screen.signin_button.update()

            # signup screen creation
            self.signup_screen = SignupView(self.root)

            # Signup button configurations
            self.signup_screen.signup_button.configure(command=self.new_user)
            self.signup_screen.signup_button.update()
            self.signup_screen.signup_frame_signin_button.configure(command=self.show_signin_frame)
            self.signup_screen.signup_frame_signin_button.update()

            # main window
            movies_df = pd.read_csv('data.csv')
            self.main_window = MainWindow(self.root,movies_df)
            self.main_window.start_button.configure(command=self.open_selection_window)
            self.main_window.quit_button.configure(command=self.quit)

            # selction window
            self.selectionWindow  = SelectionWindow(self.root, movies_df, self.main_window.user_data, self.main_window.history)
            self.selectionWindow.add_history_button.configure(command=self.add_to_history)
            self.selectionWindow.show_history_button.configure(command=self.show_history)
            self.selectionWindow.find_movies_button.configure(command=self.find_movies)


            # main screen for data management
            # self.userProfile_screen = UserProfileView(self.root)
            self.userProfile_screen = None

            self.__class__.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls()
        return cls.__instance

    # this function will load the signup screen to the main window when you click on signup
    def create_account_frame(self):
        self.signin_screen.signin_frame.place_forget()
        self.admin_login = True
        self.signup_screen.signup_frame.place(x=0, y=0)


    # function to logout and take bake to sigin screen
    def logout(self):
        self.userProfile_screen.user_profile_frame.pack_forget()
        # self.userProfile_screen.user_profile_frame.place_forget()
        self.signin_screen.signin_frame.place(x=0, y=0)

    # this will show the logout option when you click on the letter displayed in upper right corner
    def show_logout_menu(self,event):
        # Create a menu to display logout option
        menu = Menu(self.userProfile_screen.user_profile_frame, tearoff=0)
        menu.add_command(label="Logout", command=self.logout)
        menu.post(event.x_root, event.y_root)

    # this functions handles all the signin events
    def signin(self):
        username = self.signin_screen.signin_user_entry.get()
        pwd = self.signin_screen.signin_pwd_entry.get()
        user_exist, pass_correct = self.signin_screen.view_controller.check_if_user_exist(username, pwd)
        if username != "Username" and pwd != "Password":
            if len(pass_correct) == 1:
                self.success_user_name = username
                self.signin_screen.signin_frame.place_forget()
                self.main_window.mainWindow_frame.place(x=0,y=0)   
                # self.main_window.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                # self.main_window.start_button.place(relx=0.5, rely=0.5, anchor='center', width=120, height=50)
                # self.main_window.quit_button.place(relx=0.5, rely=0.6, anchor='center', width=120, height=50)            
                # self.bg_image = tk.PhotoImage(file='background.png')  # Ensure the image path is correct
                # self.obj.bg_label.configure(image=self.bg_image)
                #self.root.withdraw()
                # self.userProfile_screen = UserProfileView(self.root, username)
                # self.signin_screen.success_user_name = username
                # self.clear_signin_fields()
                # # creating the avatar using the initials
                # avatar_frame = Frame(self.userProfile_screen.user_profile_frame, width=100, height=100, bg="gray")
                # avatar_frame.place(width=40, height=40, relx=0.95, rely=0.02)
                # name_initials = self.signin_screen.success_user_name[0].upper()
                # initials_label = Label(avatar_frame, text=name_initials, font=("Arial", 30), fg="white", bg="gray")
                # initials_label.place(relx=0.5, rely=0.5, anchor=CENTER)
                # initials_label.bind("<Button-1>", self.show_logout_menu)
                # self.signin_screen.signin_frame.place_forget()
                # self.userProfile_screen.user_profile_frame.pack(fill=BOTH, expand=True)
                # self.userProfile_screen.user_profile_frame.place(x=0, y=0)
            elif len(user_exist) == 1 and len(pass_correct) == 0:
                self.clear_signin_fields()
                ms.showerror('Oops!', 'Password is incorrect.')
            else:
                ms.showerror('Oops!', 'Username does not exist.')
        else:
            ms.showerror("Error", "All fields required")

    # this will clear all the entry fields after user clicks the signin button
    def clear_signin_fields(self):
        self.signin_screen.signin_user_entry.delete(0, END)
        self.signin_screen.signin_pwd_entry.delete(0, END)
        self.signin_screen.signin_user_entry.insert(0, 'Username')
        self.signin_screen.signin_pwd_entry.insert(0, 'Password')

    # this will clear all the entry fields after user clicks the signup button
    def clear_signup_fields(self):
        self.signup_screen.signup_user_entry.delete(0, END)
        self.signup_screen.signup_pwd_entry.delete(0, END)
        self.signup_screen.signup_confirm_pwd_entry.delete(0, END)
        self.signup_screen.signup_user_entry.insert(0, 'Username')
        self.signup_screen.signup_pwd_entry.insert(0, 'Password')
        self.signup_screen.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

    def log(self):
        self.signup_screen.signup_user_entry.delete(0, END)
        self.signup_screen.signup_pwd_entry.delete(0, END)
        self.signup_screen.signup_confirm_pwd_entry.delete(0, END)
        self.signup_screen.signup_user_entry.insert(0, 'end')
        self.signup_screen.signup_pwd_entry.insert(0, 'end')
        self.signup_screen.signup_confirm_pwd_entry.insert(0, 'end')
        self.signup_screen.signup_frame.place_forget()
        self.signin_screen.signin_frame.place(x=0, y=0)

    # this function will add the new user to database
    def new_user(self):
        # checking if its admin login then we add new user
        if self.admin_login==True:
            p1 = self.signup_screen.signup_pwd_entry.get()
            p2 = self.signup_screen.signup_confirm_pwd_entry.get()
            print(p1, p2)
            if self.signup_screen.signup_user_entry.get() != 'Username' and p1 != 'Password' and p2 != 'Confirm Password':
                if p1 == p2:
                    # calling the database operation to add new user
                    result = self.signup_screen.view_controller.add_user_to_database(self.signup_screen.signup_user_entry.get(), p1)
                    if result:
                        ms.showerror('Error!', 'Username Taken Try a Different One.')
                        self.clear_signup_fields()
                    else:
                        ms.showinfo('Success!', 'Account Created!')
                        self.log()
                else:
                    ms.showerror('Error!', 'Both Password Should Match')
                    self.clear_signup_fields()
            else:
                ms.showerror('Error!', 'All Fields Required')
        else:
            ms.showerror("Error", "Only Admin can add new user")


    # function to show signin frame once users logout
    def show_signin_frame(self):
        self.signup_screen.signup_frame.place_forget()
        self.signin_screen.signin_frame.place(x=0, y=0)
    
    def open_selection_window(self):
        self.main_window.mainWindow_frame.place_forget()
        self.selectionWindow.selectionWindow_frame.place(x=0,y=0)

    def quit(self):
        self.root.destroy()

    def add_to_history(self):
        movie = self.selectionWindow.movie_listbox.get(tk.ACTIVE)
        id = self.view_controller.get_movie_id(movie)
        res = self.view_controller.insert_movie_in_watch_history(self.success_user_name,id)
        messagebox.showinfo("Feedback",res)
        # if movie and movie not in self.history:
        #     self.history.append(movie)

    def show_history(self):
        movie_list = self.view_controller.get_movie_history(self.success_user_name)
        HistoryWindow(movie_list)

    def find_movies(self):
        self.selectionWindow.user_data['name'] = self.selectionWindow.name_var.get()
        self.selectionWindow.user_data['surname'] = self.selectionWindow.surname_var.get()
        self.selectionWindow.user_data['age'] = self.selectionWindow.age_var.get()
        selected_genres = [genre for genre, var in self.selectionWindow.genre_vars.items() if var.get()]
        genre_filtered_movies = self.selectionWindow.movies_df[self.selectionWindow.movies_df['Genre'].apply(lambda x: any(genre in x for genre in selected_genres))]
        movie_history = self.view_controller.get_movie_history(self.success_user_name)
        def is_suitable(movie):
            age = self.selectionWindow.user_data['age']
            certificate = movie['Certificate']
            if pd.isna(certificate):
                return False
            certificate = str(certificate)
            if 'PG-13' in certificate and age < 13:
                return False
            if 'R' in certificate and age < 17:
                return False
            if movie['Series_Title'] in movie_history:
                return False
            return True
        
        suitable_movies = genre_filtered_movies[genre_filtered_movies.apply(is_suitable, axis=1)]
        matched_movies = suitable_movies.head(10)
        MovieDisplayWindow(matched_movies)


# earlier
class MainWindow():
    def __init__(self,root,movies_df):
        #super().__init__()
        self.root = root
        self.root.title("Movie Matcher")
        #self.geometry("800x600")
        self.movies_df = movies_df
        self.user_data = {}
        self.history = []

        self.mainWindow_frame = Frame(self.root, width=925, height=600, bg='white')
        # Background image
        self.bg_image = tk.PhotoImage(file='background.png')  # Ensure the image path is correct
        self.bg_label = tk.Label(self.root, image=self.bg_image)


        #self.bg_label = tk.Label(self.mainWindow_frame)
        #self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome label with improved visibility
        welcome_label = tk.Label( self.mainWindow_frame, text="Welcome to Movie Matcher", font=('Helvetica', 24, 'bold'), bg='navy', fg='white', padx=20, pady=10)
        welcome_label.place(relx=0.5, rely=0.2, anchor='center')

        # # Styling for buttons
        # style = ttk.Style()
        # style.configure('HighContrast.TButton', font=('Helvetica', 12, 'bold'), foreground='white', background='black', borderwidth=2)

        # Start button with style changes
        self.start_button = ttk.Button( self.mainWindow_frame, text="Start", style='HighContrast.TButton')
        self.start_button.place(relx=0.5, rely=0.5, anchor='center', width=120, height=50)

        # Quit button with style changes
        self.quit_button = ttk.Button( self.mainWindow_frame, text="Quit", style='HighContrast.TButton')
        self.quit_button.place(relx=0.5, rely=0.6, anchor='center', width=120, height=50)


class SelectionWindow():
    def __init__(self, root, movies_df, user_data, history):
        #super().__init__(root)
        self.root = root
        self.root.title("Select Your Preferences")
        self.movies_df = movies_df
        self.user_data = user_data
        self.history = history
        
        self.selectionWindow_frame = Frame(self.root, width=925, height=600, bg='white')
        #self.selectionWindow_frame.place(x=0, y=0)
        
        # Labels, Entries, and Buttons placement adjustments
        ttk.Label(self.selectionWindow_frame, text="Select genres:").place(x=50, y=20)
        self.genres = ['Drama', 'Action', 'Comedy', 'Romance', 'Sci-Fi']
        self.genre_vars = {genre: tk.BooleanVar() for genre in self.genres}
        
        y_offset = 50
        for genre in self.genres:
            ttk.Checkbutton(self.selectionWindow_frame, text=genre, variable=self.genre_vars[genre]).place(x=60, y=y_offset)
            y_offset += 30
        
        ttk.Label(self.selectionWindow_frame, text="Select duration (minutes):").place(x=50, y=y_offset)
        self.duration_var = tk.IntVar()
        ttk.Scale(self.selectionWindow_frame, from_=60, to=180, orient="horizontal", variable=self.duration_var).place(x=250, y=y_offset, width=200)
        y_offset += 40
        
        ttk.Label(self.selectionWindow_frame, text="Enter your name:").place(x=50, y=y_offset)
        self.name_var = tk.StringVar()
        ttk.Entry(self.selectionWindow_frame, textvariable=self.name_var).place(x=250, y=y_offset, width=150)
        y_offset += 30
        
        ttk.Label(self.selectionWindow_frame, text="Enter your surname:").place(x=50, y=y_offset)
        self.surname_var = tk.StringVar()
        ttk.Entry(self.selectionWindow_frame, textvariable=self.surname_var).place(x=250, y=y_offset, width=150)
        y_offset += 30
        
        ttk.Label(self.selectionWindow_frame, text="Enter your age:").place(x=50, y=y_offset)
        self.age_var = tk.IntVar()
        ttk.Entry(self.selectionWindow_frame, textvariable=self.age_var).place(x=250, y=y_offset, width=50)
        y_offset += 40
        
        ttk.Label(self.selectionWindow_frame, text="Available Movies:").place(x=50, y=y_offset)
        self.movie_listbox = Listbox(self.selectionWindow_frame, height=10, width=50)
        self.movie_listbox.place(x=250, y=y_offset, height=160, width=300)
        scrollbar = Scrollbar(self.selectionWindow_frame)
        scrollbar.place(x=550, y=y_offset, height=160)
        self.movie_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.movie_listbox.yview)
        y_offset += 180
        for movie in self.movies_df['Series_Title'].values:
            self.movie_listbox.insert(tk.END, movie)
        
        self.add_history_button = ttk.Button(self.selectionWindow_frame, text="Add to History")
        self.add_history_button.place(x=50, y=y_offset, width=150)
        self.show_history_button = ttk.Button(self.selectionWindow_frame, text="Show History")
        self.show_history_button.place(x=250, y=y_offset, width=150)
        self.find_movies_button = ttk.Button(self.selectionWindow_frame, text="Find Movies")
        self.find_movies_button.place(x=450, y=y_offset, width=150)
    
    # def add_to_history(self):
    #     movie = self.movie_listbox.get(tk.ACTIVE)
    #     if movie and movie not in self.history:
    #         self.history.append(movie)

    # def show_history(self):
    #     HistoryWindow(self.history)

    # def find_movies(self):
    #     self.user_data['name'] = self.name_var.get()
    #     self.user_data['surname'] = self.surname_var.get()
    #     self.user_data['age'] = self.age_var.get()
    #     selected_genres = [genre for genre, var in self.genre_vars.items() if var.get()]
        
    #     genre_filtered_movies = self.movies_df[self.movies_df['Genre'].apply(lambda x: any(genre in x for genre in selected_genres))]
        
    #     def is_suitable(movie):
    #         age = self.user_data['age']
    #         certificate = movie['Certificate']
    #         if pd.isna(certificate):
    #             return False
    #         certificate = str(certificate)
    #         if 'PG-13' in certificate and age < 13:
    #             return False
    #         if 'R' in certificate and age < 17:
    #             return False
    #         if movie['Series_Title'] in self.history:
    #             return False
    #         return True
        
    #     suitable_movies = genre_filtered_movies[genre_filtered_movies.apply(is_suitable, axis=1)]
    #     matched_movies = suitable_movies.head(10)
    #     MovieDisplayWindow(matched_movies)

class HistoryWindow():
    def __init__(self,history):
        self.root =Toplevel()
        self.root.title("Your Movie History")
        self.root.geometry("400x300")
        ttk.Label(self.root, text="Watched Movies:").pack(pady=10)
        listbox = Listbox(self.root, height=10, width=50)
        listbox.pack(pady=10)
        for movie in history:
            listbox.insert(tk.END, movie)

class MovieDisplayWindow():
    def __init__(self,movies_df):
        self.root = Toplevel()
        self.root.title("Recommended Movies")
        self.root.geometry("800x600")

        ttk.Label(self.root, text="Matching Movies:").pack(pady=10)
        self.listbox = Listbox(self.root, height=10, width=50)
        self.listbox.pack(pady=10)
        for index, row in movies_df.iterrows():
            self.listbox.insert(tk.END, f"{row['Series_Title']} - {row['Released_Year']}")

        # Buttons for Netflix and Amazon Prime
        self.netflix_button = ttk.Button(self.root, text="Netflix", command=self.search_netflix)
        self.amazon_button = ttk.Button(self.root, text="Amazon Prime", command=self.search_amazon)
        self.netflix_button.pack(pady=5)
        self.amazon_button.pack(pady=5)

    def search_netflix(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_movie = self.listbox.get(selected_index)
            # Here you would typically call an API or open a web search
            print(f"Search on Netflix: {selected_movie}")
            # For example:
            webbrowser.open(f"https://www.netflix.com/search?q={urllib.parse.quote(selected_movie)}")
        else:
            messagebox.showerror("Selection Error", "Please select a movie from the list.")

    # def search_amazon(self):
    #     selected_index = self.listbox.curselection()
    #     if selected_index:
    #         selected_movie = self.listbox.get(selected_index)
    #         # Here you would typically call an API or open a web search
    #         print(f"Search on Amazon Prime: {selected_movie}")
    #         # For example:
    #         webbrowser.open(f"https://www.amazon.com/s?k={urllib.parse.quote(selected_movie)}")
    #     else:
    #         messagebox.showerror("Selection Error", "Please select a movie from the list.")

    def search_amazon(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_movie = self.listbox.get(selected_index)
            # Print the search operation in the console
            print(f"Search on Amazon Prime Video: {selected_movie}")
            # Direct URL to Amazon Prime Video search
            webbrowser.open(f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={urllib.parse.quote(selected_movie)}&ie=UTF8")
        else:
            messagebox.showerror("Selection Error", "Please select a movie from the list.")




# signin view class here i created the all gui related widgets
class SigninView:
    def __init__(self,root):

        self.root = root

        # Sign in Frame variables
        self.success_user_name = ''
        self.signin_frame = None
        self.login_image = None
        self.image_label = None
        self.signin_heading_label = None
        self.signin_user_entry = None
        self.signin_user_line = None
        self.signin_pwd_entry = None
        self.signin_pwd_line = None
        self.signin_button = None
        self.signin_dont_have_account_label = None
        self.signin_frame_signup_button = None
        self.view_controller = ViewController()

        # Creating the sign in frame
        self.signin_frame = Frame(self.root, width=925, height=600, bg='white')
        self.signin_frame.place(x=0, y=0)

        # reading the signin image and then display
        self.login_image = Image.open("logo_1.png")
        self.login_image = ImageTk.PhotoImage(self.login_image)
        self.image_label = Label(self.signin_frame, image=self.login_image, bg='white')
        self.image_label.place(x=80, y=140)
        self.signin_heading_label = Label(self.signin_frame, text='Sign in', fg='#57a1f8', bg='white',
                                          font=('Microsoft YaHei UI Light', 23, 'bold'))
        # heading label for signin window
        self.signin_heading_label.place(x=580, y=125)
        self.signin_user_entry = Entry(self.signin_frame, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft YaHei UI Light', 11))
        # Entry field for username binding it with on enter and on leave functions (they will remove and add
        # placeholder on mouse hover for user ease)
        self.signin_user_entry.place(x=510, y=200)
        self.signin_user_entry.insert(0, 'Username')
        self.signin_user_line = Frame(self.signin_frame, width=295, height=2, bg='black')
        self.signin_user_line.place(x=505, y=227)
        self.signin_user_entry.bind('<Enter>', self.on_enter_signin_user_entry)
        self.signin_user_entry.bind('<Leave>', self.on_leave_signin_user_entry)
        self.signin_pwd_entry = Entry(self.signin_frame, width=25, fg='black', border=0, bg='white',
                                      font=('Microsoft YaHei UI Light', 11))
        self.signin_pwd_entry.place(x=510, y=270)

        # Entry field for password binding it with on enter and on leave functions (they will remove and add
        # placeholder on mouse hover for user ease)
        self.signin_pwd_entry.insert(0, 'Password')
        # Binding password entry field
        self.signin_pwd_entry.bind('<Enter>', self.on_enter_signin_password_entry)
        self.signin_pwd_entry.bind('<Leave>', self.on_leave_signin_password_entry)
        self.signin_pwd_line = Frame(self.signin_frame, width=295, height=2, bg='black')
        self.signin_pwd_line.place(x=505, y=297)

        # Sign in button
        self.signin_button = Button(self.signin_frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white',
                                    border=0)
        self.signin_button.place(x=515, y=324)

        # "Don't have an account?" label
        self.signin_dont_have_account_label = Label(self.signin_frame, text="Dont have an account?", fg='black',
                                                    bg='white',
                                                    font=('Microsoft YaHei UI Light', 9))
        self.signin_dont_have_account_label.place(x=555, y=390)

        # Sign up button
        self.signin_frame_signup_button  = Button(self.signin_frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
        self.signin_frame_signup_button .place(x=695, y=390)

    # When the mouse enters the signin_user_entry widget, delete its current contents
    # So that user can directly type his username
    def on_enter_signin_user_entry(self, e):
        self.signin_user_entry.delete(0, 'end')

    # When the mouse cursor leaves the signin_user_entry widget and its empty then it insert the
    # placeholder "username"
    def on_leave_signin_user_entry(self, e):
        name = self.signin_user_entry.get()
        if name == '':
            self.signin_user_entry.insert(0, 'Username')

    # When the mouse cursor enters the signin_pwd_entry widget, delete its current contents
    # So that user can directly type his password
    def on_enter_signin_password_entry(self, e):
        self.signin_pwd_entry.delete(0, 'end')
        # Configure the widget to show the entered text as asterisks (for password masking)
        self.signin_pwd_entry.configure(show="*")

    # When the mouse cursor leaves the signin_password_entry widget and its empty then it insert the
    # placeholder "password"
    def on_leave_signin_password_entry(self, e):
        name = self.signin_pwd_entry.get()
        if name == '':
            self.signin_pwd_entry.configure(show="")
            self.signin_pwd_entry.insert(0, 'Password')

# signup view class creating the all widgets for signup window
class SignupView:
    def __init__(self, root):
        self.root = root

        # Signup Frame Widgets
        self.signup_frame = None
        self.signup_image = None
        self.signup_image_label = None
        self.signup_heading_label = None
        self.signup_user_entry = None
        self.signup_user_line = None
        self.signup_pwd_entry = None
        self.signup_pwd_line = None
        self.signup_confirm_pwd_entry = None
        self.signup_confirm_pwd_entry_line = None
        self.signup_button = None
        self.signup_have_account_label = None
        self.signup_frame_signin_button = None
        self.login_image = Image.open("logo_1.png")
        self.login_image = ImageTk.PhotoImage(self.login_image)
        self.view_controller = ViewController()
        self.frames = None

        # Creating the Signup frame
        self.signup_frame = Frame(self.root, width=925, height=600, bg='#fff')

        # reading and displaying the signup image
        label = Label(self.signup_frame, image=self.login_image,border=0, bg='white')
        label.place(x=50, y=100)
        # label.cancel = label.after(0, self.play, self.frames, label)

        # Signup heading label
        self.signup_heading_label = Label(self.signup_frame, text='Sign up', fg='#57a1f8', bg='white',
                                          font=('Microsoft Yahei UI Light', 23, 'bold'))
        self.signup_heading_label.place(x=580, y=75)
        # Username entry field
        self.signup_user_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft Yahei UI Light', 11))
        self.signup_user_entry.place(x=510, y=150)
        self.signup_user_entry.insert(0, 'Username')

        # Binding the signup_user_entry with on enter and on leave functions similar to signin window
        self.signup_user_entry.bind('<Enter>', self.on_enter_signup_user_entry)
        self.signup_user_entry.bind('<Leave>', self.on_leave_signup_user_entry)
        self.signup_user_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_user_line.place(x=505, y=177)

        # Password entry field
        self.signup_pwd_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                      font=('Microsoft Yahei UI Light', 11))
        self.signup_pwd_entry.place(x=510, y=220)
        self.signup_pwd_entry.insert(0, 'Password')

        # Binding the signup_pwd_entry on_enter and on_leave functionalities
        self.signup_pwd_entry.bind('<Enter>', self.on_enter_signup_password_entry)
        self.signup_pwd_entry.bind('<Leave>', self.on_leave_signup_password_entry)
        self.signup_pwd_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_pwd_line.place(x=505, y=247)

        # Confirm password entry field
        self.signup_confirm_pwd_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                              font=('Microsoft Yahei UI Light', 11))
        self.signup_confirm_pwd_entry.place(x=510, y=290)
        self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

        # Binding the signup_confirm_pwd_entry on_enter and on_leave functionalities
        self.signup_confirm_pwd_entry.bind('<Enter>', self.on_enter_signup_conf_pwd_entry)
        self.signup_confirm_pwd_entry.bind('<Leave>', self.on_leave_signup_conf_pwd_entry)

        self.signup_confirm_pwd_entry_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_confirm_pwd_entry_line.place(x=505, y=317)

        # Signup button
        self.signup_button = Button(self.signup_frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white',
                                    border=0)
        self.signup_button.place(x=515, y=350)

        # "I have an account" label
        self.signup_have_account_label = Label(self.signup_frame, text='I have an account', fg='black', bg='white',
                                               font=('Microsoft YaHei UI Light', 9))
        self.signup_have_account_label.place(x=570, y=410)

        # Signin button
        self.signup_frame_signin_button = Button(self.signup_frame, width=6, text='Sign in', border=0, bg='white',
                                                 cursor='hand2', fg='#57a1f8')
        self.signup_frame_signin_button.place(x=680, y=410)

    # This function is triggered when the mouse cursor enters the signup_user_entry field.
    # It clears the field by deleting its contents.
    def on_enter_signup_user_entry(self, e):
        self.signup_user_entry.delete(0, END)

    # This function is triggered when the mouse cursor leaves the signup_user_entry field.
    # If the field is empty, it inserts the default text 'Username' into the field.
    def on_leave_signup_user_entry(self, e):
        if self.signup_user_entry.get() == '':
            self.signup_user_entry.insert(0, 'Username')

    # This function is triggered when the mouse enters the signup_password_entry field.
    # It clears the field by deleting its contents and configures it to show '*' characters for password input.
    def on_enter_signup_password_entry(self, e):
        self.signup_pwd_entry.delete(0, 'end')
        self.signup_pwd_entry.configure(show='*')

    # This function is triggered when the mouse leaves the signup_password_entry field.
    # If the field is empty, it inserts the default text 'Password' into the field.
    def on_leave_signup_password_entry(self, e):
        if self.signup_pwd_entry.get() == '':
            # Resets the field to display plain text instead of '*'
            self.signup_pwd_entry.configure(show="")
            self.signup_pwd_entry.insert(0, 'Password')

    # This function is triggered when the mouse enters the signup_confirm_pwd_entry field.
    # It clears the field by deleting its contents and configures it to show '*' characters for password input.
    def on_enter_signup_conf_pwd_entry(self, e):
        self.signup_confirm_pwd_entry.delete(0, END)
        self.signup_confirm_pwd_entry.configure(show='*')

    # This function is triggered when the mouse leaves the signup_confirm_pwd_entry field.
    # If the field is empty, it inserts the default text 'Confirm Password' into the field.
    def on_leave_signup_conf_pwd_entry(self, e):
        if self.signup_confirm_pwd_entry.get() == '':
            # Resets the field to display plain text instead of '*'
            self.signup_confirm_pwd_entry.configure(show="")
            self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')




class GlucoseManagementModel:
    def __init__(self):
        # this will connect to the databse.db if exists otherwise creates a new database
        self.db = sqlite3.connect('database.db')
        self.cursor = self.db.cursor()
        # this will check first if there is no table then it will generate the user table
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL);')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Poster_Link TEXT,
                                Series_Title TEXT UNIQUE,
                                Released_Year TEXT,
                                Certificate TEXT,
                                Runtime TEXT,
                                Genre TEXT,
                                IMDB_Rating REAL,
                                Overview TEXT,
                                Meta_score REAL,
                                Director TEXT,
                                Star1 TEXT,
                                Star2 TEXT,
                                Star3 TEXT,
                                Star4 TEXT,
                                No_of_Votes INTEGER,
                                Gross TEXT
                            );
                        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_watch_history (
                            user_id TEXT NOT NULL,
                            movie_id INTEGER NOT NULL,
                            PRIMARY KEY (user_id,movie_id),
                            FOREIGN KEY (user_id) REFERENCES user (username),
                            FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
                            );''')
        # this will check first if there is no table then it will generate the stock data
        # self.cursor.execute(
        #     'CREATE TABLE IF NOT EXISTS glucose_data (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL,'
        #     'glucose_level REAL NOT NULL,log_date DATE NOT NULL,FOREIGN KEY (username) REFERENCES user(username));')
        # # saving the changes to database
        self.db.commit()
        self.success_user_name = ''


class DatabaseOperations:
    # this will check is user exists or not
    def authenticate_user(self, username, password):
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            query1 = 'SELECT * FROM user WHERE username = ? and password = ?'
            c.execute(query1, [(username), (password)])
            pass_correct = c.fetchall()
            query2 = 'SELECT * FROM user WHERE username = ?'
            c.execute(query2, [(username)])
            user_exist = c.fetchall()
            return user_exist,pass_correct

    # this function will add the new user credentials to the database
    def add_new_user(self,username,pwd):
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            find_user = ('SELECT username FROM user WHERE username = ?')
            c.execute(find_user, [(username)])
            rows = c.fetchall()
            print(rows)
            if not rows:
                print("Inserted")
                insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                c.execute(insert, [(username), (pwd)])
                db.commit()
            else:
                print(rows)
                return rows
            
    def insert_watch_history(self,user_id, movie_id):
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Check if the movie_id already exists for this user
        cursor.execute("SELECT * FROM user_watch_history WHERE user_id = ? AND movie_id = ?", (user_id, movie_id))
        if cursor.fetchone():
            conn.close()
            return "Movie already added in watch history."
        
        # Insert the record into user_watch_history table
        cursor.execute("INSERT INTO user_watch_history (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        
        return "Movie added to watch history successfully."

    def get_movie_id(self,movie_name):
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Execute SQL query to find the movie id by name
        cursor.execute("SELECT movie_id FROM movies WHERE Series_Title = ?", (movie_name,))
        result = cursor.fetchone()
        
        # Close the connection
        conn.close()
        
        # Return the result
        return result[0] if result else None
    
    def get_watched_movie_names(self,user_id):
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Execute SQL query to join the movies and user_watch_history tables
        # and retrieve the Series_Title for the given user_id
        cursor.execute('''
            SELECT m.Series_Title
            FROM movies m
            JOIN user_watch_history uwh ON m.movie_id = uwh.movie_id
            WHERE uwh.user_id = ?
        ''', (user_id,))
        
        # Fetch all results
        movies = cursor.fetchall()
        
        # Close the connection
        conn.close()
        
        # Extract movie titles from the query result
        movie_titles = [movie[0] for movie in movies] if movies else []
        
        return movie_titles

# Example usage:
# movie_id = get_movie_id('/path/to/your/database.db', 'The Shawshank Redemption')
# print(movie_id)


    # def load_data_into_database(self):
    #     # Connect to the SQLite database
    #     conn = sqlite3.connect('database.db')
    #     cursor = conn.cursor()
        
    #     # Check if there are any records in the movies table
    #     cursor.execute("SELECT COUNT(*) FROM movies")
    #     if cursor.fetchone()[0] > 0:
    #         print("Data already exists in the database. No new data will be added.")
    #         conn.close()
    #         return
        
    #     # Load data from CSV
    #     data = pd.read_csv('imdb_top_1000.csv')
        
    #     # Since there are no records, insert new data
    #     data.to_sql('movies', conn, if_exists='replace', index=False)
        
    #     # Commit changes and close the connection
    #     conn.commit()
    #     conn.close()

    def load_data_into_database(self):
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Check if there are any records in the movies table
        cursor.execute("SELECT COUNT(*) FROM movies")
        if cursor.fetchone()[0] > 0:
            print("Data already exists in the database. No new data will be added.")
            conn.close()
            return
        
        # Load data from CSV
        data = pd.read_csv('data.csv')
        
        # Remove any column that should not be inserted. Ensure no 'movie_id' column in DataFrame
        data = data[['Poster_Link', 'Series_Title', 'Released_Year', 'Certificate', 'Runtime', 
                    'Genre', 'IMDB_Rating', 'Overview', 'Meta_score', 'Director', 
                    'Star1', 'Star2', 'Star3', 'Star4', 'No_of_Votes', 'Gross']]
        
        # Since there are no records, append new data into the existing table structure
        data.to_sql('movies', conn, if_exists='append', index=False)
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()

# controller class for database operations
class ViewController:
    def __init__(self):
        self.database_operations = DatabaseOperations()

    def check_if_user_exist(self,username,pwd):
        r1,r2 = self.database_operations.authenticate_user(username,pwd)
        return r1,r2
    def add_user_to_database(self,username,pwd):
        result = self.database_operations.add_new_user(username,pwd)
        return result
    def add_movie_data(self):
        self.database_operations.load_data_into_database()
    def get_movie_id(self,title):
        id = self.database_operations.get_movie_id(title)
        return id
    def insert_movie_in_watch_history(self,user_name,movie_id):
        res = self.database_operations.insert_watch_history(user_name,movie_id)
        return res
    def get_movie_history(self,user_name):
        movie_list = self.database_operations.get_watched_movie_names(user_name)
        return movie_list

# Entry point
if __name__ == "__main__":
    # movies_df = pd.read_csv('data.csv')
    # app = MainWindow(movies_df)
    app = Application.get_instance()
    app.root.mainloop()
    #app.mainloop()
