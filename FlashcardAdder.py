import json
from customtkinter import *
from tkinter import Label
from PIL import Image
from Parameters import *
from ColorPicker import ColorPicker
import CustomWidgets as CW
import FileManager as FM

class FlashCardAdder(CTkFrame):
    def __init__(self, root, *args, color=LIGHT_GRAY, command=None, **kwargs):
        super().__init__(*args, width=599, height=372, corner_radius=20, fg_color=color, **kwargs
                         , bg_color=WHITE)

        self.MAX_COLOR_PICKER = 1
        self.__root_frame = root
        self.ColorClicked = [False, False, False, False, False, False, False]
        self.custom_color = LIGHT_PINK
        ############# FLASHCARD NAME #################
        self.flash_card_name_label = Label(self, text="FLASHCARD'S NAME:", fg=BLACK, bg=LIGHT_GRAY,
                                           font=JosefinSans_20_BOLD)
        self.flash_card_name_label.place(x=78, y=30)
        ############## NAME INPUT FIELD #################
        self.flash_card_name_input = CTkTextbox(self, text_color=WHITE, fg_color=GRAY_B1, border_width=0
                                           , bg_color=LIGHT_GRAY, font=JosefinSans_20_BOLD, height=10, width=515
                                           , corner_radius=20, activate_scrollbars=FALSE)
        self.flash_card_name_input.place(x=43, y=57)
        ############### FLASH CARD COLOR ##############
        self.flash_card_color_label = Label(self, text="FLASHCARD'S COLOR:", fg=BLACK,
                                       bg=LIGHT_GRAY, font=JosefinSans_20_BOLD)
        self.flash_card_color_label.place(x=78, y=210)
        ################# RECOMMENDED COLOR 1 - MUSTARD YELLOW ##################
        self.m_yellow_color = CTkImage(light_image=Image.open('assets/YELLOW_UNSELECTED.png'), size=(75, 35))
        self.m_yellow_color_button = CTkButton(self, width=75, height=35, image=self.m_yellow_color, text='',
                                          fg_color=LIGHT_GRAY, border_width=0, hover=FALSE,
                                          bg_color=LIGHT_GRAY, command=self.m_yellow_selected)
        self.m_yellow_color_button.place(x=38, y=175)
        ################# RECOMMENDED COLOR 2 - MINT #########################
        self.mint_color = CTkImage(light_image=Image.open('assets/MINT_UNSELECTED.png'), size=(75, 35))
        self.mint_color_button = CTkButton(self, width=75, height=35, image=self.mint_color, text='',
                                      fg_color=LIGHT_GRAY, border_width=0, hover=FALSE, bg_color=LIGHT_GRAY
                                        , command=self.fresh_mint_selected)
        self.mint_color_button.place(x=123, y=175)
        ########################## RECOMMENDED COLOR 3 - DARK MINT #########################
        self.dark_mint_color = CTkImage(light_image=Image.open('assets/DARK_MINT_UNSELECTED.png'), size=(75, 35))
        self.dark_mint_color_button = CTkButton(self, width=75, height=35, image=self.dark_mint_color,
                                                text='', fg_color=LIGHT_GRAY, border_width=0, hover=FALSE,
                                                bg_color=LIGHT_GRAY, command=self.dark_mint_selected)
        self.dark_mint_color_button.place(x=208, y=175)
        ########################## RECOMMENDED COLOR 4 - KHAKI ###########################
        self.khaki_color = CTkImage(light_image=Image.open('assets/KHAKI_UNSELECTED.png'), size=(75, 35))
        self.khaki_color_button = CTkButton(self, width=75, height=35, image=self.khaki_color, text='',
                                       fg_color=LIGHT_GRAY, border_width=0, hover=FALSE, bg_color=LIGHT_GRAY,
                                            command=self.khaki_selected)
        self.khaki_color_button.place(x=293, y=175)
        ########################## RECOMMENDED COLOR 5 - DARK BLUE #######################
        self.dark_blue_color = CTkImage(light_image=Image.open('assets/DARK_BLUE_UNSELECTED.png'), size=(75, 35))
        self.dark_blue_color_button = CTkButton(self, width=75, height=35, image=self.dark_blue_color,
                                                text='', fg_color=LIGHT_GRAY, border_width=0, hover=FALSE,
                                                bg_color=LIGHT_GRAY, command=self.dark_blue_selected)
        self.dark_blue_color_button.place(x=378, y=175)
        ########################## RECOMMENDED COLOR 6 - LIGHT PINK ######################
        self.light_pink_color = CTkImage(light_image=Image.open('assets/LIGHT_PINK_UNSELECTED.png'), size=(75, 35))
        self.light_pink_color_button = CTkButton(self, width=75, height=35, image=self.light_pink_color,
                                                 text='', fg_color=LIGHT_GRAY, border_width=0, hover=FALSE,
                                                 bg_color=LIGHT_GRAY, command=self.light_pink_selected)
        # light_pink_color_button.bind("<Button-1>", lambda e: light_pink_selected(light_pink_color_button))
        self.light_pink_color_button.place(x=463, y=175)
        ########################## CUSTOM COLOR PICKER ############################
        self.color_picker_button = CTkButton(self, width=110, height=35, text='CUSTOM', text_color=WHITE,
                                        corner_radius=20, fg_color=GRAY_B1, font=JosefinSans_20_BOLD
                                        , bg_color=LIGHT_GRAY, command=self.custom_color_selected, hover_color=BLACK)
        self.color_picker_button.place(x=45, y=225)

        self.custom_color_frame = None
        ########################## CREATE BUTTON #########################
        self.create_card_button = CTkButton(self, width=155, height=40, corner_radius=20, text_color=WHITE,
                                       text="CREATE"
                                       , fg_color=GRAY_B1, font=JosefinSans_20_BOLD, bg_color=LIGHT_GRAY
                                       , command=self.createHomeCard, hover_color=BLACK)
        self.create_card_button.place(x=113, y=300)
        ########################## CANCEL BUTTON #########################
        self.cancel_card_button = CTkButton(self, width=155, height=40, corner_radius=20, text_color=WHITE,
                                       text="CANCEL"
                                       , fg_color=GRAY_B1, font=JosefinSans_20_BOLD, bg_color=LIGHT_GRAY
                                       , command=self.cancel, hover_color=BLACK)
        self.cancel_card_button.place(x=308, y=300)

    def colorPicker(self):
        self.custom_color_frame = ColorPicker(self.__root_frame)
        self.custom_color_frame.protocol("WM_DELETE_WINDOW", self.GetColorThenDestroy)

    def cancel(self):
        self.__root_frame.MAX_FLASHCARD_ADDER = 1
        self.destroy()

    def dark_mode(self):
        self.configure(fg_color=SETTINGS_DARK, bg_color=DARK_MODE_BACKGOUND)
        self.flash_card_name_label.configure(fg=WHITE, bg=SETTINGS_DARK)
        self.flash_card_color_label.configure(fg=WHITE, bg=SETTINGS_DARK)
        self.m_yellow_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.mint_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.dark_blue_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.dark_mint_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.khaki_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.light_pink_color_button.configure(fg_color=SETTINGS_DARK, bg_color=SETTINGS_DARK)
        self.color_picker_button.configure(bg_color=SETTINGS_DARK)
        self.create_card_button.configure(bg_color=SETTINGS_DARK)
        self.cancel_card_button.configure(bg_color=SETTINGS_DARK)

    def m_yellow_selected(self):
        if self.ColorClicked[0] is True:
            self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.ColorClicked[0] = False
        else:
            self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/M_YELLOW_SELECTED.png'),
                                                                size=(75, 35)))
            for i in range(0, len(self.ColorClicked)):
                if i == 0:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 1:
                        self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 2:
                        self.dark_mint_color_button.configure(image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.dark_blue_color_button.configure(image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.color_picker_button.configure(fg_color=GRAY_B1)

    def fresh_mint_selected(self):
        if self.ColorClicked[1] is True:
            self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.ColorClicked[1] = False
        else:
            self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_SELECTED.png'),
                                                                size=(75, 35)))
            for i in range(0, len(self.ColorClicked)):
                if i == 1:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 0:
                        self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.dark_mint_color_button.configure(image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.dark_blue_color_button.configure(image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.color_picker_button.configure(fg_color=GRAY_B1)

    def dark_mint_selected(self):
        if self.ColorClicked[2] is True:
            self.dark_mint_color_button.configure(image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.ColorClicked[2] = False
        else:
            self.dark_mint_color_button.configure(image=CTkImage(Image.open('assets/DARK_MINT_SELECTED.png'),
                                                                size=(75, 35)))
            for i in range(0, len(self.ColorClicked)):
                if i == 2:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 0:
                        self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 3:
                        self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.dark_blue_color_button.configure(image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.color_picker_button.configure(fg_color=GRAY_B1)

    def khaki_selected(self):
        if self.ColorClicked[3] is True:
            self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'), size=(75, 35)))
            self.ColorClicked[3] = False
        else:
            self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_SELECTED.png'),
                                                             size=(75, 35)))
            for i in range(0, len(self.ColorClicked)):
                if i == 3:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 0:
                        self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.dark_mint_color_button.configure(image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 4:
                        self.dark_blue_color_button.configure(image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 5:
                        self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.color_picker_button.configure(fg_color=GRAY_B1)

    def dark_blue_selected(self):
        if self.ColorClicked[4] is True:
            self.dark_blue_color_button.configure(image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.ColorClicked[4] = False
        else:
            self.dark_blue_color_button.configure(image=CTkImage(Image.open('assets/DARK_BLUE_SELECTED.png'),
                                                             size=(75, 35)))
            for i in range(0, len(self.ColorClicked)):
                if i == 4:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 0:
                        self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.dark_mint_color_button.configure(image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                         size=(75, 35)))
                    elif i == 5:
                        self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 6:
                        self.color_picker_button.configure(fg_color=GRAY_B1)

    def light_pink_selected(self):
        if self.ColorClicked[5] is True:
            self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                                                size=(75, 35)))
            self.ColorClicked[5] = False
        else:
            self.light_pink_color_button.configure(image=CTkImage(Image.open('assets/LIGHT_PINK_SELECTED.png'),
                                                             size=(75, 35)))
            for i in range(0, len(self.ColorClicked)):
                if i == 5:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 0:
                        self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.dark_mint_color_button.configure(
                            image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                         size=(75, 35)))
                    elif i == 4:
                        self.dark_blue_color_button.configure(
                            image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                           size=(75, 35)))
                    elif i == 6:
                        self.color_picker_button.configure(fg_color=GRAY_B1)

    def custom_color_selected(self):
        if self.ColorClicked[6] is True:
            if str(self.custom_color_frame.getColor())[0] == "#":
                self.custom_color = str(self.custom_color_frame.getColor())
            else:
                self.custom_color = DEFAULT_CARD_COLOR
            self.custom_color_frame.destroy()
            self.color_picker_button.configure(fg_color=self.custom_color)
            #self.ColorClicked[6] = False
        else:
            self.MAX_COLOR_PICKER = 1
            self.color_picker_button.configure(fg_color=BLACK)
            for i in range(0, len(self.ColorClicked)):
                if i == 6:
                    self.ColorClicked[i] = True
                else:
                    self.ColorClicked[i] = False
                    if i == 0:
                        self.m_yellow_color_button.configure(image=CTkImage(Image.open('assets/YELLOW_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 1:
                        self.mint_color_button.configure(image=CTkImage(Image.open('assets/MINT_UNSELECTED.png'),
                                                                            size=(75, 35)))
                    elif i == 2:
                        self.dark_mint_color_button.configure(
                            image=CTkImage(Image.open('assets/DARK_MINT_UNSELECTED.png'),
                                                                        size=(75, 35)))
                    elif i == 3:
                        self.khaki_color_button.configure(image=CTkImage(Image.open('assets/KHAKI_UNSELECTED.png'),
                                                                         size=(75, 35)))
                    elif i == 4:
                        self.dark_blue_color_button.configure(
                            image=CTkImage(Image.open('assets/DARK_BLUE_UNSELECTED.png'),
                                           size=(75, 35)))
                    elif i == 5:
                        self.light_pink_color_button.configure(
                            image=CTkImage(Image.open('assets/LIGHT_PINK_UNSELECTED.png'),
                                           size=(75, 35)))

        if self.MAX_COLOR_PICKER < 2:
            self.colorPicker()
            self.MAX_COLOR_PICKER += 1

    def GetColorThenDestroy(self):
        if str(self.custom_color_frame.getColor())[0] == "#":
            self.custom_color = str(self.custom_color_frame.getColor())
        else:
            self.custom_color = DEFAULT_CARD_COLOR
        self.color_picker_button.configure(fg_color=self.custom_color)
        self.ColorClicked[6] = False
        self.custom_color_frame.destroy()
        self.custom_color_frame = None

    def createHomeCard(self):
        card__name__ = str(self.flash_card_name_input.get(index1='1.0', index2='1.end'))
        with open('serialfiles/SuperFile.json', 'r') as file:
            cards = json.load(file)
        for i in range(len(cards)):
            if cards[i]['collection_name'].upper() == card__name__.upper():
                split_name = card__name__.split()
                if split_name[-1].isnumeric():
                    split_name[-1] = str(int(split_name[-1]) + 1)
                    card__name__ = ' '.join(split_name)
                else:
                    card__name__ = card__name__ + ' 1'
                break

        card__color__ = self.custom_color
        if self.ColorClicked[0] is True:
            card__color__ = MUSTARD_YELLOW
        elif self.ColorClicked[1] is True:
            card__color__ = FRESH_MINT
        elif self.ColorClicked[2] is True:
            card__color__ = DARK_MINT
        elif self.ColorClicked[3] is True:
            card__color__ = KHAKI
        elif self.ColorClicked[4] is True:
            card__color__ = DARK_BLUE
        elif self.ColorClicked[5] is True:
            card__color__ = LIGHT_PINK
        elif self.ColorClicked[6] is True:
            card__color__ = self.custom_color
        FM.FlashCard_Created(flashcard_name=card__name__, flashcard_color=card__color__)
        CW.QuestionAnswer(master=self.__root_frame, root=self.__root_frame, card_name=card__name__)
        if self.custom_color_frame is not None:
            self.custom_color_frame.destroy()
        self.__root_frame.MAX_FLASHCARD_ADDER = 1
        self.destroy()

    @staticmethod
    def getWidth():
        return 599

    @staticmethod
    def getHeight():
        return 372

    def clear(self):
        self.mint_color_button.destroy()
        self.flash_card_color_label.destroy()
        self.create_card_button.destroy()
        self.cancel_card_button.destroy()
        self.flash_card_name_input.destroy()
        self.custom_color_frame.destroy()
        self.dark_mint_color_button.destroy()
        self.khaki_color_button.destroy()
        self.color_picker_button.destroy()
        self.dark_blue_color_button.destroy()
        self.light_pink_color_button.destroy()
        self.m_yellow_color_button.destroy()
        self.flash_card_color_label.destroy()
        self.destroy()

