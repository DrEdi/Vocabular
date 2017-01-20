"""This module contains entities for program."""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///../mainDB')

Base = declarative_base()


class Word(Base):
    """Model for words that represent entity from DB."""

    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String(200))
    translation = Column(String(200))
    count_of_repetitions = Column(Integer)
    time_of_last_repetition = Column(Integer)

    def __repr__(self):
        """Render word instance as its text and translation."""
        return '{word} : {translation}'.format(word=self.word,
                                               translation=self.translation)


Base.metadata.create_all(engine)
