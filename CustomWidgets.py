import json
import os
import numpy as np
import customtkinter as cstk
import random
from Parameters import *
from PIL import Image
from tkinter import Label, Menu, messagebox
from ColorPicker import ColorPicker
import pandas as pd
import FileManager as FM
import datetime
import matplotlib.pyplot as plt

def set_center(master_width, master_height, child_width, child_height):
    CENTER_WIDTH = int(np.floor(np.divide(master_width, 2)) - np.floor(np.divide(child_width, 2)))
    CENTER_HEIGHT = int(np.floor(np.divide(master_height, 2)) - np.floor(np.divide(child_height, 2)))
    return (CENTER_WIDTH, CENTER_HEIGHT)

class HomeCard(cstk.CTkFrame):
    def __init__(self, *args, root, name, color, count, superroot,
                 width: int = 350,
                 height: int = 150,
                 command = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, corner_radius=20, fg_color=color, **kwargs)
        self.__root = root
        self.__super_root = superroot
        self.pack_propagate(cstk.FALSE)
        self.grid_propagate(cstk.FALSE)
        self.__color = color
        ##################### FLASHCARD NAME #########################
        self.card_name = cstk.CTkLabel(self, width=185, font=JosefinSans_25_BOLD, text_color=WHITE, text='')
        self.card_name_bonus = cstk.CTkLabel(self, width=185, font=JosefinSans_25_BOLD, text_color=WHITE, text='')
        self.card_name_extra = cstk.CTkLabel(self, width=185, font=JosefinSans_20_BOLD, text_color=WHITE, text='')
        if len(name) <= 18:
            self.card_name.configure(text=self.__utility_text_completeness(name=self.__utility_text_parser(self, name)))
            self.card_name.place(x=20, y=15)
        elif len(name) <= 35:
            splitted = self.text_splitter(name)
            self.card_name.configure(text=self.__utility_text_completeness(name=self.__utility_text_parser(self, splitted[0])))
            self.card_name.place(x=20, y=15)
            self.card_name_bonus.configure(text=self.__utility_text_completeness(name=self.__utility_text_parser(self, splitted[1])))
            self.card_name_bonus.place(x=20, y=47)
        elif len(name) <= 60:
            splitted = self.text_splitter(name, 2)
            self.card_name.configure(font=JosefinSans_20_BOLD)
            self.card_name.configure(text=self.__utility_text_completeness(
                                               name=self.__utility_text_parser(self, splitted[0])))
            self.card_name.place(x=20, y=15)
            self.card_name_bonus.configure(font=JosefinSans_20_BOLD)
            self.card_name_bonus.configure(text=self.__utility_text_completeness(
                                                     name=self.__utility_text_parser(self, splitted[1])))
            self.card_name_bonus.place(x=20, y=40)
            self.card_name_extra.configure(text=self.__utility_text_completeness(
                                                     name=self.__utility_text_parser(self, splitted[2].strip(' '))))
            self.card_name_extra.place(x=20, y=65)

        ####################### CARD COUNTER #########################
        self.card_counter = cstk.CTkLabel(self, width=100, font=JosefinSans_20_BOLD, text_color=WHITE,
                                          text=str(count) + " CARDS")
        self.card_counter.place(x=230, y=105)
        ####################### CARDS #########################
        self.__cards = None
        self.__cards_opened = False
        self.__card_flipper = None
        self.__words_learned = 0
        self.__day_words = {
            "DAY": str(datetime.date.today()),
            "WORDS": 0
        }
        ####################### MENU BOX ##########################
        self.right_click_menu = Menu(self, tearoff=False, bg=WHITE, borderwidth=0)
        self.right_click_menu.add_command(label="PROGRESS", font=JosefinSans_20_BOLD, command=self.progress)
        self.right_click_menu.add_command(label="MODIFY", font=JosefinSans_20_BOLD, command=self.modify)
        self.right_click_menu.add_command(label="DELETE", font=JosefinSans_20_BOLD, command=self.delete)
        self.bind("<Button-3>", lambda e: self.right_click_menu.tk_popup(e.x_root, e.y_root))
        self.bind("<Double-1>", command=self.openCards)

    @staticmethod
    def __utility_text_completeness(name: str):
        if len(name) <= 15:
            while len(name) <= 20:
                name += ' '
        elif len(name) >= 15:
            while len(name) <= 17:
                name += ' '
        return name

    def progress(self):
        try:
            with open('serialfiles/' + FM.name_to_filename(self.getCardName()) + '.json', 'r') as file:
                data = json.load(file)
            days_and_words = [iterator for iterator in data["day_and_words"]]
            x = ["DAY " + str(i) for i in range(1, len(days_and_words) + 1)]
            y = []
            for iterator in days_and_words:
                y.append(iterator["WORDS"])
        except FileNotFoundError:
            x = ["DAY " + str(i) for i in range(1, 11)]
            y = [0 for i in range(1, 11)]

        plt.figure(self.getCardName())
        plt.title(self.getCardName() + ' PROGRESS', color=self.__color, fontsize=15)
        plt.xlabel("DAYS", fontsize=12)
        plt.ylabel("WORDS LEARNED", fontsize=12)
        plt.plot(x, y, color=self.__color, linewidth=2, marker='o', markersize=10)

        plt.show()

    def getCardName(self):
        name = self.card_name.cget('text').rstrip(' ') + ' ' + self.card_name_bonus.cget('text').rstrip(' ') + ' '
        name += self.card_name_extra.cget('text').rstrip(' ')
        return name.rstrip(' ')

    def BackHome(self, e):
        self.getSuperRoot().clean_then_reload()
        with open('serialfiles/' + FM.name_to_filename(self.getCardName()) + '.json', 'r') as file:
            collection = json.load(file)
        flag = False
        for iterator in collection["day_and_words"]:
            if iterator["DAY"] == str(datetime.date.today()):
                iterator["WORDS"] += self.__words_learned
                flag = True
                break

        if flag is False:
            self.__day_words['WORDS'] = self.__words_learned
            collection["day_and_words"].append(self.__day_words)

        with open('serialfiles/' + FM.name_to_filename(self.getCardName()) + '.json', 'w') as file:
            json.dump(collection, file, indent=2)

        if self.__cards_opened is True:
            self.getSuperRoot().logo_click().unbind("<Button-1>")
            self.getSuperRoot().settings_click().configure(state=cstk.ACTIVE)
            self.getSuperRoot().add_card_click().configure(state=cstk.ACTIVE)
            self.__cards.destroy()

    def next(self):
        self.__words_learned += 1
        self.__cards.after_cancel(self.__card_flipper)
        self.__cards.current = random.choice(self.__cards.all_cards)
        self.__cards.set_Question_or_Answer(self.__cards.current["Question"])
        self.__card_flipper = self.__cards.after(5000, func=self.flip)

    def flip(self):
        self.__cards.set_Question_or_Answer(self.__cards.current["Answer"])

    def remember(self):
        self.next()

    def openCards(self, e):
        self.__cards_opened = True
        self.getSuperRoot().clean()
        self.getSuperRoot().logo_click().bind("<Button-1>", command=self.BackHome)
        self.getSuperRoot().settings_click().configure(state=cstk.DISABLED)
        self.getSuperRoot().add_card_click().configure(state=cstk.DISABLED)
        self.__cards = CardPage(master=self.getSuperRoot(), color=self._fg_color)
        center = set_center(master_width=1150, master_height=800, child_width=876, child_height=505)
        self.__cards.all_cards = FM.read_from_csv(self.getCardName())
        self.__cards.set_collection_name(self.getCardName())
        self.__cards.setCorrectFunction(func=self.remember)
        self.__cards.setWrongFunction(func=self.next)
        self.__card_flipper = self.__cards.after(5000, func=self.next)

        self.__cards.place(x=center[0], y=center[1] + 10)

        if self.getSuperRoot().Darkmode is True:
            self.__cards.dark_mode()
        else:
            self.__cards.default_mode()

    @staticmethod
    def text_splitter(text: str, words_in_line: int = 2):
        if len(text) >= 19:
            splitted_text = list(text.split(' '))
            first_line = ''
            second_line = ''
            third_line = ''
            size = 0
            for word in splitted_text:
                if size < words_in_line:
                    if size < words_in_line:
                        first_line += word
                        first_line += ' '
                    size += 1
                elif size < 2*words_in_line:
                    if size < 2*words_in_line:
                        second_line += word
                        second_line += ' '
                    size += 1
                elif size < 3*words_in_line:
                    if size < 3*words_in_line:
                        third_line += word
                        third_line += ' '
                    size += 1
            return first_line, second_line, third_line
        else:
            return text

    @staticmethod
    def to_remove(letter: str):
        if 33 <= ord(letter) <= 37:
            return True
        elif ord(letter) == 39 or ord(letter) == 42:
            return True
        elif ord(letter) == 46 or ord(letter) == 47:
            return True
        elif 58 <= ord(letter) <= 64:
            return True
        elif 91 <= ord(letter) <= 96:
            return True
        elif 123 <= ord(letter) <= 126:
            return True

    @staticmethod
    def __utility_text_parser(self, name: str):
        to_parse = list(name.upper().replace('AND', '&'))
        to_parse[:] = [c for c in to_parse if not self.to_remove(c)]
        parsed = "".join(to_parse)
        return parsed

    def delete(self):
        center = set_center(master_width=1150, master_height=800, child_width=406, child_height=146)
        remove_permission = Permission(master=self.__root, root=self, target=self.card_name.cget('text').rstrip(' '))
        remove_permission.request(option='delete')
        remove_permission.place(x=center[0], y=200)

    def modify(self):
        center = set_center(master_width=1150, master_height=800, child_width=720, child_height=676)
        mod = Modify(self.getSuperRoot(), root=self.getSuperRoot(), card_name=self.getCardName(),
                     color=self.__color)
        if self.getSuperRoot().Darkmode is True:
            mod.dark_mode()
        mod.read_data()
        mod.Initialize(self.getCardName())
        mod.place(x=center[0], y=center[1])

    def getSuperRoot(self):
        return self.__super_root

