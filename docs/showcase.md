# Showcase

Let's document module ``mkdocs_apidescribed.probe``.

```
 ::: apidescribed: mkdocs_apidescribed.probe
     debug: true
     ignore:
         - "_*"
         - "*ignore*"
```
**Below is automated documentation below.**

----

::: apidescribed: mkdocs_apidescribed.probe
    debug: true
    ignore:
        - "_*"
        - "*ignore*"

## Error example

Now let's try to document an unknown module ``somepackage.somemodule``,
using ``debug: true`` option for troubleshooting:

```
 ::: apidescribed: somepackage.somemodule
     debug: true
```

::: apidescribed: somepackage.somemodule
    debug: true
