
from customtkinter import *
from tkinter import IntVar, END
from PIL import Image, ImageColor
from Parameters import *


class ColorPicker(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_iconbitmap("assets/icons/COLORPICKERICON.ico")
        self.title("Color Picker")
        self.geometry("400x320")
        self.resizable(FALSE, FALSE)
        self.iconbitmap('assets/icons/KARTA_ICON.ico')
        self.Red = IntVar()
        self.Green = IntVar()
        self.Blue = IntVar()
        self.HexCode = IntVar()
        self.color_picker_background = CTkImage(light_image=Image.open('assets/COLOR_PICKER_BACKGROUND.png'),
                                           size=(400, 320))
        self.frame = CTkLabel(self, image=self.color_picker_background, corner_radius=20, bg_color=WHITE, fg_color=WHITE
                              , text='')
        self.frame.pack()

        self.color_canvas = CTkLabel(self, width=360, height=100, corner_radius=10, fg_color=FRESH_MINT, text='',
                                     bg_color=WHITE)
        self.color_canvas.place(x=15, y=15)
        self.color_canvas.bind("<Double-1>", lambda e: self.CopyColor())
        ################################## SLIDERS ########################################

        self.red_color_slider = CTkSlider(self, width=300, height=10, border_width=0, from_=0, to=255, button_color=RED,
                                     hover=FALSE, progress_color=GRAY_DE, corner_radius=0, fg_color=GRAY_DE
                                     , border_color=WHITE, bg_color=WHITE, button_length=15, command=self.ColorSlider)
        self.red_color_slider.place(x=15, y=140)

        self.green_color_slider = CTkSlider(self, width=300, height=10, border_width=0, from_=0, to=255,
                                            button_color=GREEN, hover=FALSE, progress_color=GRAY_DE, corner_radius=0,
                                            fg_color=GRAY_DE, border_color=WHITE, bg_color=WHITE, button_length=15
                                            , command=self.ColorSlider)
        self.green_color_slider.place(x=15, y=170)


        self.blue_color_slider = CTkSlider(self, width=300, height=10, border_width=0, from_=0, to=255, button_color=BLUE,
                                       hover=FALSE, progress_color=GRAY_DE, corner_radius=0, fg_color=GRAY_DE
                                       , border_color=WHITE, bg_color=WHITE, button_length=15, command=self.ColorSlider)
        self.blue_color_slider.place(x=15, y=200)

        ################################ TEXT BOXES #####################################

        self.red_color_text_box = CTkEntry(self, width=55, height=25, corner_radius=10, text_color=BLACK, border_width=0,
                                        font=JosefinSans_20_BOLD, bg_color=WHITE, fg_color=GRAY_DE)
        self.red_color_text_box.place(x=37, y=240)

        self.green_color_text_box = CTkEntry(self, width=55, height=25, corner_radius=10, text_color=BLACK, border_width=0,
                                      font=JosefinSans_20_BOLD, bg_color=WHITE, fg_color=GRAY_DE)
        self.green_color_text_box.place(x=107, y=240)

        self.blue_color_text_box = CTkEntry(self, width=55, height=25, corner_radius=10, text_color=BLACK, border_width=0,
                                        font=JosefinSans_20_BOLD, bg_color=WHITE, fg_color=GRAY_DE)
        self.blue_color_text_box.place(x=177, y=240)

        self.hex_code_text_box = CTkEntry(self, width=120, height=25, corner_radius=10, text_color=BLACK, border_width=0,
                                        font=JosefinSans_20_BOLD, bg_color=WHITE, fg_color=GRAY_DE)
        self.hex_code_text_box.place(x=247, y=240)
        self.hex_code_text_box.bind("<Return>", lambda e: self.setRGB())

    def ColorSlider(self, *args):
        self.Red = int(self.red_color_slider.get())
        self.Green = int(self.green_color_slider.get())
        self.Blue = int(self.blue_color_slider.get())

        self.HexCode = "#%02X%02X%02X" % (self.Red, self.Green, self.Blue)
        self.color_canvas.configure(fg_color=self.HexCode)

        self.hex_code_text_box.delete(0, END)
        self.hex_code_text_box.insert(0, self.HexCode)

        self.red_color_text_box.delete(0, END)
        self.red_color_text_box.insert(0, self.Red)

        self.green_color_text_box.delete(0, END)
        self.green_color_text_box.insert(0, self.Green)

        self.blue_color_text_box.delete(0, END)
        self.blue_color_text_box.insert(0, self.Blue)

    def getColor(self):
        return self.HexCode

    def CopyColor(self):
        super().clipboard_clear()
        super().clipboard_append(str(self.HexCode))

    def setRGB(self):
        color_string = self.hex_code_text_box.get()

        if str(color_string)[0] == '#':
            rgb = ImageColor.getrgb(str(color_string))
        else:
            rgb = ImageColor.getrgb('#' + str(color_string))

        self.red_color_slider.set(int(rgb[0]))
        self.green_color_slider.set(int(rgb[1]))
        self.blue_color_slider.set(int(rgb[2]))

        self.Red = int(self.red_color_slider.get())
        self.Green = int(self.green_color_slider.get())
        self.Blue = int(self.blue_color_slider.get())

        self.HexCode = "#%02X%02X%02X" % (self.Red, self.Green, self.Blue)
        self.color_canvas.configure(fg_color=self.HexCode)

        self.hex_code_text_box.delete(0, END)
        self.hex_code_text_box.insert(0, self.HexCode)

        self.red_color_text_box.delete(0, END)
        self.red_color_text_box.insert(0, self.Red)

        self.green_color_text_box.delete(0, END)
        self.green_color_text_box.insert(0, self.Green)

        self.blue_color_text_box.delete(0, END)
        self.blue_color_text_box.insert(0, self.Blue)



