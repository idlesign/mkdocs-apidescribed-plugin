# Introduction

*mkdocs plugin to generate API documentation for Python programs*

* Made to autodocument Python code
* Plays well with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
* Configurable
* Easy to use

!!! tip
    See demo in ``Showcase`` section.

## Requirements

1.  Python 3.10+
2.  `mkdocs` package

## Installation

``` shell
pip install mkdocs-apidescribed-plugin
```

## Configuration

1. Add ``apidescribed`` into ``mkdocs.yml``:

    ```yaml title="mkdocs.yml"
    theme:
      ...
      features:
        ...
        - content.code.annotate  # for parameter descriptions
   
    markdown_extensions:
      - mkdocs_apidescribed.extension # this is our extention
      - admonition  # nice admonitions
      - pymdownx.superfences
      - pymdownx.details  # collapsible blocks
      - md_in_html  # for proper indentation
      - pymdownx.emoji:  # for icons
        emoji_index: !!python/name:material.extensions.emoji.twemoji
        emoji_generator: !!python/name:material.extensions.emoji.to_svg
   
    ```

2. Add ``::: apidescribed:`` directive into your documentation followed by a module path:

    ```md title="index.md"
    This is my documentation
   
    ::: apidescribed: somepackage.somemodule
   
    ```


## Get involved into mkdocs-apidescribed

!!! success "Submit issues"
    If you spotted something weird in application behavior or want to propose a feature you can do 
    that at <https://github.com/idlesign/mkdocs-apidescribed-plugin/issues>

!!! tip "Write code"
    If you are eager to participate in application development, 
    fork it at <https://github.com/idlesign/mkdocs-apidescribed-plugin>, write 
    your code, whether it should be a bugfix or a feature implementation,
    and make a pull request right from the forked project page.

!!! info "Spread the word"
    If you have some tips and tricks or any other words in mind that 
    you think might be of interest for the others --- publish it.
