from terminalgptpro.encryption import EncryptionManager
from terminalgptpro.printer import PrinterFactory, PrintUtils
from terminalgptpro import config

def start_new_conversation(ctx):
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
