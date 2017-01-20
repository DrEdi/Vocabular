"""Here are all game functions."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Word
from time import time


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


class Game:
    """Main game object with functions."""

    def __init__(self):
        """Initialization of engine and preparing for session."""
        self.engine = create_engine('sqlite:///mainDB')
        self.Session = sessionmaker(self.engine)

    @repeater
    def addNew(self):
        """Add new object to DB using sqlalchemy session."""
        word = input('Write you word here: ')
        translation = input('Write translation here: ')
        if word and translation:
            session = self.Session()
            entity = Word(word=word, translation=translation,
                          time_of_last_repetition=time(),
                          count_of_repetitions=0,
                          progress=0,
                          count_of_true_answers=0)
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
        choosed = input('\n\nWelcome! The game\'s started! First of all, choose mode:\
                         \n\n1. You see a FOREIGN WORD and must write for this translation.\
                          There is no hints.\
                         \n\n2. You see a TRANSLATION and must write for this word.\
                         \nSo, what would you like to choose?\n~~~~~~~> ')
        if choosed != '1' and choosed != '2':
            print('Invalid data')
            return
        current_time = time()
        session = self.Session()
        for entity in session.query(Word).filter(current_time - Word.time_of_last_repetition > 86400000):
            if choosed == '1':
                answer = input('___________________{word}___________________\n'.format(word=entity.word))
                if answer == entity.translation:
                    print('Congratulation!')
                    entity.count_of_true_answers += 1
                else:
                    print('Sorry, but it\'s not true.')
            elif choosed == '2':
                answer = input('___________________{word}___________________\n'.format(word=entity.translation))
                if answer == entity.word:
                    print('Congratulation!')
                    entity.count_of_true_answers += 1
                else:
                    print('Sorry, but it\'s not true.')
            entity.time_of_last_repetition = time()
            entity.count_of_repetitions += 1
            entity.progress = entity.count_of_true_answers/entity.count_of_repetitions
            session.add(entity)
            session.commit()
        session.close()

    def get_stat(self):
        """Print information about your activity in game."""
        session = self.Session()
        for entity in session.query(Word).all():
            print('|Word: %10s| translation: %10s| progress: %3s|' % (entity.word,
                                                                      entity.translation,
                                                                      entity.progress))
