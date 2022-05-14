import random
import time

from fastapi import APIRouter, Depends, status

from db.database import AbstractDataBase, get_db_service
from models.fake import Response
from services.producer import producer

router = APIRouter()


@router.get('/registration')
async def fake_response(db: AbstractDataBase = Depends(get_db_service)) -> Response:
    random_user = random.choice(db.get_all_users())
    await producer(random_user)
    return Response(result='Письмо для подтверждения отправлено на вашу почту')


@router.get('/redirect')
async def fake_response(id: str, timestamp: float,
                        db: AbstractDataBase = Depends(get_db_service)) -> Response:
    if time.time() > timestamp:
        return status.HTTP_404_NOT_FOUND
    db.update_user(id)
    return Response(result='Спасибо за регистрацию!')
