
from FlashcardAdder import FlashCardAdder
from tkinter import *
from ColorPicker import *
import CustomWidgets as CW
import GridSystem
import json

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1150x800")
        self.title("K A R T A")
        self.config(bg=WHITE)
        self.resizable(FALSE, FALSE)
        self.iconbitmap('assets/icons/KARTA_ICON.ico')

        with open("serialfiles/settings.json") as fp:
            parameters = json.load(fp)

        self.Darkmode = parameters["dark"]
        ############ APP_NAME ##############
        self.__logo = CTkButton(self, text="K A R T A", border_width=0, font=JosefinSans_22_BOLD,
                         text_color=BLACK, fg_color=WHITE, bg_color=WHITE, hover=FALSE, anchor='nw')
        self.__logo.place(x=23, y=30)

        ############### ADD CARD BUTTON ################
        self.__plus_image = CTkImage(light_image=Image.open('assets/ADD_CARD_BUTTON.png'), size=(30, 30))
        self.__add_card_button = CTkButton(self, width=32, height=32, image=self.__plus_image, fg_color=WHITE,
                                    border_width=0, text='', bg_color=WHITE, hover=FALSE, command=self.flash_card_adder)
        self.__add_card_button.place(x=1030, y=30)

        ############ SETTINGS BUTTON ###############
        self.__settings_image = CTkImage(light_image=Image.open('assets/SETTINGS.png'), size=(32, 32))
        self.__settings_button = CTkButton(self, width=32, height=32, image=self.__settings_image, fg_color=WHITE,
                                    border_width=0, text='', bg_color=WHITE, hover=FALSE, command=self.settings)
        self.__settings_button.place(x=1080, y=30)

        ################ FRAME ####################
        self.__Exterior_Frame = CTkFrame(self, fg_color=WHITE, border_width=0, bg_color=WHITE, width=1110
                                  , height=670)
        self.__Exterior_Frame.place(x=30, y=100)

        self.__internal_frame = CTkFrame(self.__Exterior_Frame, width=1110, height=670, fg_color=WHITE, border_width=0,
                                  border_color=BLACK)
        self.__internal_frame.place(x=0, y=0)

        self.__back_image = None
        self.__next_image = None

        self.__back_button = None
        self.__next_button = None

        self.__page_index = 0
        self.__card_index = 0

        self.MAX_FLASHCARD_ADDER = 1
        self.MAX_SETTINGS_OPENED = 1

        self.super_reload()

        if self.Darkmode is True:
            self.set_dark_mode()
        else:
            self.set_default_mode()

        self.protocol("WM_DELETE_WINDOW", self.__on_close)

    def flash_card_adder(self):

        if self.MAX_FLASHCARD_ADDER < 2:
            if self.Darkmode is False:
                adder = FlashCardAdder(master=self, root=self)
                center = GridSystem.set_center(master_width=1150, master_height=800,
                                               child_width=adder.getWidth(),
                                               child_height=adder.getHeight())
                adder.place(x=center[0], y=center[1])
            else:
                adder = FlashCardAdder(master=self, root=self)
                center = GridSystem.set_center(master_width=1150, master_height=800,
                                               child_width=adder.getWidth(),
                                               child_height=adder.getHeight())
                adder.place(x=center[0], y=center[1])
                adder.dark_mode()
            self.MAX_FLASHCARD_ADDER += 1

    def settings(self):
        if self.MAX_SETTINGS_OPENED < 2:
            self.MAX_SETTINGS_OPENED += 1
            if self.Darkmode is True:
                settings_card = CW.Settings(master=self, root=self, dark=True)
                center = GridSystem.set_center(master_width=1150, master_height=800, child_width=settings_card.getWidth(),
                                               child_height=settings_card.getHeight())
                settings_card.place(x=center[0], y=center[1])
                settings_card.dark_mode()
            else:
                settings_card = CW.Settings(master=self, root=self, dark=False)
                center = GridSystem.set_center(master_width=1150, master_height=800,
                                               child_width=settings_card.getWidth(),
                                               child_height=settings_card.getHeight())
                settings_card.place(x=center[0], y=center[1])
                settings_card.default_mode()
                self.set_default_mode()

    def logo_click(self):
        return self.__logo

    def settings_click(self):
        return self.__settings_button

    def add_card_click(self):
        return self.__add_card_button

    def __load_previous_page(self):
        if self.__page_index == 16:
            self.__back_button.configure(state=DISABLED)
        else:
            if self.__next_button.cget('state') == DISABLED:
                self.__next_button.configure(state=ACTIVE)

            with open('serialfiles/SuperFile.json', 'r') as superfile:
                existing_data = json.load(superfile)

            for child in self.__internal_frame.winfo_children():
                child.destroy()
            GridSystem.x_coord = 0
            GridSystem.y_coord = 0
            self.__page_index -= 16
            self.__card_index = self.__page_index - 16
            i = self.__card_index
            while i < self.__page_index:
                GridSystem.add_to_grid(self.__internal_frame, card_name=str(existing_data[i]["collection_name"]),
                                       card_color=str(existing_data[i]["collection_color"]),
                                       num_cards=int(existing_data[i]["collection_card_count"]), super_root=self)
                i += 1
                self.__card_index += 1

    def __load_next_page(self):
        with open('serialfiles/SuperFile.json', 'r') as superfile:
            existing_data = json.load(superfile)

        if self.__card_index == len(existing_data):
            self.__next_button.configure(state=DISABLED)
        else:
            if self.__back_button.cget('state') == DISABLED:
                self.__back_button.configure(state=ACTIVE)
            for child in self.__internal_frame.winfo_children():
                child.destroy()
            GridSystem.x_coord = 0
            GridSystem.y_coord = 0
            i = self.__card_index
            self.__page_index += 16
            while i < self.__page_index:
                if i < len(existing_data):
                    GridSystem.add_to_grid(self.__internal_frame, card_name=str(existing_data[i]["collection_name"]),
                                           card_color=str(existing_data[i]["collection_color"]),
                                           num_cards=int(existing_data[i]["collection_card_count"]), super_root=self)
                    self.__card_index += 1
                else:
                    break
                i += 1

    def super_reload(self):
        with open('serialfiles/SuperFile.json', 'r') as file:
            existing_data = json.load(file)

        if len(existing_data) > 16:
            for i in range(0, 16):
                GridSystem.add_to_grid(self.__internal_frame, card_name=str(existing_data[i]["collection_name"]),
                                       card_color=str(existing_data[i]["collection_color"]),
                                       num_cards=int(existing_data[i]["collection_card_count"]), super_root=self)
                self.__card_index += 1

            self.__page_index += 16

            self.__back_image = CTkImage(light_image=Image.open('assets/Back.png'), size=(13, 14))
            self.__next_image = CTkImage(light_image=Image.open('assets/Next.png'), size=(13, 14))
            if self.Darkmode is False:
                self.__back_button = CTkButton(self, image=self.__back_image, width=13, height=14, hover=FALSE,
                                               fg_color=WHITE, bg_color=WHITE, text='')
                self.__back_button.place(x=542, y=770)
                self.__back_button.configure(command=self.__load_previous_page)

                self.__next_button = CTkButton(self, image=self.__next_image, width=13, height=14, hover=FALSE,
                                               fg_color=WHITE, bg_color=WHITE, text='')
                self.__next_button.configure(command=self.__load_next_page)
                self.__next_button.place(x=592, y=770)
            else:
                self.__back_button = CTkButton(self, image=self.__back_image, width=13, height=14, hover=FALSE,
                                               fg_color=DARK_MODE_BACKGOUND, bg_color=DARK_MODE_BACKGOUND, text='')
                self.__back_button.place(x=542, y=770)
                self.__back_button.configure(command=self.__load_previous_page)

                self.__next_button = CTkButton(self, image=self.__next_image, width=13, height=14, hover=FALSE,
                                               fg_color=DARK_MODE_BACKGOUND, bg_color=DARK_MODE_BACKGOUND, text='')
                self.__next_button.configure(command=self.__load_next_page)
                self.__next_button.place(x=592, y=770)

        else:
            for data in existing_data:
                GridSystem.add_to_grid(self.__internal_frame, card_name=str(data["collection_name"]),
                                       card_color=str(data["collection_color"]),
                                       num_cards=int(data["collection_card_count"]), super_root=self)

    def reload(self):
        with open('serialfiles/SuperFile.json', 'r') as file:
            existing_data = json.load(file)
        GridSystem.add_to_grid(self.__internal_frame, card_name=str(existing_data[-1]["collection_name"]),
                               card_color=str(existing_data[-1]["collection_color"]),
                               num_cards=int(existing_data[-1]["collection_card_count"]), super_root=self)

    def clean(self):
        for child in self.__internal_frame.winfo_children():
            child.destroy()

    def clean_then_reload(self):
        for child in self.__internal_frame.winfo_children():
            child.destroy()
        GridSystem.x_coord = 0
        GridSystem.y_coord = 0
        self.super_reload()

    def set_dark_mode(self):
        self.Darkmode = True
        self.config(bg=DARK_MODE_BACKGOUND)
        self.__internal_frame.configure(fg_color=DARK_MODE_BACKGOUND)
        self.__Exterior_Frame.configure(fg_color=DARK_MODE_BACKGOUND, bg_color=DARK_MODE_BACKGOUND)
        self.__logo.configure(fg_color=DARK_MODE_BACKGOUND, bg_color=DARK_MODE_BACKGOUND, text_color=WHITE)
        self.__add_card_button.configure(bg_color=DARK_MODE_BACKGOUND, fg_color=DARK_MODE_BACKGOUND)
        self.__add_card_button.configure(image=CTkImage(light_image=Image.open('assets/ADD_CARD_BUTTON_WHITE.png'),
                                                        size=(30, 30)))
        self.__settings_button.configure(bg_color=DARK_MODE_BACKGOUND, fg_color=DARK_MODE_BACKGOUND)
        self.__settings_button.configure(image=CTkImage(light_image=Image.open('assets/SETTINGS_WHITE.png'),
                                                        size=(30, 30)))

    def set_default_mode(self):
        self.Darkmode = False
        self.config(bg=WHITE)
        self.__internal_frame.configure(fg_color=WHITE)
        self.__Exterior_Frame.configure(fg_color=WHITE, bg_color=WHITE)
        self.__logo.configure(fg_color=WHITE, bg_color=WHITE, text_color=BLACK)
        self.__add_card_button.configure(bg_color=WHITE, fg_color=WHITE)
        self.__add_card_button.configure(image=CTkImage(light_image=Image.open('assets/ADD_CARD_BUTTON.png'),
                                                        size=(30, 30)))
        self.__settings_button.configure(bg_color=WHITE, fg_color=WHITE)
        self.__settings_button.configure(image=CTkImage(light_image=Image.open('assets/SETTINGS.png'),
                                                        size=(30, 30)))

    def __on_close(self):

        with open("serialfiles/settings.json") as fp:
            parameters = json.load(fp)

        parameters["dark"] = self.Darkmode

        with open("serialfiles/settings.json", 'w') as fp:
            json.dump(parameters, fp)

        self.destroy()


# KARTA = MainWindow()
# KARTA.mainloop()

