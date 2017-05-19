# -*- coding: utf-8 -*-
"""
Home view
"""
import feedparser
import time
import twitter
from flask import render_template, request, redirect
from flask.ext.login import current_user


from backend.backend.views import ENDPOINT
from backend.backend.decorators import authentication_required

BLOG_FEED_UPDATE_INTERVAL = 900  # 15 minutes


class BlogFeedHandler(object):
    """
    Retrieve the blog feed
    """
    blog_rss_url = 'http://blog.eventsage.com/feed/'
    blog_feed_cache = []
    last_time_updated = 0
    update_interval = BLOG_FEED_UPDATE_INTERVAL

    def _cache_needs_update(self):
        """
        Does the feed cache need to be updated?

        - when the cache has expired
        - when the cache is empty
        """
        expired = (time.time() - self.last_time_updated) > self.update_interval
        return expired or len(self.blog_feed_cache) == 0

    def _update_blog_feed(self, try_again=True):
        """
        Retrieve blog feed (no cache)

        - if retrieval fails, try again once more
        - if retrieval fails a second time (try_again=False), use the existing
          cache and DO NOT mark the cache as updated
        """
        feed = feedparser.parse(self.blog_rss_url)
        new_blog_feed = feed.entries
        # new_blog_feed = feedparser.parse(self.blog_rss_url).entries

        if len(new_blog_feed) > 0:
            self.blog_feed_cache = new_blog_feed
            self.last_time_updated = time.time()
        elif try_again:
            self._update_blog_feed(try_again=False)

    def get_blog_feed(self):
        """
        Retrieve blog feed

        - use this method to access the blog feed
        """
        if self._cache_needs_update():
            self._update_blog_feed()
        return self.blog_feed_cache

    def __init__(self, *args, **kwargs):
        """
        Initialize
        """
        super(self.__class__, self).__init__(*args, **kwargs)


BLOG_FEED_HANDLER = BlogFeedHandler()


@ENDPOINT.route('/')
def home_page():
    """
    The Eventsage homepage
    """
    from backend.backend.app import TWITTER

    try:
        tweets = TWITTER.get_tweets()
    except twitter.error.TwitterError:
        tweets = [{'text': 'Cannot Display Tweets'}]

    data_args = {
        'blog_feed': BLOG_FEED_HANDLER.get_blog_feed(),
        'tweets': tweets,
    }

    return render_template('home.html', **data_args)


@ENDPOINT.route('/sign-up')
@ENDPOINT.route('/sign-in')
def redirect_page():
    """
    Signup / Signin redirect pages, load over a stub of the homepage
    """
    return render_template('home-stub.html')


@ENDPOINT.route('/signup')
@ENDPOINT.route('/signin')
def legacy_signin_redirect():
    """
    Work-around for an unfortunate use of 301 moved permanently
    """
    next = request.args.get('next', '')
    if next:
        return redirect('/' + next, 301)
    url = '/sign-up' if request.path == '/signup' else 'sign-in'
    return redirect(url, 302)


@ENDPOINT.route('/notifications')
@authentication_required
def user_notifications():
    """
    User-level notifications page
    """
    from backend.backend.models.notification import Notification
    user = current_user.to_dbref()
    notifications = {
        'new': Notification.objects(user_for=user, read=False, complete=False).order_by('-created'),
        'read': Notification.objects(user_for=user, read=True, complete=False).order_by('-created'),
        'completed': Notification.objects(user_for=user, complete=True).order_by('-created')
    }
    return render_template('notifications.html', notifications=notifications)


@ENDPOINT.route('/supplier-terms')
def supplier_terms():
    """
    Terms of use page for suppliers
    """
    return render_template('supplier-terms.html')


@ENDPOINT.route('/careers')
def careers():
    """
    Job postings
    """
    return render_template('careers.html')
