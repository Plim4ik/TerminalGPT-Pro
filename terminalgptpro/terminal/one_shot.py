from ..config import *
from ..chat import *
from ..conversations import *
from ..encryption import *
from ..printer import *
from ..main import *

def one_shot_message(ctx, question):
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
