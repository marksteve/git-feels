#!/bin/bash
npm install
watchify -t reactify -g uglifyify \
  app/static/js/main.js \
  -o app/static/js/main.min.js \
  -v
