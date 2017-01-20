"""Start module for game."""
from src.game_logic import Game


def start():
    """Starting the game."""
    game = Game()
    opinion = input('What would you like to do?\n'
                    '1. Add new words to my vocabulary\n'
                    '2. Delete some words\n'
                    '3. Let\'s play :)\n'
                    'For exit press any other button\n')
    if opinion == '1':
        game.addNew()
    elif opinion == '2':
        game.delete()
    elif opinion == '3':
        game.play()
        game.get_stat()
    else:
        game.get_stat()
        print('Bye :)')


if __name__ == '__main__':
    start()