global x_coord
x_coord = 0
global y_coord
y_coord = 0


class AddButton(cstk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color=WHITE, border_width=0, bg_color=WHITE)
        plus_image = cstk.CTkImage(light_image=Image.open('assets/ADD_CARD_BUTTON.png'), size=(32, 32))
        self.configure(image=plus_image)
        # self.configure(text='')
        self.configure(hover=cstk.FALSE)


class QuestionAnswer(cstk.CTkFrame):
    def __init__(self, root, *args, card_name,
                 command = None,
                 **kwargs):
        super().__init__(*args, width=680, height=310, corner_radius=20, fg_color=LIGHT_GRAY, **kwargs
                         , bg_color=WHITE)
        self.pack_propagate(cstk.FALSE)
        self.grid_propagate(cstk.FALSE)
        self.__root = root
        ###################### FLASHCARD CSV FILES SETUP ###################
        self.__folder = 'data'
        self.__name = card_name
        self.__path = self.__folder + '/' + self.__name_to_filename(card_name) + '.csv'
        self.__data = []
        ###################### QUESTION LABEL ###########################
        self.__Question_label = Label(self, text="QUESTION:", fg=BLACK, bg=LIGHT_GRAY, font=JosefinSans_20_BOLD)
        self.__Question_label.place(x=40, y=45)
        ###################### ANSWER LABEL ############################
        self.__Answer_label = Label(self, text="ANSWER:", fg=BLACK, bg=LIGHT_GRAY, font=JosefinSans_20_BOLD)
        self.__Answer_label.place(x=530, y=45)
        ###################### QUESTION ENTRY #########################
        self.__Question_Input_Field = cstk.CTkTextbox(self, height=10, width=300, text_color=WHITE, corner_radius=20
                                                    , font=JosefinSans_20_BOLD, fg_color=GRAY_B1)
        self.__Question_Input_Field.place(x=25, y=65)
        ###################### ANSWER ENTRY #########################
        self.__Answer_Input_Field = cstk.CTkTextbox(self, height=10, width=300, text_color=WHITE, corner_radius=20
                                                    , font=JosefinSans_20_BOLD, fg_color=GRAY_B1)
        self.__Answer_Input_Field.place(x=350, y=65)
        ###################### ADD CARD BUTTON ######################
        self.__add_card_button = cstk.CTkButton(self, text='ADD CARD', fg_color=GRAY_B1, hover_color=BLACK,
                                                corner_radius=20, font=JosefinSans_20_BOLD, height=40, width=155,
                                                text_color=WHITE, command=self.dimensionize_card)
        self.__add_card_button.place(x=260, y=180)
        ########################## CONFIRM BUTTON #########################
        self.__confirm_button = cstk.CTkButton(self, width=155, height=40, corner_radius=20, text_color=WHITE,
                                            text="CONFIRM", hover_color=BLACK, fg_color=GRAY_B1, font=JosefinSans_20_BOLD
                                            ,bg_color=LIGHT_GRAY, command=self.__confirm)
        self.__confirm_button.place(x=160, y=250)
        ########################## CANCEL BUTTON #########################
        self.__cancel_button = cstk.CTkButton(self, width=155, height=40, corner_radius=20, text_color=WHITE,
                                            text="CANCEL", hover_color=BLACK, fg_color=GRAY_B1, font=JosefinSans_20_BOLD
                                           , bg_color=LIGHT_GRAY, command=self.destroy)
        self.__cancel_button.place(x=365, y=250)
        self.place(x=234, y=243)

    def getQuestion(self):
        question = str(self.__Question_Input_Field.get(index1='1.0', index2='1.end'))
        return question

    def getAnswer(self):
        answer = str(self.__Answer_Input_Field.get(index1='1.0', index2='1.end'))
        return answer

    def dimensionize_card(self):
        value_tuple = (str(self.getQuestion()), str(self.getAnswer()))
        self.__data.append(value_tuple)
        self.__Question_Input_Field.delete(index1='1.0', index2='1.end')
        self.__Answer_Input_Field.delete(index1='1.0', index2='1.end')

    def __confirm(self):
        if len(self.__data) > 0:
            if len(str(self.getQuestion())) == 0 and len(str(self.getAnswer())) == 0:
                pd.DataFrame(self.__data).to_csv(self.__path, header=False, index=False, mode='a')
                count = len(pd.read_csv(self.__path).index)
                FM.Card_Count_Changer(number_of_cards=count, collection_name=self.__name)
                self.__root.reload()
                self.destroy()
            else:
                qa_tuple = (str(self.getQuestion()), str(self.getAnswer()))
                self.__data.append(qa_tuple)
                pd.DataFrame(self.__data).to_csv(self.__path, header=False, index=False, mode='a')
                self.__Question_Input_Field.delete(index1='1.0', index2='1.end')
                self.__Answer_Input_Field.delete(index1='1.0', index2='1.end')
                count = len(pd.read_csv(self.__path).index)
                FM.Card_Count_Changer(number_of_cards=count, collection_name=self.__name)
                self.__root.reload()
                self.destroy()
        else:
            if len(str(self.getQuestion())) == 0 and len(str(self.getAnswer())) == 0:
                count = len(pd.read_csv(self.__path).index)
                FM.Card_Count_Changer(number_of_cards=count, collection_name=self.__name)
                self.__root.reload()
                self.destroy()
            else:
                qa_tuple = (str(self.getQuestion()), str(self.getAnswer()))
                self.__data.append(qa_tuple)
                pd.DataFrame(self.__data).to_csv(self.__path, header=False, index=False, mode='a')
                self.__Question_Input_Field.delete(index1='1.0', index2='1.end')
                self.__Answer_Input_Field.delete(index1='1.0', index2='1.end')
                count = len(pd.read_csv(self.__path).index)
                FM.Card_Count_Changer(number_of_cards=count, collection_name=self.__name)
                self.__root.reload()
                self.destroy()

    @staticmethod
    def __name_to_filename(name: str):
        filename = name.lower()
        for i in range(0, len(filename)):
            if 32 <= ord(filename[i]) <= 39 or 42 <= ord(filename[i]) <= 47 or 58 <= ord(filename[i]) <= 64:
                filename = filename.replace(filename[i], '_')
            elif 91 <= ord(filename[i]) <= 94 or 58 <= ord(filename[i]) <= 64 or ord(filename[i]) == 96:
                filename = filename.replace(filename[i], '_')
            elif 123 <= ord(filename[i]) <= 127:
                filename = filename.replace(filename[i], '_')
        return filename

    def changeFolder(self, folder: str):
        self.__folder = folder

    def setPath(self, path: str):
        if os.path.exists(path) is True:
            self.__path = path
        else:
            messagebox.showerror("ERROR", "THE PATH YOU'VE SPECIFIED DOESN'T EXIST")

