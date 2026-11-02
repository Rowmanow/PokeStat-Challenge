# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from pokestat.screens import HomeScreen, GuesserScreen, DraftScreen

class PokeStatApp(App):
    language = "fr"
    def build(self):
        self.title = "PokeStat Challenge"
        Window.clearcolor = (0.059, 0.09, 0.165, 1)
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(GuesserScreen(name="guesser"))
        sm.add_widget(DraftScreen(name="draft"))
        return sm
    def set_language(self, language):
        self.language = language
        for screen in self.root.screens:
            if hasattr(screen, "refresh_texts"):
                screen.refresh_texts()

if __name__ == "__main__":
    PokeStatApp().run()
