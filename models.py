from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, text, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

DATABASE_URL = "postgresql://postgres:admin@localhost/vkr_db"
def connect_db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class Student(Base):
    __tablename__ = 'student'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('student_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    speciality = Column(String, nullable=False)
    team_for_lectures = Column(String)
    team_for_practices = Column(String, nullable=False)


class StudyMeeting(Base):
    __tablename__ = 'study_meeting'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('study_meeting_id_seq'::regclass)"))
    presence = Column(Boolean, nullable=False)
    mark = Column(Float, nullable=False)
    test = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    date_of_add = Column(DateTime, nullable=False)
    student_id = Column(ForeignKey('student.id'), ForeignKey('student.id', ondelete='CASCADE'), nullable=False)

    student = relationship('Student', primaryjoin='StudyMeeting.student_id == Student.id')
    student1 = relationship('Student', primaryjoin='StudyMeeting.student_id == Student.id')
