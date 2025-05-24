import mkdocs
from material.extensions.emoji import twemoji, to_svg
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)


class ApiDescribedPlugin(mkdocs.plugins.BasePlugin):

    _required_extensions = [
        'mkdocs_apidescribed.extension',  # this is our extension
        'admonition',  # nice admonitions
        'md_in_html',  # for proper indentation
        'pymdownx.details',  # collapsible blocks
        'pymdownx.superfences',  # for block embedding
        'pymdownx.emoji',  # for icons
    ]

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        extensions = config['markdown_extensions']
        current_extensions = set(extensions)

        for ext in self._required_extensions:
            if ext not in current_extensions:
                extensions.append(ext)

        icons_conf = config['mdx_configs'].setdefault('pymdownx.emoji', {})
        icons_conf['emoji_index'] = twemoji
        icons_conf['emoji_generator'] = to_svg

        theme_features = config['theme']._vars.setdefault('features', [])

        feature_annotate = 'content.code.annotate'
        if feature_annotate not in theme_features:
            theme_features.append(feature_annotate)

        return config
