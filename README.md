django-static-hashes
====================

Output files containing hashes of when static files were last updated.

**Installing**

1. Run `pip install git+https://github.com/marinko-peso/django-static-hashes.git`
2. Add 'static_hashes' to `INSTALLED APPS`
3. Add the following to your settings:
```
STATIC_HASHES_STATIC_DIRS = ... #list of folders containing static files you want to get hashes for
STATIC_HASHES_OUTPUT_DIR = ... #path/to/output/javascript/and/json
```


**Create the hashes**

1. Run `manage.py collect_static_hashes`. This may take some time.
2. Take a look at the files defined in STATIC_HASHES_OUTPUT_DIR


**Use the hashes in the browser**

1. Add `{% load static_hashes_tags %}` to your template
2. Add `{% get_static_hashes %}` to your template
3. In javascript you can now acess `hashes`.

Related to [this blog post](http://richardtier.com/2014/10/19/tell-browser-when-files-are-updated/)
