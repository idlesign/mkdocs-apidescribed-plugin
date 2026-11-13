# Configuration

To configure ``apidescribed`` one can use yaml just after  ``::: apidescribed: `` directive:

```
 ::: apidescribed: mkdocs_apidescribed.config
     debug: true
     categorize: false
     only: 
         - DEFAULT_CONFIG
     location:
         mode: module
```

----

A global configuration may be set in ``mkdocs.yml``, so that it applies to every directive:

```yaml title="mkdocs.yml"
plugins:
 - apidescribed:
     config:
       categorize: false
```

The resulting configuration is composed as follows: built-in defaults, updated with the global config, updated with directive options.

----

**All available configuration options are listed below:**

::: apidescribed: mkdocs_apidescribed.config
    debug: true
    categorize: false
    only: 
        - DEFAULT_CONFIG
    location:
        mode: module
