import os
import time
import getpass
import json
from ..config import *
from ..chat import *
from ..conversations import *
from ..encryption import *
from ..printer import *
from ..main import *


def install_api_key():
    """Install the terminalgpt openai api key and create app directories."""

    printer: Printer = PrinterFactory.get_printer(style="plain")
    enc_manager: EncryptionManager = EncryptionManager()

    printer.printt(PrintUtils.INSTALL_WELCOME_MESSAGE)

    printer: Printer = PrinterFactory.get_printer(style="plain")
    enc_manager: EncryptionManager = EncryptionManager()

    printer.printt(PrintUtils.INSTALL_WELCOME_MESSAGE)

    while True:
        api_key = getpass.getpass(
            prompt=f"{Style.RESET_ALL}{Style.BRIGHT}Please enter your OpenAI API key:\n{Style.RESET_ALL}"
        )

        printer.printt(f"{Style.BRIGHT}{Fore.GREEN}Great!{Style.RESET_ALL}\n")
        time.sleep(0.5)

        models = list(config.MODELS.keys())
        printer.printt(
            f"{Style.BRIGHT}Please choose one of the models below to be your default model:"
        )

        for model, token_limit in config.MODELS.items():
            printer.printt(
                f"{Style.BRIGHT} - Model: {Style.RESET_ALL}{model}"
                f"{Style.BRIGHT}    tokens-limit: {Style.RESET_ALL}{int(int(token_limit)/1000)}k"
            )

        model = prompt(
            "\nType the desired model:\n",
            completer=WordCompleter(models, ignore_case=True),
            style=PromptStyle.from_dict({"prompt": "bold lightblue"}),
            default=models[0],
        )

        printing_styles = ["markdown", "plain"]
        printer.printt(
            f"{Style.BRIGHT}Please choose one of the printing styles below to be your default printing style:"
        )
        for style in printing_styles:
            printer.printt(f"{Style.BRIGHT} - Style: {Style.RESET_ALL}{style}")

        printing_style = prompt(
            "\n Choose a printing style ('markdown' is recommended):\n",
            completer=WordCompleter(printing_styles, ignore_case=True),
            style=PromptStyle.from_dict({"prompt": "bold lightblue"}),
            default=printing_styles[0],
        )

        if model in models and printing_style in printing_styles:
            printer.printt(f"\n{Style.BRIGHT}{Fore.GREEN}Great!{Style.RESET_ALL}\n")
            break
        else:
            invalid_input = ""
            if model not in models:
                invalid_input += "Invalid model! Please choose from the provided list.\n"
            if printing_style not in printing_styles:
                invalid_input += "Invalid printing style! Please choose from the provided list.\n"

            printer.printt(f"\n{Style.BRIGHT}{Fore.RED}{invalid_input}{Style.RESET_ALL}\n")
            continue

    encryption_key = enc_manager.set_encryption_key()
    encrypted_secret = enc_manager.encrypt(api_key.encode(), encryption_key)

    if not os.path.exists(os.path.dirname(config.SECRET_PATH)):
        os.makedirs(os.path.dirname(config.SECRET_PATH))

    if not os.path.exists(config.CONVERSATIONS_PATH):
        os.mkdir(config.CONVERSATIONS_PATH)

    # Save the encrypted secret to a file
    with open(config.SECRET_PATH, "wb") as file:
        file.write(encrypted_secret)

    # Save the default config to a file
    with open(config.DEFAULTS_PATH, "w", encoding="utf-8") as file:
        json.dump({"model": model, "style": printing_style}, file)

    printer.printt(PrintUtils.INSTALL_SUCCESS_MESSAGE)
    printer.printt(PrintUtils.INSTALL_ART)
    printer.printt(PrintUtils.INSTALL_SMALL_PRINTS)
