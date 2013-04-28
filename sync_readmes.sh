#!/bin/bash

pandoc -f markdown -t rst README.md > README.rst
cat README.rst | sed -e 's/\/_screenshots\//https:\/\/raw\.github\.com\/yakxxx\/django-addview\/master\/_screenshots\//g' > README.rst.tmp
cat README.rst.tmp > README.rst
rm README.rst.tmp