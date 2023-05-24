import logging
import logging.config

logging.config.fileConfig('logger.conf')
LOG = logging.getLogger(__name__)