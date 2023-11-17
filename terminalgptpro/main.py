"""Main module for the terminalgpt package."""

import getpass
import json
import os
import time

import click
from colorama import Fore, Style
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PromptStyle

from terminalgptpro import config
from terminalgptpro.chat import ChatManager
from terminalgptpro.conversations import ConversationManager
from terminalgptpro.encryption import EncryptionManager
from terminalgptpro.printer import Printer, PrinterFactory, PrintUtils

@click.group()
@click.version_option(prog_name="TerminalGPT-Pro", message="%(prog)s %(version)s")
@click.option(
    "--model",
    "-m",
    type=click.Choice(list(config.MODELS.keys())),
    default=config.get_default_config().get("model", "gpt-3.5-turbo"),
    show_default=True,
    help="Choose a model to use.",
)
# option to choose rich text output
@click.option(
    "--style",
    "-s",
    type=click.Choice(["markdown", "plain"]),
    default=config.get_default_config().get("style", "markdown"),
    show_default=True,
    help="Output style.",
)
@click.pass_context
def cli(ctx, model, style: str):
    """*~ TerminalGPT-Pro - Ваш персональный терминальный ассистент ~*"""

    token_limit = config.MODELS[model]
    safety_buffer = token_limit * 0.25

    ctx.ensure_object(dict)

    ctx.obj["STYLE"] = style
    ctx.obj["PRINTER"] = PrinterFactory.get_printer(style)
    ctx.obj["MODEL"] = model
    ctx.obj["ENC_MNGR"] = EncryptionManager()
    ctx.obj["CONV_MANAGER"] = ConversationManager(ctx.obj["PRINTER"])

    ctx.obj["SESSION"] = PromptSession(
        style=PromptStyle.from_dict({"prompt": "bold"}),
        message="\nUser: ",
    )

    ctx.obj["CHAT"] = ChatManager(
        conversations_manager=ctx.obj["CONV_MANAGER"],
        token_limit=int(token_limit - safety_buffer),
        session=ctx.obj["SESSION"],
        messages=[],
        model=ctx.obj["MODEL"],
        printer=ctx.obj["PRINTER"],
    )


@click.command(
    help="Creating a secret api key for the chatbot."
    + " You will be asked to enter your OpenAI API key."
)
def install():
    """Install the terminalgpt openai api key and create app directories."""

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


@cli.command(help="Start a new conversation.")
@click.pass_context
def new(ctx):
    """Start a new conversation."""

    enc_manager: EncryptionManager = ctx.obj["ENC_MNGR"]
    chat_manager: ChatManager = ctx.obj["CHAT"]
    printer: Printer = ctx.obj["PRINTER"]
    enc_manager.set_api_key()

    token_limit = int(config.MODELS[ctx.obj["MODEL"]] / 1000)
    printer.printt(
        f"{Style.RESET_ALL}{Style.BRIGHT}Model: {Style.RESET_ALL}{ctx.obj['MODEL']} "
        f"{Style.BRIGHT}Token Limit: {Style.RESET_ALL}{token_limit}k "
        f"{Style.RESET_ALL}{Style.BRIGHT}Style: {Style.RESET_ALL}{ctx.obj['STYLE']}"
    )

    messages = [config.INIT_SYSTEM_MESSAGE]
    chat_manager.welcome_message(messages + [config.INIT_WELCOME_MESSAGE])
    chat_manager.messages = messages
    chat_manager.chat_loop()


@cli.command(help="One shot question answer.")
# argument to ask a question
@click.argument(
    "question",
    type=str,
)
@click.pass_context
def one_shot(ctx, question):
    """One shot question answer."""

    chat_manager: ChatManager = ctx.obj["CHAT"]
    enc_manager: EncryptionManager = ctx.obj["ENC_MNGR"]
    printer: Printer = ctx.obj["PRINTER"]

    enc_manager.set_api_key()

    messages = [config.INIT_SYSTEM_MESSAGE]

    messages.append({"role": "user", "content": question})

    printer.printt("")
    answer = chat_manager.get_user_answer(messages=messages)
    message = answer["choices"][0]["message"]["content"]

    printer.print_assistant_message(message)


