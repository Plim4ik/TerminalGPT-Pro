from terminalgptpro.printer import PrinterFactory, PrintUtils
from terminalgptpro.conversations import ConversationManager

def delete_conversation(ctx):
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