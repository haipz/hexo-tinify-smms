#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2020-11-25 00:00:00
# @Author  : Haipz Lin (haipzm@gmail.com)
# @Link  : https://github.com/haipz/
# @Version : 1.0.0
import re
import requests
import json
import sys
import os
import hashlib
import tinify

class ImageUploader():
  def __init__(self,hexo_source_dir,next_source_dir):
    self.__hexo_source_dir = hexo_source_dir
    self.__next_source_dir = next_source_dir
    self.__backup_dir = 'backup'
    self.__tinify_dir = 'tinify'
    self.__images_db = 'images.db'
    self.__smms_key = 'Please put your SMMS key here'
    self.__tinify_key = 'Please put your Tinify key here'
    if not os.path.exists(self.__backup_dir):
      os.makedirs(self.__backup_dir)
    if not os.path.exists(self.__tinify_dir):
      os.makedirs(self.__tinify_dir)
    os.system('cp -rf ' + self.__hexo_source_dir + '/ ' + self.__backup_dir + '/')
    print('Backup ' + self.__hexo_source_dir + ' to ' + self.__backup_dir)
    if not os.path.exists(self.__images_db):
      with open(self.__images_db,mode='w',encoding='utf-8') as ff:
        print('Create image.db')
    with open(self.__images_db,mode='r',encoding='utf-8') as img_db:
      db_str = img_db.read()
      if db_str.strip() == '':
        db_str = '{}'
      self.__images_dict = json.loads(db_str)
      print('Load image.db')
      print(db_str)

  def smms_upload(self,img_path):
    try:
      smms_url = 'https://sm.ms/api/v2/upload'
      data = {'smfile':open(img_path,'rb'),'format':'json'}
      headers = {'Authorization':self.__smms_key}
      response = requests.post(
        smms_url,
        files=data,
        headers=headers
      )
      #print(response.text)
      img_new_url = json.loads(response.text)
      try:
        cloud_path = img_new_url['data']['url']
      except BaseException as err:
        print(err)
        cloud_path = img_new_url['images']
      print('SMMS url to {}'.format(cloud_path))
      return cloud_path
    except BaseException as err:
      print('Error in smms_upload: {}'.format(err))

  def tinify_upload(self,img_path):
    try:
      tinify.key = self.__tinify_key
      img_name = os.path.basename(img_path)
      tiny_img_path = os.path.join(self.__tinify_dir, img_name)
      source = tinify.from_file(img_path)
      source.to_file(tiny_img_path)
      print('Tinify file to {}'.format(tiny_img_path))
      return tiny_img_path
    except BaseException as err:
      print('Error in tinify_upload: {}'.format(err))
      return img_path

  def get_img_url(self,img_path):
    try:
      md5 = hashlib.md5()
      md5.update(open(img_path,'rb').read())
      img_md5 = md5.hexdigest()
      print('Image MD5 {}'.format(img_md5))
      if img_md5 not in self.__images_dict:
        tiny_img_path = self.tinify_upload(img_path)
        img_url = self.smms_upload(tiny_img_path)
        if img_url != ''  and img_url != None:
        	self.__images_dict[img_md5] = img_url
      else:
        img_url = self.__images_dict.get(img_md5)
      return img_url
    except BaseException as err:
      print('Error in get_img_url: {}'.format(err))

  def change_img_path(self, file_path):
    try:
      with open(file_path,mode='r',encoding='utf-8') as ff:
        file_content = ff.read()
        img_blocks = re.findall(r'!\[.*?\)',file_content)
        print('Find {} image block'.format(len(img_blocks)))
        article_content = file_content
        for i in range(len(img_blocks)):
          #print('Image block {}'.format(img_blocks[i]))
          img_origin_url = re.findall(r'\((.*?)\)',img_blocks[i])
          if (len(img_origin_url) > 0):
            #print('Image origin url {}'.format(img_origin_url[0]))
            if str(img_origin_url[0]).startswith('/images'):
              img_path = self.__next_source_dir + img_origin_url[0]
              #print('Image path {}'.format(img_path))
              img_new_url = self.get_img_url(img_path)
              #print(img_new_url)
              if img_new_url != None:
                article_content = article_content.replace(str(img_origin_url[0]),str(img_new_url))
              #print(article_content)
              print('Origin URL: {}, Path: {}, New URL: {}'.format(img_origin_url[0],img_path,img_new_url))
        return article_content
    except BaseException as err:
      print('Error in change_img_path: {}'.format(err))
      return ''

  def md_write(self,file_path,file_content):
    try:
      with open(file_path,'w',encoding = 'utf-8') as md:
        md.write(file_content)
      print('Job done {}'.format(file_path))
    except BaseException as err:
      print('Error in md_write: {}'.format(err))

  def save_cache(self):
    try:
      with open(self.__images_db,'w',encoding='utf-8') as img_db:
        img_db.writelines(json.dumps(self.__images_dict))
    except BaseException as err:
      print('Error in save_cache: {}'.format(err))

  def do_work(self):
    try:
      for root,dirs,files in os.walk(self.__hexo_source_dir):
        for name in files:
          if str(name).endswith('md'):
            file_path = os.path.join(root,name)
            print(file_path)
            file_content = self.change_img_path(file_path)
            if file_content == '':
              print('Job failed {}'.format(file_path))
              continue
            self.md_write(file_path,file_content)
            self.save_cache()
    except BaseException as err:
      print('Error in do_work: {}'.format(err))

if __name__ == '__main__':
  hexo_source_dir = '/home/haipz/hexo/blog/source'
  next_source_dir = '/home/haipz/hexo/blog/themes/next/source'
  smms = ImageUploader(hexo_source_dir, next_source_dir)
  smms.do_work()
