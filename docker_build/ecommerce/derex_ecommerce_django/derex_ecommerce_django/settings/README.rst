Settings for edX
================

This directory contains django settings files that `derex.ecommerce` uses to drive
the edX Ecommerce Service. If your project does not have a `plugins/derex.ecommerce/settings`
directory, this one will be used for you, and its `base.py` file will be used to configure
the Ecommerce Service

If your project has a `plugins/derex.ecommerce/settings` directory, it will be populated
using these files. The files derex copies to your project dir are not meant to be edited.
If you upgrade derex, a new version of these files might be bundled. In this
case the existing files in the project will be updated to the new content.
