#!/bin/bash

hexo clean
hexo g
python tiny_smms.py
pm2 restart hexo.js