class Settings(cstk.CTkFrame):
    def __init__(self, root, *args, color=LIGHT_GRAY, dark: bool = False,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=600, height=450, corner_radius=20, fg_color=color, **kwargs
                         , bg_color=WHITE)
        self.__DarkMode = dark
        ##################################### EXIT BUTTON ####################################
        self.__XButton = cstk.CTkImage(light_image=Image.open('assets/ExitButton.png'), size=(19, 19))
        self.__ExitButton = cstk.CTkButton(self, image=self.__XButton, height=19, width=19, text='', fg_color=LIGHT_GRAY,
                                    hover=cstk.FALSE, command=self.ExitSettings)
        self.__ExitButton.place(x=555, y=15)
        self.__root_frame = root
        ##################################### THEMES #########################################
        self.__theme_options_label = Label(self, text="DARK MODE", fg=BLACK, bg=LIGHT_GRAY, font=JosefinSans_25_BOLD)
        self.__theme_options_label.place(x=50, y=65)

        self.__dark_mode_toggle_image = cstk.CTkImage(light_image=Image.open('assets/ToggleButtonLarge.png'),
                                                  size=(63, 29))
        self.__dark_mode_toggled_image = None

        self.__logo_image = cstk.CTkImage(light_image=Image.open('assets/LOGO.png'), size=(188, 117))
        self.__logo = cstk.CTkLabel(self, image=self.__logo_image, bg_color=LIGHT_GRAY, fg_color=LIGHT_GRAY, text='')
        center = set_center(master_width=600, master_height=450, child_width=188, child_height=117)
        self.__logo.place(x=center[0], y=center[1]-25)

        self.__dev_label = Label(self, text="DEVELOPED BY", fg=BLACK, bg=LIGHT_GRAY, font=JosefinSans_20_BOLD)
        self.__dev_label.place(x=335, y=430)

        self.__devs_image = cstk.CTkImage(light_image=Image.open('assets/Devs.png'), size=(550, 40))
        self.__devs = cstk.CTkLabel(self, image=self.__devs_image, bg_color=LIGHT_GRAY, fg_color=LIGHT_GRAY, text='')
        center_img = set_center(master_width=600, master_height=450, child_width=550, child_height=40)
        self.__devs.place(x=center_img[0], y=350)

        self.__dark_mode_toggle_button = cstk.CTkButton(self, image=self.__dark_mode_toggle_image, height=29, width=63,
                                                        fg_color=LIGHT_GRAY, hover=cstk.FALSE,
                                                        bg_color=LIGHT_GRAY, text='', command=self.__DarkModeToggled)
        self.__dark_mode_toggle_button.place(x=468, y=45)

    def default_mode(self):
        self.__dark_mode_toggle_image.configure(light_image=Image.open('assets/ToggleButtonLarge.png'))
        self.__dark_mode_toggle_button.configure(image=self.__dark_mode_toggle_image)
        self.__DarkMode = False
        self.__root_frame.set_dark_mode()
        self.__dark_mode_toggle_button.configure(bg_color=LIGHT_GRAY, fg_color=LIGHT_GRAY)
        self.__theme_options_label.configure(fg=BLACK, bg=LIGHT_GRAY)
        self.__logo.configure(bg_color=LIGHT_GRAY, fg_color=LIGHT_GRAY, image=self.__logo_image)
        self.__dev_label.configure(bg=LIGHT_GRAY, fg=BLACK)
        self.__devs.configure(bg_color=LIGHT_GRAY, fg_color=LIGHT_GRAY, image=self.__devs_image)
        self.__ExitButton.configure(bg_color=LIGHT_GRAY, fg_color=LIGHT_GRAY, image=self.__XButton)
        self.configure(fg_color=LIGHT_GRAY, bg_color=WHITE)
    def dark_mode(self):
        self.__dark_mode_toggled_image = cstk.CTkImage(light_image=Image.open('assets/ToggleButtonLargeToggledWhite.png'),
                                                      size=(63, 29))
        self.__dark_mode_toggle_button.configure(image=self.__dark_mode_toggled_image)
        self.__DarkMode = True
        self.__root_frame.set_dark_mode()
        self.__dark_mode_toggle_button.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK)
        self.__theme_options_label.configure(fg=WHITE, bg=SETTINGS_DARK)
        logo_white = cstk.CTkImage(light_image=Image.open('assets/LOGOWhite.png'), size=(188, 117))
        self.__logo.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK, image=logo_white)
        self.__dev_label.configure(bg=SETTINGS_DARK, fg=WHITE)
        devs_white = cstk.CTkImage(light_image=Image.open('assets/DevsWhite.png'), size=(550, 40))
        self.__devs.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK, image=devs_white)
        self.__XButtonWhite = cstk.CTkImage(light_image=Image.open('assets/ExitButtonWhite.png'), size=(19, 19))
        self.__ExitButton.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK, image=self.__XButtonWhite)
        self.configure(fg_color=SETTINGS_DARK, bg_color=DARK_MODE_BACKGOUND)

    def ExitSettings(self):
        self.__root_frame.MAX_SETTINGS_OPENED = 1
        self.destroy()

    @staticmethod
    def getWidth():
        return 600

    @staticmethod
    def getHeight():
        return 450

    def __DarkModeToggled(self):
        if self.__DarkMode is False:
            self.dark_mode()
            self.__DarkMode = True
            self.__root_frame.set_dark_mode()
        else:
            self.default_mode()
            self.__DarkMode = False
            self.__root_frame.set_default_mode()

