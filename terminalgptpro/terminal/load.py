
from ..config import *
from ..chat import *
from ..conversations import *
from ..encryption import *
from ..printer import *
from ..main import *

def load_conversation(ctx):
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