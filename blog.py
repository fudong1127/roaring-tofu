from tornado import web

from model import Article, Commit, Post, Review, Tweet, meta
from util import render_mako
import app_urls

def render_blog(posts=[], offset=0, post_count=1, rpp=5):
	articles = Article.recent_articles()
	commits = Commit.recent_commits()
	reviews = Review.recent_reviews()
	tweet = Tweet.recent_tweet()

	prev = None
	if offset:
		prev = max(offset - rpp, 0)
	next = None
	if offset + rpp < post_count:
		next = min(post_count - 1, offset + rpp)

	return render_mako('index.mako',
					   posts=posts,
					   recent_tweet=tweet,
					   commits=commits,
					   reviews=reviews,
					   articles=articles,
					   start=offset,
					   end=offset + len(posts),
					   prev=prev,
					   next=next,
					   total=post_count)


class view_post(web.RequestHandler):
	"""
	Blog servlet
	"""
	def get(self, id):
		self.set_header("Content-Type","text/html; charset=utf-8")
		post = meta.session.query(Post).filter(Post.id == id).all()

		if not post:
			# 404
			return app_blog.notfound()

		return render_blog(posts=post, rpp=1)

urls = [('/view/(\d+)', view_post)]
app_urls.urls.extend(urls)
