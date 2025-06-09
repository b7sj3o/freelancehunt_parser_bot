import logging

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.engine.Engine').disabled = True

