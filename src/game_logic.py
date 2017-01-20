"""Here are all game functions."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Word
from time import time

engine = create_engine('sqlite:///../mainDB')
Session = sessionmaker(engine)


def addNew():
    """Add new object to DB using sqlalchemy session."""
    new = True
    while new:
        word = input('Write you word here: ')
        translation = input('Write translation here: ')
        if word and translation:
            session = Session()
            entity = Word(word=word, translation=translation,
                          time_of_last_repetition=time(),
                          count_of_repetitions=0)
            session.add(entity)
            session.commit()
            session.close()
            add_one_more = input('Add more? y/n\n')
            if add_one_more == 'y':
                pass
            else:
                new = False
        else:
            print('Some part of data may be damaged. Please, try again')


def delete():
    """Delete object from DB using sqlalchemy session."""
    word = input('CAUTION! If you put word that does not exist in DB, exeption will not raised\
                \n\nPut here word you want to delete: ')
    if word:
        session = Session()
        session.query(Word).filter(Word.word == word).delete(synchronize_session=False)
        session.commit()
        session.close()


if __name__ == '__main__':
    addNew()
