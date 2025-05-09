import mkdocs
from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)


class ApiDescribedPlugin(mkdocs.plugins.BasePlugin):
    ...
