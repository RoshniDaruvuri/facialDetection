import subprocess
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import os.path
import datetime
from test import test

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                         self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = os.path.join(os.path.dirname(__file__), 'log.txt')

    def login(self):
        print("Checking for face spoofing...")
        label = test(
                image=self.most_recent_capture_arr,
                model_dir='./Silent_Face_Anti_Spoofing/resources/anti_spoof_models',
                device_id=0
                )
        
        if label == 1:  # Real face
            unknown_img_path = './.tmp.jpg'

            cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

            try:
                output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
                # Split by newlines and take the first result
                lines = output.split('\\n')
                if lines:
                    # Take the first valid recognition result
                    for line in lines:
                        if line and ',' in line:
                            name = line.split(',')[1].strip()
                            if name and name not in ["unknown_person", "no_persons_found"]:
                                break
                    else:
                        name = "unknown_person"
                else:
                    name = "no_persons_found"

                print(f"Recognition output: {output}")
                print(f"Parsed name: {name}")

                if name in ["unknown_person", "no_persons_found"]:
                    util.msg_box('Oops...', 'Unknown user. Please register new user or try again.')
                else:
                    util.msg_box('Welcome back!', 'Welcome, {}.'.format(name))
                    with open(self.log_path, 'a') as f:
                        f.write('{},{},login\n'.format(name, datetime.datetime.now()))
            except Exception as e:
                print(f"Error during face recognition: {str(e)}")
                util.msg_box('Error', 'An error occurred during face recognition. Please try again.')
            finally:
                if os.path.exists(unknown_img_path):
                    os.remove(unknown_img_path)

        elif label == 0:  # No face or error
            util.msg_box('Detection Error', 'Could not properly detect a face. Please try again with better lighting and positioning.')
        else:  # Fake face
            util.msg_box('Spoofing Detected', 'Warning: Potential spoofing attempt detected!')

    def logout(self):
        print("Checking for face spoofing...")
        label = test(
                image=self.most_recent_capture_arr,
                model_dir='./Silent_Face_Anti_Spoofing/resources/anti_spoof_models',
                device_id=0
                )
                
        if label == 1:  # Real face
            unknown_img_path = './.tmp.jpg'

            cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

            try:
                output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
                # Split by newlines and take the first result
                lines = output.split('\\n')
                if lines:
                    # Take the first valid recognition result
                    for line in lines:
                        if line and ',' in line:
                            name = line.split(',')[1].strip()
                            if name and name not in ["unknown_person", "no_persons_found"]:
                                break
                    else:
                        name = "unknown_person"
                else:
                    name = "no_persons_found"

                print(f"Recognition output: {output}")
                print(f"Parsed name: {name}")

                # Check user's login status
                user_logged_in = False
                last_login_time = None
                try:
                    with open(self.log_path, 'r') as f:
                        log_entries = f.readlines()
                        # Check all entries for this user
                        user_entries = [entry for entry in log_entries if name in entry]
                        if user_entries:
                            # Get the last entry for this user
                            last_entry = user_entries[-1]
                            last_action = 'login' if 'login' in last_entry else 'logout'
                            user_logged_in = last_action == 'login'
                            if user_logged_in:
                                last_login_time = datetime.datetime.strptime(
                                    last_entry.split(',')[1],
                                    '%Y-%m-%d %H:%M:%S.%f'
                                )
                except FileNotFoundError:
                    user_logged_in = False

                if name in ["unknown_person", "no_persons_found"]:
                    util.msg_box('Oops...', 'Unknown user. Please register new user or try again.')
                elif not user_logged_in and last_action == 'logout':
                    util.msg_box('Already Logged Out', 'User {} is already logged out. Please log in first.'.format(name))
                elif not user_logged_in:
                    util.msg_box('Login Required', 'User {} was never logged in. Please log in first.'.format(name))
                else:
                    current_time = datetime.datetime.now()
                    time_diff = current_time - last_login_time
                    total_hours = time_diff.total_seconds() / 3600
                    days = int(total_hours // 24)
                    hours = total_hours % 24
                    
                    # Create time message
                    time_msg = ""
                    if days > 0:
                        time_msg += f"{days} days and "
                    time_msg += f"{hours:.1f} hours"
                    
                    util.msg_box('Goodbye!', 'See you later, {}.\nYou were logged in for: {}'.format(name, time_msg))
                    with open(self.log_path, 'a') as f:
                        f.write('{},{},logout\n'.format(name, datetime.datetime.now()))

            except Exception as e:
                print(f"Error during face recognition: {str(e)}")
                util.msg_box('Error', 'An error occurred during face recognition. Please try again.')
            finally:
                if os.path.exists(unknown_img_path):
                    os.remove(unknown_img_path)

        elif label == 0:  # No face or error
            util.msg_box('Detection Error', 'Could not properly detect a face. Please try again with better lighting and positioning.')
        else:  # Fake face
            util.msg_box('Spoofing Detected', 'Warning: Potential spoofing attempt detected!')

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, "{}.jpg".format(name)), self.register_new_user_capture)
        util.msg_box('Success!', 'User was registered successfully !')
        self.register_new_user_window.destroy()

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()