@cli.command(help="Choose a previous conversation to load.")
@click.pass_context
def load(ctx):
    """Load a previous conversation."""

    printer: Printer = PrinterFactory.get_printer("plain")
    chat_manager: ChatManager = ctx.obj["CHAT"]
    enc_manager: EncryptionManager = ctx.obj["ENC_MNGR"]
    conv_manager: ConversationManager = ctx.obj["CONV_MANAGER"]

    messages = []
    enc_manager.set_api_key()

    # get conversations list
    conversations = conv_manager.get_conversations()

    msg = (
        Style.BRIGHT
        + Fore.RED
        + "\n** There are no conversations to load! **"
        + Style.RESET_ALL
    )

    if conv_manager.is_conversations_empty(files=conversations, message=msg):
        return

    # setup file names auto-completion
    completer = WordCompleter(conversations, ignore_case=True)
    printer.printt(PrintUtils.CONVERSATIONS_INIT_MESSAGE)

    # print conversations list
    for conversation in conversations:
        printer.printt(Style.BRIGHT + "- " + conversation)

    # prompt user to choose a conversation and load it into messages
    conversation = prompt(
        "\nChoose a conversation:\n",
        completer=completer,
        style=PromptStyle.from_dict({"prompt": "bold lightblue"}),
    )

    # if conversation not found, return
    if conversation not in conversations:
        printer.printt(
            Style.BRIGHT
            + Fore.RED
            + "\n** Conversation not found! **"
            + Style.RESET_ALL
        )
        return

    # load conversation
    conv_manager.conversation_name = conversation
    while not messages:
        messages = conv_manager.load_conversation()

    messages.append(config.INIT_WELCOME_BACK_MESSAGE)
    chat_manager.messages = messages
    chat_manager.total_usage = chat_manager.num_tokens_from_messages()

    printer.printt(
        Style.BRIGHT
        + "\nConversation details and settings:"
        + Style.RESET_ALL
        + f"""
    Name: {conversation}
    Model: {ctx.obj["MODEL"]}
    Token Limit: {config.MODELS[ctx.obj["MODEL"]]}
    Current Token length: {chat_manager.total_usage}
    """
    )

    if chat_manager.exceeding_token_limit():
        printer.printt(
            Style.BRIGHT
            + Fore.RED
            + "Warning:\n"
            + Style.RESET_ALL
            + "The token length of this conversation is exceeding the token limit (+ some buffer) for the current model.\n"
            "We are about to reduce the token length by removing the oldest messages from the conversation.\n"
        )
        user_approval = prompt(
            "Should we continue? (y/n)  ",
            style=PromptStyle.from_dict({"prompt": "bold lightblue"}),
        )

        if user_approval.lower() != "y":
            printer.printt(
                Style.BRIGHT
                + Fore.LIGHTBLUE_EX
                + "\n** Conversation loading aborted! **\n"
                + Style.RESET_ALL
            )
            return

        printer.printt(
            "\nReducing token length by removing the oldest messages from the conversation...\n"
        )
        chat_manager.reduce_tokens()
        printer.printt(
            f"{Style.BRIGHT}{Fore.GREEN}Token length reduced successfully!{Style.RESET_ALL}"
        )

    printer.printt(
        Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + "\n** Conversation "
        + Fore.WHITE
        + conversation
        + Fore.LIGHTBLUE_EX
        + " is loaded! **\n"
        + "- - - - - - - - - - - - - - - - - - - - - - - - -"
        + Style.RESET_ALL
    )
    token_limit = int(config.MODELS[ctx.obj["MODEL"]] / 1000)
    printer.printt(
        f"{Style.RESET_ALL}{Style.BRIGHT}Model: {Style.RESET_ALL}{ctx.obj['MODEL']} "
        f"{Style.BRIGHT}Token Limit: {Style.RESET_ALL}{token_limit}k "
        f"{Style.RESET_ALL}{Style.BRIGHT}Style: {Style.RESET_ALL}{ctx.obj['STYLE']}"
    )

    chat_manager.welcome_message(messages=messages)
    messages.pop()

    chat_manager.messages = messages
    chat_manager.chat_loop()


@click.command(help="Choose a previous conversation to delete.")
@click.pass_context
def delete(ctx):
    """Delete previous conversations."""

    printer: Printer = PrinterFactory.get_printer("plain")
    conv_manager: ConversationManager = ctx.obj["CONV_MANAGER"]
    printer.printt(PrintUtils.CONVERSATIONS_INIT_MESSAGE)

    while True:
        conversations = conv_manager.get_conversations()

        msg = (
            Style.BRIGHT
            + Fore.RED
            + "\n** There are no conversations to delete! **"
            + Style.RESET_ALL
        )

        if conv_manager.is_conversations_empty(files=conversations, message=msg):
            return

        # setup file names auto completion
        completer = WordCompleter(conversations, ignore_case=True)

        # print conversations list
        printer.printt(Style.BRIGHT + "Conversations list:" + Style.RESET_ALL)
        for conversation in conversations:
            printer.printt("- " + conversation)

        conversation = prompt(
            "\nChoose a conversation to delete:\n",
            completer=completer,
            style=PromptStyle.from_dict({"prompt": "bold"}),
        )

        # delete conversation file
        if conversation in conversations:
            conv_manager.delete_conversation(conversation)

            printer.printt(
                Style.BRIGHT
                + Fore.LIGHTBLUE_EX
                + "\n** Conversation "
                + Fore.WHITE
                + conversation
                + Fore.LIGHTBLUE_EX
                + " deleted! **\n"
                + Style.RESET_ALL
            )

            # delete conversation from conversations list
            conversations.remove(conversation)
            completer = WordCompleter(conversations, ignore_case=True)
        else:
            printer.printt(
                Style.BRIGHT
                + Fore.RED
                + "\n** Conversation not found! **"
                + Style.RESET_ALL
            )

        msg = (
            Style.BRIGHT
            + Fore.LIGHTBLUE_EX
            + "\n** No more conversations to delete! **"
            + Style.RESET_ALL
        )
        if conv_manager.is_conversations_empty(files=conversations, message=msg):
            return

cli.add_command(install)
cli.add_command(new)
cli.add_command(load)
cli.add_command(delete)

# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    cli()