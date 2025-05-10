import yaml
from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)


DEFAULT_CONFIG = {
    'debug': False,  # show traceback
    'skip': False,  # do not describe (allows instructions to be ignored)
    'format': 'auto',  # docstrings format (sphinx, google, numpy)

    'heading_base': 2,  # headings base level
    'autolinks': True,  # automatically create hyperlinks
    'categorize': True,  # show symbol types (categories) titles

    'location': {
        # signature block title options
        # hidden - do not show the block
        # module - show module "path"
        # file - show filepath
        'mode': 'hidden',
        'line': False,  # show line number of source file
    },
    'icons': {
        'attr': ':material-alpha:',  # for attributes
        'func': ':material-function:',  # for functions
        'cls': ':material-delta:',  # for classes
        'property': ':material-alpha-p-box-outline:',  # for class properties
        'classmethod': ':material-alpha-c-box-outline:',  # for class methods
        'staticmethod': ':material-alpha-s-box-outline:',  # for static methods
        'inherited': ':material-subdirectory-arrow-left:',  # for class inherited items
        'clsbases': ':material-alpha-b-box:',  # for base classes
        'raises': ':material-lightning-bolt:',  # for descriptions of raised exceptions
        'returns': ':material-arrow-right-thin:',  # for descriptions of returned value
    },

    'undocumented': False,  # describe items without docstrings
    'inherited': True,  # describe inherited items (e.g. from parent classes)
    'types': [
        # symbol types to describe (order respected)
        'attributes',
        'functions',
        'classes',
    ],
    'ignore': [
        # patterns of symbol names to ignore
        '_*',
    ],
    'only': [
        # symbol names to describe (others will be ignored)
    ],
}
"""Default configuration for mkdocs-apidescribed."""


def config_parse(src: str) -> dict:
    try:
        cfg = yaml.load(src, yaml.SafeLoader)
    except yaml.MarkedYAMLError:
        log.exception('Unable to parse options.')
        cfg = {}

    return cfg or {}


def config_merge(base: dict, *, upd: dict) -> dict:
    out = {}

    for key, val in base.items():

        if (upd_val := upd.get(key)) is not None:

            if isinstance(val, dict) and isinstance(upd_val, dict):
                upd_val = config_merge(val, upd=upd_val)

            val = upd_val

        out[key] = val

    return out


def get_config(src: str) -> dict:
    parsed = config_parse(src)
    merged = config_merge(DEFAULT_CONFIG, upd=parsed)
    return merged