class CardPage(cstk.CTkFrame):
    def __init__(self, *args, color,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=876, height=505, corner_radius=20, fg_color=color, bg_color=WHITE, **kwargs)
        self.__bg_color = color
        ################################ COLLECTION NAME ##############################
        self.__collection_name = cstk.CTkLabel(self, text='', bg_color=color, text_color=WHITE,font=JosefinSans_30_BOLD)
        self.__collection_name.place(x=self.fit_to_dimensions(self.__collection_name), y=30)
        self.__collection_name_2 = cstk.CTkLabel(self, text='', bg_color=color, text_color=WHITE,
                                                 font=JosefinSans_30_BOLD)
        self.__collection_name_2.place(x=self.fit_to_dimensions(self.__collection_name_2), y=70)
        ################################ QUESTION OR ANSWER LABEL #########################
        self.__qa_label = cstk.CTkLabel(self, text='', bg_color=color, text_color=BLACK, font=JosefinSans_35_BOLD)
        # self.__qa_label.place(x=self.fit_to_dimensions(self.__qa_label, 3), y=200)
        self.__qa_label_2 = cstk.CTkLabel(self, text='', bg_color=color, text_color=BLACK, font=JosefinSans_35_BOLD)
        #self.__qa_label_2.place(x=self.fit_to_dimensions(self.__qa_label_2, 3), y=250)
        self.__qa_label_3 = cstk.CTkLabel(self, text='', bg_color=color, text_color=BLACK, font=JosefinSans_30_BOLD)
        #self.__qa_label_3.place(x=self.fit_to_dimensions(self.__qa_label_3, 3), y=290)
        self.__qa_label_4 = cstk.CTkLabel(self, text='', bg_color=color, text_color=BLACK, font=JosefinSans_30_BOLD)
        #self.__qa_label_4.place(x=self.fit_to_dimensions(self.__qa_label_4, 3), y=320)
        self.__qa_label_5 = cstk.CTkLabel(self, text='', bg_color=color, text_color=BLACK, font=JosefinSans_30_BOLD)
        #self.__qa_label_5.place(x=self.fit_to_dimensions(self.__qa_label_5, 3), y=350)
        ############################### CORRECT BUTTON ########################
        self.__correct_image = cstk.CTkImage(light_image=Image.open('assets/CORRECTBUTTON.png'), size=(70, 50))
        self.__correct_button = cstk.CTkButton(self, corner_radius=30, bg_color=color, border_width=0, height=50,
                                               width=70, fg_color=WHITE, text_color=BLACK, font=JosefinSans_20_BOLD,
                                               image=self.__correct_image, text='', hover=cstk.FALSE)
        self.__correct_button.place(x=228, y=420)
        ############################### WRONG BUTTON ###########################
        self.__wrong_image = cstk.CTkImage(light_image=Image.open('assets/WRONGBUTTON.png'), size=(70, 50))
        self.__wrong_button = cstk.CTkButton(self, corner_radius=30, bg_color=color, border_width=0, height=50,
                                               width=70, fg_color=WHITE, text_color=BLACK, font=JosefinSans_20_BOLD,
                                               image=self.__wrong_image, text='', hover=cstk.FALSE)
        self.__wrong_button.place(x=508, y=420)
        ############################### CARDS ##################################
        self.current = {}
        self.all_cards = {}

    def default_mode(self):
        self.configure(bg_color=WHITE)

    def dark_mode(self):
        self.configure(bg_color=DARK_MODE_BACKGOUND)

    @staticmethod
    def fit_to_dimensions(label: cstk.CTkLabel, font_shift: int = 0):
        text_in_pixels = 0
        tx = label.cget('text')
        for i in range(0, len(tx)):
            if tx[i] == 'e' or tx[i] == 'h' or tx[i] == 'k' or tx[i] == 'n' or tx[i] == 'o' or tx[i] == 'u':
                text_in_pixels += 16 + font_shift
            elif tx[i] == 'v' or tx[i] == 'x' or tx[i] == 'y':
                text_in_pixels += 16 + font_shift
            elif tx[i] == 'a' or tx[i] == 'd' or tx[i] == 'g' or tx[i] == 'F' or tx[i] == 'S' or tx[i] == 'T':
                text_in_pixels += 17 + font_shift
            elif tx[i] == 'b' or tx[i] == 'p' or tx[i] == 'B' or tx[i] == 'E' or tx[i] == 'L' or tx[i] == 'P':
                text_in_pixels += 18 + font_shift
            elif tx[i] == 'c' or tx[i] == 'z':
                text_in_pixels += 14 + font_shift
            elif tx[i] == 'f':
                text_in_pixels += 13 + font_shift
            elif tx[i] == 'i' or tx[i] == 'j' or tx[i] == 'l' or tx[i] == 'q':
                text_in_pixels += 7 + font_shift
            elif tx[i] == 'm' or tx[i] == 'O':
                text_in_pixels += 24 + font_shift
            elif tx[i] == 'r' or tx[i] == 's' or tx[i] == 't' or tx[i] == ' ':
                text_in_pixels += 12 + font_shift
            elif tx[i] == 'w' or tx[i] == 'C' or tx[i] == 'R' or tx[i] == 'Z':
                text_in_pixels += 20 + font_shift
            elif tx[i] == 'A' or tx[i] == 'G' or tx[i] == 'U' or tx[i] == 'V' or tx[i] == 'X' or tx[i] == 'Y' or tx[i] == 'K':
                text_in_pixels += 21 + font_shift
            elif tx[i] == 'D' or tx[i] == 'H':
                text_in_pixels += 22 + font_shift
            elif tx[i] == 'I':
                text_in_pixels += 8 + font_shift
            elif tx[i] == 'J':
                text_in_pixels += 10 + font_shift
            elif tx[i] == 'M' or tx[i] == 'Q':
                text_in_pixels += 26 + font_shift
            elif tx[i] == 'N':
                text_in_pixels += 23 + font_shift
            elif tx[i] == 'W':
                text_in_pixels += 30 + font_shift
            elif tx[i] == ',':
                text_in_pixels += 6 + font_shift

        text_in_pixels += 28 + font_shift
        CENTER_WIDTH = int(np.ceil(np.divide(876, 2)) - np.ceil(np.divide(text_in_pixels, 2)))
        return CENTER_WIDTH

    @staticmethod
    def text_splitter(text: str, words_in_line: int = 3):
        if len(text) >= 32:
            splitted_text = list(text.split(' '))
            first_line = ''
            second_line = ''
            third_line = ''
            forth_line = ''
            fifth_line = ''
            size = 0
            for word in splitted_text:
                if size < words_in_line:
                    if size < words_in_line:
                        first_line += word
                        first_line += ' '
                    size += 1
                elif size < 2*words_in_line:
                    if size < 2*words_in_line:
                        second_line += word
                        second_line += ' '
                    size += 1
                elif size < 3*words_in_line:
                    if size < 3*words_in_line:
                        third_line += word
                        third_line += ' '
                    size += 1
                elif size < 4*words_in_line:
                    if size < 4*words_in_line:
                        forth_line += word
                        forth_line += ' '
                    size += 1
                elif size < 5*words_in_line:
                    if size < 5*words_in_line:
                        fifth_line += word
                        fifth_line += ' '
            return first_line, second_line, third_line, forth_line, fifth_line.rstrip(' ')
        else:
            return text

    def set_collection_name(self, name: str):
        if len(name) > 32:
            splitted = self.text_splitter(name, 3)
            self.__collection_name.configure(text=splitted[0])
            self.__collection_name.place(x=self.fit_to_dimensions(self.__collection_name, -2), y=30)
            self.__collection_name_2.configure(text=splitted[1])
            self.__collection_name_2.place(x=self.fit_to_dimensions(self.__collection_name_2, -2), y=70)
        else:
            self.__collection_name.configure(text=name)
            self.__collection_name.place(x=self.fit_to_dimensions(self.__collection_name, -2), y=30)

    def set_Question_or_Answer(self, question_answer: str):
        if len(question_answer) <= 32:
            self.__qa_label.configure(text=question_answer)
            self.__qa_label.place(x=self.fit_to_dimensions(self.__qa_label, 3), y=200)
        elif 32 < len(question_answer) <= 71:
            splitted = self.text_splitter(question_answer, 3)
            self.__qa_label.configure(text=splitted[0])
            self.__qa_label.place(x=self.fit_to_dimensions(self.__qa_label, 3), y=180)
            self.__qa_label_2.configure(text=splitted[1])
            self.__qa_label_2.place(x=self.fit_to_dimensions(self.__qa_label_2, 3), y=250)
        elif 71 < len(question_answer) <= 110:
            splitted = self.text_splitter(question_answer, 6)
            self.__qa_label.configure(font=JosefinSans_30_BOLD)
            self.__qa_label.configure(text=splitted[0])
            self.__qa_label.place(x=self.fit_to_dimensions(self.__qa_label, 0), y=150)
            self.__qa_label_2.configure(font=JosefinSans_30_BOLD)
            self.__qa_label_2.configure(text=splitted[1])
            self.__qa_label_2.place(x=self.fit_to_dimensions(self.__qa_label_2, 0), y=195)
            self.__qa_label_3.configure(text=splitted[2])
            self.__qa_label_3.place(x=self.fit_to_dimensions(self.__qa_label_3, 0), y=240)
        elif 110 < len(question_answer) <= 200:
            splitted = self.text_splitter(question_answer, 5)
            self.__qa_label.configure(font=JosefinSans_30_BOLD)
            self.__qa_label.configure(text=splitted[0])
            self.__qa_label.place(x=self.fit_to_dimensions(self.__qa_label, 0), y=130)
            self.__qa_label_2.configure(font=JosefinSans_30_BOLD)
            self.__qa_label_2.configure(text=splitted[1])
            self.__qa_label_2.place(x=self.fit_to_dimensions(self.__qa_label_2, 0), y=175)
            self.__qa_label_3.configure(text=splitted[2])
            self.__qa_label_3.place(x=self.fit_to_dimensions(self.__qa_label_3, 0), y=220)
            self.__qa_label_4.configure(text=splitted[3])
            self.__qa_label_4.place(x=self.fit_to_dimensions(self.__qa_label_4, 0), y=265)
            self.__qa_label_5.configure(text=splitted[4])
            self.__qa_label_5.place(x=self.fit_to_dimensions(self.__qa_label_5, 0), y=310)

    def setWrongFunction(self, func):
        self.__wrong_button.configure(command=func)

    def setCorrectFunction(self, func):
        self.__correct_button.configure(command=func)


