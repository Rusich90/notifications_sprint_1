import logging

from db.database import PostgresDataBase
from emails.emails import Emails

users = PostgresDataBase()

user = users.get_user('27796a4f-6437-41d6-b536-179d3de00fd1')

logger = logging.getLogger('app')
logger.info('hello!!!')

data = {
    'subject': 'Привет!',
    'recipients': [user['email']],
    'html_template': 'mail.html',
    'full_name': f'{user["first_name"]} {user["last_name"]}',
    'text': 'Произошло что-то интересное! :)',
    'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png'
}

email = Emails()
email.send_email(data)
