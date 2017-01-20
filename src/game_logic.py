"""Here are all game functions."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Word
from time import time


class Game():
    """Main game object with functons."""

    def __init__(self):
        """Initialization of engine and preparing for session."""
        self.engine = create_engine('sqlite:///../mainDB')
        self.Session = sessionmaker(self.engine)

    def repeater(fn):
        """Decorator that wheel function till user want to play."""
        def wrap(self):
            next_step = True
            while next_step:
                fn(self)
                one_more = input('One more? y/n\n')
                if one_more != 'y':
                    next_step = False
        return wrap

    @repeater
    def addNew(self):
        """Add new object to DB using sqlalchemy session."""
        word = input('Write you word here: ')
        translation = input('Write translation here: ')
        if word and translation:
            session = self.Session()
            entity = Word(word=word, translation=translation,
                          time_of_last_repetition=time(),
                          count_of_repetitions=0)
            session.add(entity)
            session.commit()
            session.close()
        else:
            print('Some part of data may be damaged. You can try again')

    @repeater
    def delete(self):
        """Delete object from DB using sqlalchemy session."""
        word = input('CAUTION! If you put word that does not exist in DB, exeption will not raised\
                    \n\nPut here word you want to delete: ')
        if word:
            session = self.Session()
            session.query(Word).filter(Word.word == word).delete(synchronize_session=False)
            session.commit()
            session.close()

    @repeater
    def play(self):
        """Main game logic."""
        choosed = input('\n\nWelcome! The game\'s started! Fisrt of all, chose mode:\
                         \n\n1. You see a FOREIGN WORD and must write for this translation.\
                         \nThere is no hints.\
                         \n\n2. You see a TRANSLATION and must write for this word.\
                         \nSo, what would you like to choose?\n~~~~~~~>')
        if choosed == 1:
            pass
        elif choosed == 2:
            pass
        else:
            print('Ouuuups, something gone wrong! Try one more time!')


if __name__ == '__main__':
    game = Game()
    game.addNew()
