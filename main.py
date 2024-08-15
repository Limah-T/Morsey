import os
# Environments variables to enable me to control kivy behaviour
os.environ['KIVY_TEXT'] = 'pil'
os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from morse_code import morsecodes


class MorseCodeConverter(GridLayout):
    def __init__(self, **kwargs):
        super(MorseCodeConverter, self).__init__(**kwargs)
        self.padding = [50, 30, 50, 30]
        self.spacing = 30
        self.cols = 1
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        input_layout = GridLayout(cols=1, size_hint_y=None, height=220)
        input_label = Label(text='Input', font_size=20, halign='left', valign='middle', size_hint_y=None, height=40)
        input_label.bind(size=input_label.setter('text_size'))
        input_layout.add_widget(input_label)
        self.input = TextInput(multiline=True, font_family='Sans Serif', font_size=25, padding=(30, 20),
                               height=180, hint_text='Type your text here', halign='left', size_hint_y=None)
        self.input.bind(text=self.on_text_change)
        input_layout.add_widget(self.input)
        self.add_widget(input_layout)
        output_layout = GridLayout(cols=1, size_hint_y=None, height=220)
        output_label = Label(text='Output', font_size=20, halign='left', valign='middle', size_hint_y=None, height=40)
        output_label.bind(size=output_label.setter('text_size'))
        output_layout.add_widget(output_label)
        self.output = TextInput(multiline=True, font_family='Sans Serif', font_size=25, padding=(30, 20),
                                hint_text="Morse code will appear here", height=180, size_hint_y=None)
        output_layout.add_widget(self.output)
        self.add_widget(output_layout)

        content = Label(text='Morse Code Hint:'
                             'Morse code is a method of encoding text characters as sequences of dots (.) '
                             'and dashes (-). Each letter, number, or punctuation mark is represented by'
                             ' a unique combination of these symbols. For example, “A” is represented as '
                             '“.-”, “B” as “-…”, and “C” as “-.-.”. Spaces between sequences indicate the '
                             'separation between letters or words.'
                             'Just type letters, numbers and symbols into the top box'
                             'and the Morse code will appear in the bottom box(Output), if the character'
                             'cannot be translated, it\'ll show "Invalid Input" in the bottom box.'
                             'Morse to Text You can type Morse code into the top box using "." for a dot and'
                             '"-" or "_" for a dash. Letters are separated by spaces and words by "/".'
                             , text_size=(self.width, None), halign='center', valign='center',
                             size_hint_y=None, height=300, line_height=1, font_family='Sans Serif',
                             font_size=20)
        self.add_widget(content)
        Window.bind(on_resize=self.update_padding)

        content.bind(size=lambda l, s: l.setter('text_size')(l, (s[0], None)))
        self.bind(size=self._update_rect, pos=self._update_rect)

        with self.canvas.before:
            Color(0.33, 0.38, 0.75, 0.3)  # Adjust color to be within 0-1 range
            self.rect = Rectangle(size=self.size,
                                  pos=self.pos)
    def update_padding(self, *args):
        # Update padding based on the window width
        self.padding = [Window.width * 0.05, Window.height * 0.05]  # 5% of window width and height

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_text_change(self, instance, value):
        user_text = value.upper()
        print(user_text)
        # text_to_morsecode = [morsecodes[a] if a in morsecodes else self.display_invalid_input.text for a in user_text]
        code = ""
        invalid_symbol = []
        for txt in user_text:
            if txt in morsecodes:
                code += morsecodes[txt]
                self.output.text = code
            else:
                invalid_symbol.append(txt)
                symbols = ""
                for n in invalid_symbol:
                    symbols += n
                    self.output.text = f"Invalid input ({symbols})"
        print(code)


class MyApp(App):
    def build(self):
        self.title = "Morsey"
        Window.size = (414, 896)
        print(Window.size)
        # Create the main layout
        main_layout = BoxLayout(orientation='vertical')

        # Create a top section (fixed content)
        fixed_layout = BoxLayout(size_hint_y=None, height=50)  # Adjust height as needed
        input_label = Label(text='Text to Morse Code', font_size=20, halign='center', valign='middle')
        fixed_layout.add_widget(input_label)

        # Create the scrollable section
        scroll_layout = ScrollView()
        scroll_content = MorseCodeConverter()
        scroll_layout.add_widget(scroll_content)

        # Add both layouts to the main layout
        main_layout.add_widget(fixed_layout)
        main_layout.add_widget(scroll_layout)

        return main_layout


if __name__ == "__main__":
    MyApp().run()
