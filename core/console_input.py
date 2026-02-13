from threading import Thread
from config import LOG_TO_CONSOLE, API_PORT
from globals import Globals
from .logs import log, RESPONSE, INFO, CRITICAL
from dataclasses import dataclass
from typing import Callable, List
import urllib.request
from main_functions import check_all, start_all, close_all


@dataclass
class Command:
    ect: Callable[[List[str]], None]
    desc: str = ""
    args_min: int | None = None
    args_max: int | None = None


class ConsoleInput:
    def __init__(self):
        self.main_input_thread = Thread(target=self.main_input, daemon=True)
        self.running = True

        self.commands = {
            "s": Command(None, "stops/starts log output to console"),                                           # noqa:E501
            "help": Command(self.c_help, "prins all commands. help[command] returns rescription", None, 1),     # noqa:E501
            "shutdown": Command(self.c_shutdown, "shutdowns everything", None, 0),                              # noqa:E501
            "update_all": Command(self.c_update_all, "updates all services", None, 0),                          # noqa:E501
        }
        self.using_command = ""
        self.run_to_shutdown: Callable[[]] | None = None

    def _resp(self, message: str):
        fill = "\n"+" "*len(self.using_command)+"\\>"
        log(RESPONSE, f"{self.using_command}>>{message.replace("\n", fill)}")

    def start_thread(self) -> Thread:
        self.main_input_thread.start()
        return self.main_input_thread

    def main_input(self):
        try:
            while self.running:
                user_input = input()
                self.using_command = ""
                log(INFO, f"CONSOLE>{user_input}")
                if user_input == "s":
                    # stops/starts console logs.
                    # used to write commands because input gets broken by logs.
                    if not LOG_TO_CONSOLE:
                        self._resp("already off")
                        continue
                    Globals.stop_logging_to_console =\
                        not Globals.stop_logging_to_console
                    if Globals.stop_logging_to_console:
                        self._resp("logging to console (OFF)")
                    else:
                        self._resp("logging to console (ON)")
                    continue
                user_args = user_input.split(" ")
                user_command = user_args.pop(0).lower()
                if user_command not in self.commands:
                    self._resp(f"Command '{user_command}' not found-use HELP")
                    continue
                self.using_command = user_command
                command = self.commands[user_command]
                args_len = len(user_args)
                if command.args_max is not None:
                    if command.args_min is not None:
                        if command.args_max == command.args_min:
                            if args_len != command.args_max:
                                self._resp("Command requires "
                                           f"{command.args_max} inputs - "
                                           f"given {args_len}")
                                continue
                        elif args_len < command.args_min:
                            self._resp("Command requires at least "
                                       f"{command.args_min} inputs - "
                                       f"given {args_len}")
                            return
                    if args_len > command.args_max:
                        self._resp("Command requires at most "
                                   f"{command.args_min} inputs - "
                                   f"given {args_len}")
                        return
                elif (command.args_min is not None and
                      args_len < command.args_min):
                    self._resp(f"Command requires at least {command.args_min}"
                               f" inputs - given {args_len}")
                    return
                command.ect(*user_args)
        except Exception as Error:
            if self.running:
                log(CRITICAL, "ConsoleInput error!;\n"+str(Error))

    # COMMANDS
    def c_help(self, command: str = None):
        if command is not None:
            command = command.lower()
            if command not in self.commands:
                self._resp(f"Command '{command}' not found")
                return
            self._resp(f"{command} - '{self.commands[command].desc}'")
            return
        self._resp("commands;\n"+"\n".join(self.commands))

    def c_shutdown(self):
        Thread(target=self._c_shutdown, daemon=True).start()

    def _c_shutdown(self):
        with urllib.request.urlopen(
             urllib.request.Request(
                 f"http://127.0.0.1:{API_PORT}/api/shutdown",
                 method="POST"),
             timeout=5) as response:
            self._resp(response.read().decode())

    def c_update_all(self):
        close_all()
        check_all()
        start_all()
        self._resp("Updated all")
