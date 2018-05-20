# Tempy

Template manager for the command line. Templates are written in
[Mako](http://www.makotemplates.org/) with additional metainfo in Python.

## Metainfo

Metainfos are specified in Python. A file template can include a section
enclosed in `<<<` and `>>>` at the beginning of the template. This section can
contain arbitrary Python code.
For directory templates, this information is contained in a file `metainfo.py`.

Example:
```
<<<
import argparse

description = 'Optional description printed by the "list" command.'
name = 'Optional name used instead of the filename'
parser = argparse.ArgumentParser()
parser.add_argument('somevar', type=sometype)
>>>
...
```

The parser variable is required and is used to pass arguments to the template.
In the template, the variables are accessible through the dictionary variable
`arguments`.

Filenames can also be set through arguments by using a Python format string
as the filename during template definition.
