import os

from mkdocs.commands import build
from mkdocs import config

os.chdir('../')

cfg = config.load_config()
cfg.plugins.on_startup(command='build', dirty=False)
try:
    build.build(cfg)
finally:
    cfg.plugins.on_shutdown()
