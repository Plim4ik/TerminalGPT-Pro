from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='terminalgpt-pro',
    version='0.3.1',
    description='AI chat assistant in your terminal powered by OpenAI ChatGPT models.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Adam Yodinsky, Shabernev Fedor',
    author_email='quantumstack01@gmail.com',
    keywords=[
        "ai", "chat", "terminal", "openai", "gpt-3", "gpt-4", "gpt4", "gpt3", "chatGPT",
        "assistant", "gpt-3.5", "gpt-3.5-turbo", "terminalGPT-Pro"
    ],
    packages=find_packages(),
    install_requires=[
        'openai>=0.27.6',
        'tiktoken>=0.2,<0.6',
        'colorama>=0.4.6',
        'cryptography>=40.0.2,<42.0.0',
        'click>=8.1.3',
        'prompt-toolkit>=3.0.38',
        'yaspin>=2.3.0',
        'rich>=13.3.5',
        'isort>=5.12.0',
        'pytest>=7.3.1',
        'pylint>=3.0.2'
    ],
    extras_require={
        'dev': [
            'black>=23.1.0',
            'pytest>=7.2.2',
            'pylint>=3.0.2',
            'pexpect>=4.8.0',
            'pytest-cov>=4.0.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'terminalgpt = terminalgptpro.main:cli'
        ]
    },
    python_requires='>=3.9',
)
