#!/bin/sh

rsync -auP  posts/assets/* root@bugswriter.com:/var/www/blog/posts/assets/
rsync -uP posts/*.html root@bugswriter.com:/var/www/blog/posts/
rsync -uP index.html root@bugswriter.com:/var/www/blog/ 
