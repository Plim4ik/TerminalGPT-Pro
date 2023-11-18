# [TerminalGPT-Pro]


Welcome to TerminalGPT-Pro, the terminal-based ChatGPT personal assistant app!
With TerminalGPT-Pro, you can easily interact with the OpenAI GPT-3.5 and GPT-4 language models.

Whether you need help with a quick question or want to explore a complex topic, TerminalGPT-Pro is here to assist you. Simply enter your query and TerminalGPT-Pro will provide you with the best answer possible based on its extensive knowledge base.


## Why?

Some advantages of using TerminalGPT-Pro over the chatGPT browser-based app:

- It doesn't disconnect like the browser-based app, so you can leave it running in a terminal session on the side without losing context.
- It's highly available and can be used whenever you need it.
- It's faster with replies than the browser-based app.
- You can use TerminalGPT-Pro with your IDE terminal, which means you won't have to constantly switch between your browser and your IDE when you have questions.
- TerminalGPT-Pro's answers are tailored to your machine's operating system, distribution, and chip-set architecture
- Doesn't use your conversation data for training the model (unlike the browser-based app).
- Your conversations are stored locally on your machine, so only you can access them.

## Pre-requisites

- Python 3.6 or higher
- An OpenAI Account and API key.
   1. Sign up at <https://beta.openai.com/signup> using email or Google/Microsoft account.
   2. Go to <https://beta.openai.com/account/api-keys> or click on "View API keys" in the menu to get your API key.

## Installation

1. Install the latest TerminalGPT-Pro with pip install.

```sh
pip install terminalgpt (optional -U --user)
```

2. Now you have `terminalgpt` command available in your terminal. Run the following install command to configure the app.

```sh
terminalgpt install
```

3. Enter your OpenAI API key when prompted and press enter.

4. Choose one of the models below as the default model. it can be overridden with the `-m --model` flag later.

5.  Choose a printing style ('markdown' is recommended)

That's it! You're ready to use TerminalGPT!
You can now start a new conversation with `terminalgpt new` or load a previous conversation with `terminalgpt load`. Also you can reinstall with `terminalgpt install` or delete previous conversations with `terminalgpt delete`.

---

## Usage

### TL;DR

```sh
Usage: terminalgpt [OPTIONS] COMMAND [ARGS]...

  *~ TerminalGPT-Pro - Your Personal Terminal Assistant ~*

Options:
  --version                       Show the version and exit.
  -m, --model [gpt-3.5-turbo|gpt-3.5-turbo-16k|gpt-4|gpt-4-32k]
                                  Choose a model to use. [default:gpt-3.5-turbo]
  -s, --style [markdown|plain]    Output style. [default: markdown]
  --help                          Show this message and exit.

Commands:
  delete    Choose a previous conversation to delete.
  install   Creating a secret api key for the chatbot.
  load      Choose a previous conversation to load.
  new       Start a new conversation.
  one-shot  One shot question answer.
```

### New

Start a new conversation:

```sh
terminalgpt new
```

### One-Shot

One shot question to get a fast answer in the terminal.

```sh
terminalgpt one-shot "What is the meaning of life?"
```

### Load

Load previous conversations:

```sh
terminalgpt load
```

### Delete

Delete previous conversations:

```sh
terminalgpt delete
```

