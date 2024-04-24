import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger import LOGGER
from models import connect_db_users

user_router = APIRouter(tags=["User"])


@user_router.get('/api/get_all_users', name='User:get_all_users', status_code=status.HTTP_200_OK, description=
"""
        Returns:
            List of Users
        \n
        [
          {
            "password": "$2b$12$DCthI8sRH52m7ax0c8r1D.hAsHLLp4.Kmy5cveAoYNOeYnWaykS7e",
            "id": 5,
            "isadmin": true,
            "iscurator": true,
            "email": "string",
            "fio": "string",
            "username": "string",
            "isteacher": true,
            "date_of_add": "2024-01-12T00:00:00"
          },
          {
            "password": "$2b$12$vtIbx59Sh.GuN3MqijRmoO769ZfdSC3JStLkL5L9RH97Cw/aE81ja",
            "id": 6,
            "isadmin": true,
            "iscurator": true,
            "email": "strin1g",
            "fio": "strin1g",
            "username": "strin1g",
            "isteacher": true,
            "date_of_add": "2024-01-12T00:00:00"
          }
        ]
""")
async def get_all_users(db: AsyncSession = Depends(connect_db_users)):
    start_time = time.time()
    href = f"get_all_users"
    LOGGER.info(f"{href} start")
    try:
        all_users = await db.execute("""
            Select *
            from users u
        """)
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        return all_users.fetchall()
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@user_router.get('/api/delete_all_users', name='User:delete_all_users', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Returns:
                             {"message": "All users deleted successfully"}
                         \n
                         {
                           "message": "All users deleted successfully"
                         }
                 """)
async def delete_all_users(db: AsyncSession = Depends(connect_db_users)):
    start_time = time.time()
    href = f"delete_all_users"
    LOGGER.info(f"{href} start")
    try:
        await db.execute("""DELETE FROM users""")
        await db.commit()
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        return {"message": "All users deleted successfully"}
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@user_router.get('/api/delete_test_user', name='User:delete_test_user', status_code=status.HTTP_200_OK,
                 description=
                 """
                         Returns:
                             {"message": "All users deleted successfully"}
                         \n
                         {
                           "message": "All users deleted successfully"
                         }
                 """)
async def delete_test_user(db: AsyncSession = Depends(connect_db_users)):
    start_time = time.time()
    href = f"delete_test_user"
    LOGGER.info(f"{href} start")
    try:
        await db.execute("""
            DELETE FROM users u
             where u.username = 'string' and 
             u.email = 'string' and 
             u.fio = 'string'
         """)
        await db.commit()
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        return {"message": "test user deleted successfully"}
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
