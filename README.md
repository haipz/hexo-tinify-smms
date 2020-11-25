# hexo-tinify-smms

This is a Python script to compress your local images then upload to SMMS, and then retrieve image link from SMMS, and replace into the hexo markdown files of post/page.
It supports to cache image MD5 hash to `images.db` with JSON format, to save the API usage.

# How to deploy

Clone this repository to `hexo` root folder. 

# How to use

1. Please go to [SMMS](https://sm.ms/), register and login.
2. Go to [SMMS -> User -> Dashboard -> API Token](https://sm.ms/home/apitoken) to get your SMMS API key.
3. Go to [Tinify -> Developer API](https://tinypng.com/developers), enter your name and email address, then you will receive a mail contains Tinify API key.
4. Put your SMMS API key and Tinify API key into that script.
5. Modify `hexo_source_dir` to your hexo source folder absolute path.
6. Modify `next_source_dir` to your hexo theme source folder absolute path.
7. Run the script with Python.

# Python references

* tinify
* requests
* hashlib
* json

# Note

You could use the `deploy.sh` to make it easier for deployment.
If you are not using `pm2` to manage your `hexo` job, please remove `pm2 restart hexo.js` from `deploy.sh`.
