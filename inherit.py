from enum import Enum
import sys

from sqlalchemy import Column, create_engine, Enum as EnumCol, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()
engine = create_engine("sqlite://")
DBSession = sessionmaker(bind=engine)
session = DBSession()


class UserType(Enum):
  """An Enum to store the 'types' used to differentiate the join"""
  User = "user"
  Participant = "participant"
  Host = "host"

  def __str__(self):
    return self.value


class User(Base):
  """The base type of user"""

  __tablename__ = "user"
  id = Column(Integer, primary_key=True)
  username = Column(String(128), nullable=False)
  type = Column(EnumCol(UserType, length=128, values_callable=lambda ut: [t.value for t in ut]), nullable=False)

  __mapper_args__ = {
    "polymorphic_identity": UserType.User,
    "polymorphic_on": type
  }

  def __str__(self):
    return f"{self.username} is type {self.type}\n"


class Participant(User):
  """A sub-type of user"""

  __tablename__ = "participant"
  id = Column(Integer, ForeignKey("user.id"), primary_key=True)
  questions = relationship("Question", back_populates="participant")

  __mapper_args__ = {
    "polymorphic_identity": UserType.Participant
  }

  def __str__(self):
    return f"{super().__str__()}{self.username} asked {'. '.join([question.content for question in self.questions])}"


class Host(User):
  """Another sub-type of user"""
  __tablename__ = "host"
  id = Column(Integer, ForeignKey("user.id"), primary_key=True)
  answers = relationship("Answer", back_populates="host")

  __mapper_args__ = {
    "polymorphic_identity": UserType.Host
  }

  def __str__(self):
    return f"{super().__str__()}{self.username} answered {'. '.join([answer.content for answer in self.answers])}"


class Question(Base):
  """An example relationship"""

  __tablename__ = "question"
  answer = relationship("Answer", back_populates="question", uselist=False)
  content = Column(String(128), nullable=False)
  id = Column(Integer, primary_key=True)
  participant_id = Column(Integer, ForeignKey("participant.id"), nullable=False)
  participant = relationship("Participant", back_populates="questions")


class Answer(Base):
  """Another example relationship"""

  __tablename__ = "answer"
  content = Column(String(128), nullable=False)
  id = Column(Integer, primary_key=True)
  host_id = Column(Integer, ForeignKey("host.id"), nullable=False)
  host = relationship("Host", back_populates="answers")
  question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
  question = relationship("Question", back_populates="answer")


if __name__ == "__main__":
  Base.metadata.create_all(engine)

  q1 = Question(content="What is blue?")
  p1 = Participant(username="Peter", questions=[q1])

  q2 = Question(content="What is red?")
  p2 = Participant(username="Paul", questions=[q2])
  
  a1 = Answer(question=q1, content="A blue cat")
  h1 = Host(username="Henry", answers=[a1])
  
  a2 = Answer(question=q2, content="A red cat")
  h2 = Host(username="Harold", answers=[a2])

  session.add_all([p1, p2, h1, h2])
  session.commit()

  print("All Users:")
  all_users = session.query(User).all()
  for user in all_users:
    print(user.username)
  
  print()

  print("All participants:")
  all_participants = session.query(Participant).all()
  for participant in all_participants:
    print(participant.username)

  print()

  print("All questions:")
  all_questions = session.query(Question).all()
  for question in all_questions:
    print(f"{question.participant.username} asked: {question.content}")
    if question.answer:
      print(f"and {question.answer.host.username} answered: {question.answer.content}")
