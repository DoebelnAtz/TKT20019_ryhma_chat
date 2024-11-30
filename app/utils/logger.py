from flask import current_app


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

    def log(self, message):
        print(f"{Color.bold}{self.name}{Color.reset} | {
              Color.cyan}LOG{Color.reset}: {message}")

    def debug(self, message):
        if current_app.config['DEBUG']:
            print(f"{Color.bold}{self.name}{Color.reset} | {
                  Color.green}DEBUG{Color.reset}: {message}")

    def error(self, message):
        print(f"{Color.bold}{self.name}{Color.reset} | {
              Color.red}ERROR{Color.reset}: {message}")
