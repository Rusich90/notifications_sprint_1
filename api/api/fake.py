import random
import time

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from db.database import AbstractDataBase
from db.database import get_db_service
from emails.emails import Emails
from emails.emails import get_email_service
from models.fake import Response
from services.short_url import ShortUrl
from services.short_url import get_short_url_service

router = APIRouter()


@router.get('/registration')
async def fake_response(short_url: ShortUrl = Depends(get_short_url_service),
                        emails: Emails = Depends((get_email_service)),
                        db: AbstractDataBase = Depends(get_db_service)) -> Response:
    random_user = random.choice(db.get_all_users())
    link = short_url.get_short_url(random_user['id'])
    data = {
        'subject': 'Привет!',
        'recipients': [random_user['email']],
        'html_template': 'welcome_mail.html',
        'full_name': f'{random_user["first_name"]} {random_user["last_name"]}',
        'link': link,
        'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png'
    }
    emails.send_email(data)

    return Response(result='Письмо для подтверждения отправлено на вашу почту')


@router.get('/redirect')
async def fake_response(id: str, timestamp: float,
                        db: AbstractDataBase = Depends(get_db_service)) -> Response:
    if time.time() > timestamp:
        return status.HTTP_404_NOT_FOUND
    db.update_user(id)
    return Response(result='Спасибо за регистрацию!')
