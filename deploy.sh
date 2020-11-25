#!/bin/bash

hexo clean
hexo g
python tinify_smms.py
pm2 restart hexo.js
