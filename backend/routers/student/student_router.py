import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger import LOGGER
from models import connect_db_data
from redis import process_href, save_resp_and_return_it

student_router = APIRouter(tags=["Student"])


@student_router.get('/api/get_student', name='Student:get_stud', status_code=status.HTTP_200_OK,
                    description=
                    """
                            Получает id_stud: int
                            Returns:
                                Студент
                            \n
                            {
                              "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                              "id": 2,
                              "email": "stud0000278787@study.utmn.ru",
                              "date_of_add": "2024-01-13T00:00:00",
                              "name": "bcd765d44ffc513ca68a954f119ea527407c413e3486c7029ff0c5522343810a"
                            }
                    """)
async def get_student(id_stud: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    href = f"get_student-{id_stud}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        all_users = await db.execute(f"""
            select
                *
            from
                stud s
            where
                s.id = {id_stud}
        """)
        result = all_users.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
