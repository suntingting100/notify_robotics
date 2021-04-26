import uvicorn
from cyclone import setting
from cyclone import app_logger


if __name__ == '__main__':
    app_logger.info('****************** Starting Server *****************')
    uvicorn.run(app='cyclone:app',
                host=setting.host,
                port=setting.port,
                reload=True,
                log_level=setting.log_level,
                debug=True)
