import click
from colorama import Fore, Style
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PromptStyle



from .terminal.new import start_new_conversation
from .terminal.install import install_api_key
from .terminal.load import load_conversation
from .terminal.delete import delete_conversation
from .terminal.one_shot import one_shot_message

from terminalgptpro import config
from terminalgptpro.chat import ChatManager
from terminalgptpro.conversations import ConversationManager
from terminalgptpro.encryption import EncryptionManager
from terminalgptpro.printer import PrinterFactory, PrintUtils


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

@cli.command(help="Creating a secret api key for the chatbot."
                + " You will be asked to enter your OpenAI API key.")
def install():
    install_api_key()

@cli.command(help="Start a new conversation.")
@click.pass_context
def new(ctx):
    start_new_conversation(ctx)

@cli.command(help="Choose a previous conversation to load.")
@click.pass_context
def load(ctx):
    load_conversation(ctx)

@cli.command(help="Choose a previous conversation to delete.")
@click.pass_context
def delete(ctx):
    delete_conversation(ctx)

# Добавление команды one_shot
@cli.command(help="One shot question answer.")
@click.argument("question", type=str)
@click.pass_context
def one_shot(ctx, question):
    one_shot_message(ctx, question)

cli.add_command(install)
cli.add_command(load)
cli.add_command(new)
cli.add_command(delete)
cli.add_command(one_shot)


if __name__ == "__main__":
    cli()