class Permission(cstk.CTkFrame):
    def __init__(self, root, *args, target: str,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=406, height=146, corner_radius=20, fg_color=LIGHT_GRAY, **kwargs
                         , bg_color=WHITE)
        self.__root = root
        self.__confirmed_ = False
        self.__canceled_ = False
        self.__target = target
        self.__question_label = cstk.CTkLabel(self, text='', text_color=BLACK, font=JosefinSans_20_BOLD,
                                              bg_color=LIGHT_GRAY)
        self.__question_label.place(x=50, y=15)
        self.__request_label = cstk.CTkLabel(self, text='', text_color=BLACK, font=JosefinSans_20_BOLD,
                                              bg_color=LIGHT_GRAY)
        self.__request_label.place(x=50, y=45)
        self.__confirm_button = cstk.CTkButton(self, corner_radius=30, text='CONFIRM', text_color=WHITE,
                                               font=JosefinSans_20_BOLD, height=30, width=150, hover=cstk.FALSE,
                                               fg_color=GRAY_B1, bg_color=LIGHT_GRAY, command=self.__confirmed)
        self.__confirm_button.place(x=30, y=90)
        self.__cancel_button = cstk.CTkButton(self, corner_radius=30, text='CANCEL', text_color=WHITE,
                                               font=JosefinSans_20_BOLD, height=30, width=150, hover=cstk.FALSE,
                                               fg_color=GRAY_B1, bg_color=LIGHT_GRAY, command=self.__canceled)
        self.__cancel_button.place(x=226, y=90)

    def request(self, option: str):
        if option.upper() == 'DELETE':
            self.__request = 'ARE YOU SURE YOU WANT TO DELETE, ' + self.__target + '?'
        if len(self.__request) > 20:
            splitted = self.text_splitter(self.__request, 6)
            self.__question_label.configure(text=splitted[0])
            self.__question_label.place(x=self.fit_to_dimensions(self.__question_label), y=15)
            self.__request_label.configure(text=splitted[1])
            self.__request_label.place(x=self.fit_to_dimensions(self.__request_label), y=45)
        else:
            self.__question_label.configure(text=self.__request_label)
            self.__question_label.place(x=self.fit_to_dimensions(self.__question_label), y=15)

    def __confirmed(self):
        filename = FM.name_to_filename(self.__target)

        if os.path.exists('data/' + filename + '.csv'):
            os.remove('data/' + filename + '.csv')

        if os.path.exists('serialfiles/' + filename + '.json') is True:
            os.remove('serialfiles/' + filename + '.json')

        with open('serialfiles/SuperFile.json') as superfile:
            superdata = json.load(superfile)
        for i in range(0, len(superdata)):
            if superdata[i]["collection_name"].upper() == self.__target.upper():
                del superdata[i]
                break
        with open('serialfiles/SuperFile.json', 'w') as superfile:
            json.dump(superdata, superfile, indent=2)

        main = self.__root.getSuperRoot()
        self.__root.destroy()
        main.clean_then_reload()
        self.destroy()


    def __canceled(self):
        self.destroy()

    @staticmethod
    def fit_to_dimensions(label: cstk.CTkLabel):
        text_in_pixels = 0
        tx = label.cget('text')
        for i in range(0, len(tx)):
            if tx[i] == 'e' or tx[i] == 'h' or tx[i] == 'k' or tx[i] == 'n' or tx[i] == 'o' or tx[i] == 'u':
                text_in_pixels += 11
            elif tx[i] == 'v' or tx[i] == 'x' or tx[i] == 'y':
                text_in_pixels += 11
            elif tx[i] == 'a' or tx[i] == 'd' or tx[i] == 'g' or tx[i] == 'F' or tx[i] == 'S' or tx[i] == 'T':
                text_in_pixels += 12
            elif tx[i] == 'b' or tx[i] == 'p' or tx[i] == 'B' or tx[i] == 'E' or tx[i] == 'L' or tx[i] == 'P':
                text_in_pixels += 12
            elif tx[i] == 'c' or tx[i] == 'z':
                text_in_pixels += 10
            elif tx[i] == 'f':
                text_in_pixels += 9
            elif tx[i] == 'i' or tx[i] == 'j' or tx[i] == 'l' or tx[i] == 'q':
                text_in_pixels += 5
            elif tx[i] == 'm' or tx[i] == 'O':
                text_in_pixels += 16
            elif tx[i] == 'r' or tx[i] == 's' or tx[i] == 't' or tx[i] == ' ':
                text_in_pixels += 8
            elif tx[i] == 'w' or tx[i] == 'C' or tx[i] == 'R' or tx[i] == 'Z' or tx[i] == 'K':
                text_in_pixels += 14
            elif tx[i] == 'A' or tx[i] == 'G' or tx[i] == 'U' or tx[i] == 'V' or tx[i] == 'X' or tx[i] == 'Y':
                text_in_pixels += 14
            elif tx[i] == 'D' or tx[i] == 'H':
                text_in_pixels += 15
            elif tx[i] == 'I':
                text_in_pixels += 6
            elif tx[i] == 'J':
                text_in_pixels += 7
            elif tx[i] == 'M' or tx[i] == 'Q':
                text_in_pixels += 18
            elif tx[i] == 'N':
                text_in_pixels += 16
            elif tx[i] == 'W':
                text_in_pixels += 20
            elif tx[i] == ',':
                text_in_pixels += 4

        text_in_pixels += 15

        CENTER_WIDTH = int(np.ceil(np.divide(406, 2)) - np.ceil(np.divide(text_in_pixels, 2)))
        return CENTER_WIDTH

    @staticmethod
    def text_splitter(text: str, words_in_line: int = 3):
        if len(text) >= 32:
            splitted_text = list(text.split(' '))
            first_line = ''
            second_line = ''
            size = 0
            for word in splitted_text:
                if size < words_in_line:
                    if size < words_in_line:
                        first_line += word
                        first_line += ' '
                    size += 1
                elif size < 2*words_in_line:
                    if size < 2*words_in_line:
                        second_line += word
                        second_line += ' '
                    size += 1
            return first_line, second_line
        else:
            return text

    def dark_mode(self):
        pass
class ModifyQA(cstk.CTkFrame):
    def __init__(self, *args,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=660, height=120, corner_radius=20, fg_color=LIGHT_GRAY, **kwargs
                         , bg_color=LIGHT_GRAY)

        ###################### QUESTION LABEL ########################
        self.__Question_label = Label(self, text="QUESTION:", fg=BLACK, bg=LIGHT_GRAY, font=JosefinSans_20_BOLD)
        self.__Question_label.place(x=75, y=0)
        ###################### ANSWER LABEL ############################
        self.__Answer_label = Label(self, text="ANSWER:", fg=BLACK, bg=LIGHT_GRAY, font=JosefinSans_20_BOLD)
        self.__Answer_label.place(x=560, y=0)
        ###################### QUESTION ENTRY #########################
        self.Question_Input_Field = cstk.CTkTextbox(self, height=10, width=280, text_color=WHITE, corner_radius=20
                                                      , font=JosefinSans_20_BOLD, fg_color=GRAY_B1)
        self.Question_Input_Field.place(x=44, y=30)
        ###################### ANSWER ENTRY #########################
        self.Answer_Input_Field = cstk.CTkTextbox(self, height=10, width=280, text_color=WHITE, corner_radius=20
                                                    , font=JosefinSans_20_BOLD, fg_color=GRAY_B1)
        self.Answer_Input_Field.place(x=366, y=30)
        ###################### REMOVE BUTTON ########################
        self.__remove_x_image = cstk.CTkImage(light_image=Image.open('assets/XBUTTONBLACK.png'), size=(25, 25))
        self.__remove_x_button = cstk.CTkButton(self, image=self.__remove_x_image, text='', bg_color=LIGHT_GRAY,
                                                hover=cstk.FALSE, height=25, width=25, fg_color=LIGHT_GRAY)
        self.__remove_x_button.place(x=-4, y=50)

    def x_button_call(self, function):
        self.__remove_x_button.configure(command=function)

    def dark_mode(self):
        self.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__Question_label.configure(fg=WHITE, bg=SETTINGS_DARK)
        self.__Answer_label.configure(fg=WHITE, bg=SETTINGS_DARK)
        self.__remove_x_button.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK
                                         , image=cstk.CTkImage(Image.open('assets/XBUTTONDARKMODE.png'), size=(25, 25)))
