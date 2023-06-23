from datetime import datetime

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker

import settings


BASE_URL = 'https://jservice.io/api/random?count='

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################


# create async engine for interaction with database
engine = create_async_engine(
    settings.REAL_DATABASE_URL, future=True, echo=True
)

# create session for the interaction with database
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


##############################
# BLOCK WITH DATABASE MODELS #
##############################


# class Base(DeclarativeBase):
#     pass
Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, nullable=False, primary_key=True)
    question_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=False)
    pub_date = Column(DateTime(timezone=True), nullable=False)


###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class QuestionDAL:
    """Data Access Layer for creating question in db"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_question(
        self,
        question_id: int,
        question_text: str,
        answer_text: str,
        pub_date: str,
    ) -> Question:
        new_question = Question(
            question_id=question_id,
            question_text=question_text,
            answer_text=answer_text,
            pub_date=pub_date,
        )
        self.db_session.add(new_question)
        await self.db_session.flush()
        return new_question


#########################
# BLOCK WITH API MODELS #
#########################


# gets question from request
class Question_API(BaseModel):
    """Used as input to get number of questions needed"""

    questions_num: int = Field(gt=-1, description="Must be positive number")


class ShowQuestion(BaseModel):
    """Question from external API"""

    id: int = None
    answer: str = None
    question: str = None
    created_at: datetime = None


#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="task1")

question_router = APIRouter()


async def task(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        questions = response.json()
        return questions


@question_router.post('/', response_model=ShowQuestion)
async def get_questions(question: Question_API, additional: bool = False):
    """Get and validate set of questions from external API"""
    count = question.questions_num
    if count:
        url = BASE_URL + str(count)
        questions = await task(url)

        questions = [ShowQuestion(**data) for data in questions]
        duplicates = await _check_if_exists(questions)
        if duplicates:
            del_list = []
            add_qty = len(duplicates)
            for _ in range(len(questions)):
                if questions[_].id in duplicates:
                    del_list.append(_)
            for _ in del_list:
                del questions[_]
            new = await get_questions(
                Question_API(questions_num=add_qty), additional=True
            )
            questions.extend(new)
        if additional:
            return questions
        question = await _create_new_questions(questions)
        return ShowQuestion(
            id=question.question_id,
            answer=question.answer_text,
            question=question.question_text,
            created_at=question.pub_date,
        )
    return ShowQuestion()


async def _check_if_exists(body: list[ShowQuestion]) -> int:
    async with async_session() as session:
        async with session.begin():
            for question in body:
                q = select(Question).filter(
                    Question.question_id == question.id
                )
                result = await session.execute(q)
                result = result.all()
                if result:
                    ids = [q.question_id for q in result[0]]
                    return ids
                return


async def _create_new_questions(body: list[ShowQuestion]) -> Question:
    async with async_session() as session:
        async with session.begin():
            question_dal = QuestionDAL(session)
            question = []

            for question in body:
                question = await question_dal.create_question(
                    question_id=question.id,
                    question_text=question.question,
                    answer_text=question.answer,
                    pub_date=question.created_at,
                )
            return question


# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(
    question_router,
    prefix="",
    tags=["question_num"],
)
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
