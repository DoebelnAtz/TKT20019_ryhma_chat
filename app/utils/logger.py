import os


class Color:
    red = "\033[1;31m"
    blue = "\033[1;34m"
    cyan = "\033[1;36m"
    green = "\033[0;32m"
    reset = "\033[0;0m"
    bold = "\033[;1m"


class Logger:
    def __init__(self, name):
        self.name = name

    def log(self, *args):
        print(f"{Color.cyan}LOG{Color.reset} | {Color.bold}{
              self.name}{Color.reset}", *args)

    def debug(self, *args):
        if os.environ.get('FLASK_ENV') == 'development':
            print(f"{Color.green}DEBUG{Color.reset} | {Color.bold}{
                  self.name}{Color.reset}:", *args)

    def error(self, *args):
        print(f"{Color.red}ERROR{Color.reset} | {Color.bold}{
              self.name}{Color.reset}:", *args)
