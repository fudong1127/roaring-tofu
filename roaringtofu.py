#!/usr/bin/env python
from sqlalchemy import create_engine
import web

from blog import app_blog, render_blog
from read import app_read
import config
from model import Post, init_model, meta
from yelp_redir import yelp_redir

web.config.debug = False

urls = ('/blog', app_blog,
		'/read', app_read,
		'/(\d*)', 'index',
		'/yelp/(.*)', yelp_redir)

app = web.application(urls, globals())
#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
#application = app.wsgifunc()
read_conn = create_engine(config.engine_url, **config.engine_params)
init_model(read_conn)

class index(object):
	def GET(self, offset):
		web.header("Content-Type","text/html; charset=utf-8")
		count = meta.session.query(Post).count()

		if offset:
			offset = int(offset)
		else:
			offset = 0

		if offset > count:
			# temp redirect to home
			pass

		posts = meta.session.query(Post).order_by(Post.time_created.desc()).limit(5).offset(offset).all()

		return render_blog(posts=posts, offset=offset, post_count=count, rpp=5)

if __name__ == "__main__":
	app.run()
