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

**All available configuration options are listed below:**

::: apidescribed: mkdocs_apidescribed.config
    debug: true
    categorize: false
    only: 
        - DEFAULT_CONFIG
    location:
        mode: module