class Modify(cstk.CTkFrame):
    def __init__(self, *args, root, card_name, color,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=720, height=676, corner_radius=20, fg_color=LIGHT_GRAY, **kwargs
                         , bg_color=WHITE)
        self.__root = root
        self.__ColorClicked = [False, False, False, False, False, False, False]
        self.__custom_color = color
        self.MAX_COLOR_PICKER = 1
        self.__collectionname = card_name
        ################################ FLASHCARD NAME #############################
        self.__flashcard_name = Label(self, text="FLASHCARD'S NAME:", fg=BLACK, bg=LIGHT_GRAY,font=JosefinSans_20_BOLD)
        self.__flashcard_name.place(x=390, y=40)

        ################################ FLASHCARD INPUT FIELD ######################
        self.__flashcard_name_input = cstk.CTkTextbox(self, text_color=WHITE, fg_color=GRAY_B1, border_width=0
                                                , bg_color=LIGHT_GRAY, font=JosefinSans_20_BOLD, height=10, width=375
                                                , corner_radius=20, activate_scrollbars=cstk.FALSE)
        self.__flashcard_name_input.place(x=173, y=70)
        ################################ FLASHCARD COLOR ###################
        self.__flashcard_color_label = Label(self, text="FLASHCARD'S COLOR:", fg=BLACK,bg=LIGHT_GRAY,
                                            font=JosefinSans_20_BOLD)
        self.__flashcard_color_label.place(x=390, y=230)
        ################# RECOMMENDED COLOR 1 - MUSTARD YELLOW ##################
        self.__m_yellow_color = cstk.CTkImage(light_image=Image.open('assets/YELLOW_UNSELECTED.png'), size=(75, 35))
        self.__m_yellow_color_button = cstk.CTkButton(self, width=75, height=35, image=self.__m_yellow_color, text='',
                                               fg_color=LIGHT_GRAY, border_width=0, hover=cstk.FALSE,
                                               bg_color=LIGHT_GRAY, command=self.m_yellow_selected)
        self.__m_yellow_color_button.place(x=105, y=190)
        ################# RECOMMENDED COLOR 2 - MINT #########################
        self.__mint_color = cstk.CTkImage(light_image=Image.open('assets/MINT_UNSELECTED.png'), size=(75, 35))
        self.__mint_color_button = cstk.CTkButton(self, width=75, height=35, image=self.__mint_color, text='',
                                           fg_color=LIGHT_GRAY, border_width=0, hover=cstk.FALSE, bg_color=LIGHT_GRAY
                                           , command=self.fresh_mint_selected)
        self.__mint_color_button.place(x=190, y=190)
        ########################## RECOMMENDED COLOR 3 - DARK MINT #########################
        self.__dark_mint_color = cstk.CTkImage(light_image=Image.open('assets/DARK_MINT_UNSELECTED.png'), size=(75, 35))
        self.__dark_mint_color_button = cstk.CTkButton(self, width=75, height=35, image=self.__dark_mint_color,
                                                text='', fg_color=LIGHT_GRAY, border_width=0, hover=cstk.FALSE,
                                                bg_color=LIGHT_GRAY, command=self.dark_mint_selected)
        self.__dark_mint_color_button.place(x=275, y=190)
        ########################## RECOMMENDED COLOR 4 - KHAKI ###########################
        self.__khaki_color = cstk.CTkImage(light_image=Image.open('assets/KHAKI_UNSELECTED.png'), size=(75, 35))
        self.__khaki_color_button = cstk.CTkButton(self, width=75, height=35, image=self.__khaki_color, text='',
                                            fg_color=LIGHT_GRAY, border_width=0, hover=cstk.FALSE, bg_color=LIGHT_GRAY,
                                            command=self.khaki_selected)
        self.__khaki_color_button.place(x=360, y=190)
        ########################## RECOMMENDED COLOR 5 - DARK BLUE #######################
        self.__dark_blue_color = cstk.CTkImage(light_image=Image.open('assets/DARK_BLUE_UNSELECTED.png'), size=(75, 35))
        self.__dark_blue_color_button = cstk.CTkButton(self, width=75, height=35, image=self.__dark_blue_color,
                                                text='', fg_color=LIGHT_GRAY, border_width=0, hover=cstk.FALSE,
                                                bg_color=LIGHT_GRAY, command=self.dark_blue_selected)
        self.__dark_blue_color_button.place(x=445, y=190)
        ########################## RECOMMENDED COLOR 6 - LIGHT PINK ######################
        self.__light_pink_color = cstk.CTkImage(light_image=Image.open('assets/LIGHT_PINK_UNSELECTED.png'), size=(75, 35))
        self.__light_pink_color_button = cstk.CTkButton(self, width=75, height=35, image=self.__light_pink_color,
                                                 text='', fg_color=LIGHT_GRAY, border_width=0, hover=cstk.FALSE,
                                                 bg_color=LIGHT_GRAY, command=self.light_pink_selected)
        self.__light_pink_color_button.place(x=530, y=190)
        ########################## CUSTOM COLOR PICKER ############################
        self.__color_picker_button = cstk.CTkButton(self, width=110, height=35, text='CUSTOM', text_color=WHITE,
                                             corner_radius=20, fg_color=GRAY_B1, font=JosefinSans_20_BOLD
                                             , bg_color=LIGHT_GRAY, command=self.custom_color_selected,
                                             hover_color=BLACK)
        self.__color_picker_button.place(x=112, y=240)
        ############################ FIRST QA MODIFIER ###########################
        self.__first_qa_modifier = ModifyQA(self)
        self.__first_qa_modifier.place(x=17, y=300)
        self.__first_qa_modifier.Question_Input_Field.bind("<Leave>", command=self.saveQuestionFirstModifier)
        self.__first_qa_modifier.Answer_Input_Field.bind("<Leave>", command=self.saveAnswerFirstModifier)
        self.__first_qa_modifier.x_button_call(self.removeFirstQA)
        ############################ SECOND QA MODIFIER ##########################
        self.__second_qa_modifier = ModifyQA(self)
        self.__second_qa_modifier.place(x=17, y=410)
        self.__second_qa_modifier.Question_Input_Field.bind("<Leave>", command=self.saveQuestionSecondModifier)
        self.__second_qa_modifier.Answer_Input_Field.bind("<Leave>", command=self.saveAnswerSecondModifier)
        self.__second_qa_modifier.x_button_call(self.removeSecondQA)
        ############################ PREVIOUS AND NEXT BUTTONS ############################
        self.__back_image = cstk.CTkImage(light_image=Image.open('assets/Back.png'), size=(13, 14))
        self.__next_image = cstk.CTkImage(light_image=Image.open('assets/Next.png'), size=(13, 14))

        self.__back_button = cstk.CTkButton(self, image=self.__back_image, width=13, height=14, hover=cstk.FALSE,
                                       fg_color=LIGHT_GRAY, bg_color=LIGHT_GRAY, text='', command=self.load_previous)
        self.__back_button.place(x=190, y=560)
        #self.__back_button.configure(command=self.__load_previous_page)

        self.__next_button = cstk.CTkButton(self, image=self.__next_image, width=13, height=14, hover=cstk.FALSE,
                                       fg_color=LIGHT_GRAY, bg_color=LIGHT_GRAY, text='', command=self.load_next)
        #self.__next_button.configure(command=self.__load_next_page)
        self.__next_button.place(x=500, y=560)
        ############################ ADD CARD BUTTON #############################
        self.__add_card_button = cstk.CTkButton(self, text='ADD CARD', fg_color=GRAY_B1, hover_color=BLACK,
                                                corner_radius=20, font=JosefinSans_20_BOLD, height=40, width=155,
                                                text_color=WHITE, command=self.add_card)
        self.__add_card_button.place(x=280, y=550)
        ########################## CONFIRM BUTTON #########################
        self.__confirm_button = cstk.CTkButton(self, width=155, height=40, corner_radius=20, text_color=WHITE,
                                               text="CONFIRM", hover_color=BLACK, fg_color=GRAY_B1,
                                               font=JosefinSans_20_BOLD
                                               , bg_color=LIGHT_GRAY, command=self.confirm)
        self.__confirm_button.place(x=186, y=620)
        ########################## CANCEL BUTTON #########################
        self.__cancel_button = cstk.CTkButton(self, width=155, height=40, corner_radius=20, text_color=WHITE,
                                              text="CANCEL", hover_color=BLACK, fg_color=GRAY_B1,
                                              font=JosefinSans_20_BOLD
                                              , bg_color=LIGHT_GRAY, command=self.destroy)
        self.__cancel_button.place(x=385, y=620)
        ######################### DATA ########################
        self.__card_data = None
        self.__data_index = 0
        self.__data_size = 0
        self.__updates = []
        self.__card_added = False

    def dark_mode(self):
        self.configure(fg_color=SETTINGS_DARK, bg_color=DARK_MODE_BACKGOUND)
        self.__flashcard_name.configure(fg=WHITE, bg=SETTINGS_DARK)
        self.__flashcard_color_label.configure(fg=WHITE, bg=SETTINGS_DARK)
        self.__m_yellow_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__mint_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__dark_blue_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__dark_mint_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__khaki_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__light_pink_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.__back_button.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK)
        self.__next_button.configure(bg_color=SETTINGS_DARK, fg_color=SETTINGS_DARK)
        self.__first_qa_modifier.dark_mode()
        self.__second_qa_modifier.dark_mode()

    def saveQuestionFirstModifier(self, e):
        question = str(self.__first_qa_modifier.Question_Input_Field.get('1.0', '1.end'))
        if self.__card_data is None:
            pass
        else:
            for i in range(0, len(self.__card_data)):
                if i == self.__data_index:
                    self.__card_data[i]["Question"] = question
                    break

    def saveAnswerFirstModifier(self, e):
        answer = str(self.__first_qa_modifier.Answer_Input_Field.get('1.0', '1.end'))
        if self.__card_data is None:
            pass
        else:
            for i in range(0, len(self.__card_data)):
                if i == self.__data_index:
                    self.__card_data[i]["Answer"] = answer
                    break

    def saveQuestionSecondModifier(self, e):
        question = str(self.__second_qa_modifier.Question_Input_Field.get('1.0', '1.end'))

        if self.__card_data is None:
            pass
        else:
            for i in range(0, len(self.__card_data)):
                if i == self.__data_index + 1:
                    self.__card_data[i]["Question"] = question
                    break

    def saveAnswerSecondModifier(self, e):
        answer = str(self.__second_qa_modifier.Answer_Input_Field.get('1.0', '1.end'))
        if self.__card_data is None:
            pass
        else:
            for i in range(0, len(self.__card_data)):
                if i == self.__data_index + 1:
                    self.__card_data[i]["Answer"] = answer
                    break

    def m_yellow_selected(self):
        if self.__ColorClicked[0] is True:
            self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.__ColorClicked[0] = False
        else:
            self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/M_YELLOW_SELECTED.png'),
                                                                size=(75, 35)))
            for i in range(0, len(self.__ColorClicked)):
                if i == 0:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 1:
                        self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 2:
                        self.__dark_mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.__dark_blue_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.__color_picker_button.configure(fg_color=GRAY_B1)

    def fresh_mint_selected(self):
        if self.__ColorClicked[1] is True:
            self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.__ColorClicked[1] = False
        else:
            self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_SELECTED.png'),
                                                                size=(75, 35)))
            for i in range(0, len(self.__ColorClicked)):
                if i == 1:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 0:
                        self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.__dark_mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.__dark_blue_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.__color_picker_button.configure(fg_color=GRAY_B1)

    def dark_mint_selected(self):
        if self.__ColorClicked[2] is True:
            self.__dark_mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.__ColorClicked[2] = False
        else:
            self.__dark_mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_MINT_SELECTED.png'),
                                                                size=(75, 35)))
            for i in range(0, len(self.__ColorClicked)):
                if i == 2:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 0:
                        self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 3:
                        self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.__dark_blue_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.__color_picker_button.configure(fg_color=GRAY_B1)

    def khaki_selected(self):
        if self.__ColorClicked[3] is True:
            self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'), size=(75, 35)))
            self.__ColorClicked[3] = False
        else:
            self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_SELECTED.png'),
                                                             size=(75, 35)))
            for i in range(0, len(self.__ColorClicked)):
                if i == 3:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 0:
                        self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.__dark_mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.__dark_blue_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.__color_picker_button.configure(fg_color=GRAY_B1)

    def dark_blue_selected(self):
        if self.__ColorClicked[4] is True:
            self.__dark_blue_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.__ColorClicked[4] = False
        else:
            self.__dark_blue_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_BLUE_SELECTED.png'),
                                                             size=(75, 35)))
            for i in range(0, len(self.__ColorClicked)):
                if i == 4:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 0:
                        self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.__dark_mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                         size=(75, 35)))
                    elif i == 5:
                        self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.__color_picker_button.configure(fg_color=GRAY_B1)

    def light_pink_selected(self):
        if self.__ColorClicked[5] is True:
            self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.__ColorClicked[5] = False
        else:
            self.__light_pink_color_button.configure(image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_SELECTED.png'),
                                                             size=(75, 35)))
            for i in range(0, len(self.__ColorClicked)):
                if i == 5:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 0:
                        self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.__dark_mint_color_button.configure(
                            image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                         size=(75, 35)))
                    elif i == 4:
                        self.__dark_blue_color_button.configure(
                            image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                           size=(75, 35)))
                    elif i == 6:
                        self.__color_picker_button.configure(fg_color=GRAY_B1)

    def colorPicker(self):
        self.__custom_color_frame = ColorPicker(self.__root)
        self.__custom_color_frame.protocol("WM_DELETE_WINDOW", self.GetColorThenDestroy)

    def GetColorThenDestroy(self):
        if str(self.__custom_color_frame.getColor())[0] == "#":
            self.__custom_color = str(self.__custom_color_frame.getColor())
        else:
            self.__custom_color = DEFAULT_CARD_COLOR
        self.__color_picker_button.configure(fg_color=self.__custom_color)
        self.__ColorClicked[6] = False
        self.__custom_color_frame.destroy()

    def custom_color_selected(self):
        if self.__ColorClicked[6] is True:
            if str(self.__custom_color_frame.getColor())[0] == "#":
                self.__custom_color = str(self.__custom_color_frame.getColor())
            else:
                self.__custom_color = DEFAULT_CARD_COLOR
            self.__custom_color_frame.destroy()
            self.__color_picker_button.configure(fg_color=self.__custom_color)
        else:
            self.MAX_COLOR_PICKER = 1
            self.__color_picker_button.configure(fg_color=BLACK)
            for i in range(0, len(self.__ColorClicked)):
                if i == 6:
                    self.__ColorClicked[i] = True
                else:
                    self.__ColorClicked[i] = False
                    if i == 0:
                        self.__m_yellow_color_button.configure(image=cstk.CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.__mint_color_button.configure(image=cstk.CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.__dark_mint_color_button.configure(
                            image=cstk.CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.__khaki_color_button.configure(image=cstk.CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                         size=(75, 35)))
                    elif i == 4:
                        self.__dark_blue_color_button.configure(
                            image=cstk.CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                           size=(75, 35)))
                    elif i == 5:
                        self.__light_pink_color_button.configure(
                            image=cstk.CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                           size=(75, 35)))

        if self.MAX_COLOR_PICKER < 2:
            self.colorPicker()
            self.MAX_COLOR_PICKER += 1

    def Initialize(self, collection_name: str):

        self.__flashcard_name_input.insert('0.0', text=collection_name)
        if self.__card_data is None:
            pass
        elif len(self.__card_data) == 0:
            self.__first_qa_modifier.Question_Input_Field.delete('0.0', 'end')
            self.__first_qa_modifier.Answer_Input_Field.delete('0.0', 'end')
            self.__second_qa_modifier.Question_Input_Field.delete('0.0', 'end')
            self.__second_qa_modifier.Answer_Input_Field.delete('0.0', 'end')
        elif len(self.__card_data) == 1:
            self.__first_qa_modifier.Question_Input_Field.insert('0.0', text=self.__card_data[self.__data_index]['Question'])
            self.__first_qa_modifier.Answer_Input_Field.insert('0.0', text=self.__card_data[self.__data_index]['Answer'])
            self.__second_qa_modifier.Question_Input_Field.delete('0.0', 'end')
            self.__second_qa_modifier.Answer_Input_Field.delete('0.0', 'end')
        elif len(self.__card_data) >= 2:
            self.__first_qa_modifier.Question_Input_Field.insert('0.0',
                                                                 text=self.__card_data[self.__data_index]['Question'])
            self.__first_qa_modifier.Answer_Input_Field.insert('0.0',
                                                               text=self.__card_data[self.__data_index]['Answer'])
            self.__second_qa_modifier.Question_Input_Field.insert('0.0', text=self.__card_data[self.__data_index + 1][
                'Question'])
            self.__second_qa_modifier.Answer_Input_Field.insert('0.0',
                                                                text=self.__card_data[self.__data_index + 1]['Answer'])

    def read_data(self):
        self.__card_data = FM.read_from_csv(self.__collectionname)

    def load_next(self):

        self.__back_button.configure(state=cstk.ACTIVE)
        self.__data_size = len(self.__card_data)
        if self.__data_index >= self.__data_size:
            self.__next_button.configure(state=cstk.ACTIVE)
        else:
            if self.__data_size == 2:
                self.__next_button.configure(state=cstk.DISABLED)
            else:
                self.__data_index += 2
            self.__first_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
            self.__first_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
            self.__second_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
            self.__second_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
            if self.__data_index + 1 == self.__data_size:
                self.__next_button.configure(state=cstk.DISABLED)
                self.__first_qa_modifier.Question_Input_Field.insert('1.0', text=self.__card_data[self.__data_index]['Question'])
                self.__first_qa_modifier.Answer_Input_Field.insert('1.0', text=self.__card_data[self.__data_index]['Answer'])
            else:
                self.__first_qa_modifier.Question_Input_Field.insert('1.0', text=self.__card_data[self.__data_index][
                    'Question'])
                self.__first_qa_modifier.Answer_Input_Field.insert('1.0',
                                                                   text=self.__card_data[self.__data_index]['Answer'])
                self.__second_qa_modifier.Question_Input_Field.insert('1.0',
                                                                      text=self.__card_data[self.__data_index + 1][
                                                                          'Question'])
                self.__second_qa_modifier.Answer_Input_Field.insert('1.0', text=self.__card_data[self.__data_index + 1][
                    'Answer'])

    def load_previous(self):

        self.__next_button.configure(state=cstk.ACTIVE)
        self.__data_size = len(self.__card_data)
        if self.__data_index <= 0:
            self.__back_button.configure(state=cstk.DISABLED)
        else:
            self.__data_index -= 2
            self.__first_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
            self.__first_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
            self.__second_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
            self.__second_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
            if self.__data_index + 1 == self.__data_size:
                self.__first_qa_modifier.Question_Input_Field.insert('1.0', text=self.__card_data[self.__data_index]['Question'])
                self.__first_qa_modifier.Answer_Input_Field.insert('1.0', text=self.__card_data[self.__data_index]['Answer'])
            else:
                self.__first_qa_modifier.Question_Input_Field.insert('1.0', text=self.__card_data[self.__data_index][
                    'Question'])
                self.__first_qa_modifier.Answer_Input_Field.insert('1.0',
                                                                   text=self.__card_data[self.__data_index]['Answer'])
                self.__second_qa_modifier.Question_Input_Field.insert('1.0',
                                                                      text=self.__card_data[self.__data_index + 1][
                                                                          'Question'])
                self.__second_qa_modifier.Answer_Input_Field.insert('1.0', text=self.__card_data[self.__data_index + 1][
                    'Answer'])

    def add_card(self):
        if self.__card_added is False:
            self.__second_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
            self.__second_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
            self.__card_added = True
        else:
            question = str(self.__second_qa_modifier.Question_Input_Field.get('1.0', '1.end'))
            answer = str(self.__second_qa_modifier.Answer_Input_Field.get('1.0', '1.end'))
            if len(question) > 0 and len(answer) > 0:
                self.__card_data.append({"Question": question, "Answer": answer})
                self.__second_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
                self.__second_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
                self.__second_qa_modifier.Question_Input_Field.insert('1.0', text=self.__card_data[self.__data_index + 1]['Question'])
                self.__second_qa_modifier.Answer_Input_Field.insert('1.0', text=self.__card_data[self.__data_index + 1]['Answer'])
            self.__card_added = False

    def removeFirstQA(self):
        collection_to_remove = {
            "Question": self.__card_data[self.__data_index]["Question"],
            "Answer": self.__card_data[self.__data_index]["Answer"]
        }
        self.__first_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
        self.__first_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
        self.__card_data.remove(collection_to_remove)

    def removeSecondQA(self):
        collection_to_remove = {
            "Question": self.__card_data[self.__data_index + 1]["Question"],
            "Answer": self.__card_data[self.__data_index + 1]["Answer"]
        }
        self.__second_qa_modifier.Question_Input_Field.delete('1.0', '1.end')
        self.__second_qa_modifier.Answer_Input_Field.delete('1.0', '1.end')
        self.__card_data.remove(collection_to_remove)

    def confirm(self):
        card_new_name = str(self.__flashcard_name_input.get('1.0', '1.end'))
        card__color__ = self.__custom_color

        if self.__ColorClicked[0] is True:
            card__color__ = MUSTARD_YELLOW
        elif self.__ColorClicked[1] is True:
            card__color__ = FRESH_MINT
        elif self.__ColorClicked[2] is True:
            card__color__ = DARK_MINT
        elif self.__ColorClicked[3] is True:
            card__color__ = KHAKI
        elif self.__ColorClicked[4] is True:
            card__color__ = DARK_BLUE
        elif self.__ColorClicked[5] is True:
            card__color__ = LIGHT_PINK

        filename = FM.name_to_filename(self.__collectionname)
        pd.DataFrame([('Question', 'Answer')]).to_csv('data/' + filename + '.csv', header=False, index=False, mode='w')
        pd.DataFrame(self.__card_data).to_csv('data/' + filename + '.csv', header=False, index=False, mode='a')
        FM.Card_Count_Changer(len(self.__card_data), self.__collectionname)
        with open('serialfiles/SuperFile.json', 'r') as superfile:
            data = json.load(superfile)
        if type(data) is dict:
            data = [data]
        for iterator in data:
            if iterator["collection_name"] == self.__collectionname:
                iterator["collection_name"] = card_new_name
                iterator["collection_color"] = card__color__

        with open('serialfiles/SuperFile.json', 'w') as superfile:
            json.dump(data, superfile, indent=2)

        with open('serialfiles/' + filename + '.json', 'r') as file:
            filedata = json.load(file)

        filedata["collection_name"] = card_new_name
        filedata["collection_color"] = card__color__

        with open('serialfiles/' + filename + '.json', 'w') as file:
            json.dump(filedata, file, indent=2)

        if filename != FM.name_to_filename(card_new_name):
            os.rename('serialfiles/' + filename + '.json', 'serialfiles/' + FM.name_to_filename(card_new_name) + '.json')
            os.rename('data/' + filename + '.csv', 'data/' + FM.name_to_filename(card_new_name) + '.csv')

        self.__root.clean_then_reload()
        self.destroy()

