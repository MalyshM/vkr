from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


# DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/vkr_db"

DATABASE_URL_vkr = "postgresql+asyncpg://postgres:admin@db/vkr_db"

engine = create_async_engine(DATABASE_URL_vkr, echo=False)
async_session_vkr = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
async def connect_db_data() -> AsyncSession:
    async with async_session_vkr() as session:
        yield session
DATABASE_URL_users = "postgresql+asyncpg://postgres:admin@db/vkr_db_users"

engine = create_async_engine(DATABASE_URL_users, echo=False)
async_session_users = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def connect_db_users() -> AsyncSession:
    async with async_session_users() as session:
        yield session

def connect_db_data_old():
    DATABASE_URL = "postgresql://postgres:admin@db/vkr_db"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
class Rmup(Base):
    __tablename__ = 'rmup'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('rmup_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    date_of_add = Column(DateTime, nullable=False)


class Stud(Base):
    __tablename__ = 'stud'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stud_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    email = Column(String)
    speciality = Column(String, nullable=False)
    date_of_add = Column(DateTime, nullable=False)


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('teacher_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    lect_or_pract = Column(String, nullable=False)
    date_of_add = Column(DateTime, nullable=False)


class Team(Base):
    __tablename__ = 'team'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('team_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    rmup_id = Column(ForeignKey('rmup.id', ondelete='CASCADE'), ForeignKey('rmup.id'), nullable=False)
    date_of_add = Column(DateTime, nullable=False)

    rmup = relationship('Rmup', primaryjoin='Team.rmup_id == Rmup.id')


class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(BigInteger, primary_key=True, nullable=False, server_default=text("nextval('lesson_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    mark_for_work = Column(Float)
    arrival = Column(String)
    test = Column(Float)
    result_points = Column(Float)
    result_mark = Column(String)
    stud_id = Column(ForeignKey('stud.id', ondelete='CASCADE'), ForeignKey('stud.id'), nullable=False)
    team_id = Column(ForeignKey('team.id', ondelete='CASCADE'), ForeignKey('team.id'), primary_key=True, nullable=False)
    teacher_id = Column(ForeignKey('teacher.id'), ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)
    date_of_add = Column(DateTime, nullable=False)

    stud = relationship('Stud', primaryjoin='Lesson.stud_id == Stud.id')
    teacher = relationship('Teacher', primaryjoin='Lesson.teacher_id == Teacher.id')
    team = relationship('Team', primaryjoin='Lesson.team_id == Team.id')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    fio = Column(String, nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(255), nullable=False)
    isadmin = Column(Boolean, nullable=False)
    isteacher = Column(Boolean, nullable=False)
    iscurator = Column(Boolean, nullable=False)
    date_of_add = Column(DateTime, nullable=False)

