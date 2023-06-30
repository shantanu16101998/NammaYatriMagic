from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# List of available commands for autocompletion
available_commands = ['command1', 'command2', 'command3', 'command4']

# Create a WordCompleter with the available commands
completer = WordCompleter(available_commands)

# Main loop for user input
while True:
    user_input = prompt('> ', completer=completer)
    # Process the user input
    print('Input:', user_input)
