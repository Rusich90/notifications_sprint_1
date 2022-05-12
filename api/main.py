import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import fake

app = FastAPI(
    default_response_class=ORJSONResponse,
)

app.include_router(fake.router, prefix='/api/fake')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.DEBUG,
        reload=True,
    )
