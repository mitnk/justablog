"""
Flask Module Docs:  http://flask.pocoo.org/docs/api/#flask.Module

This file is used for both the routing and logic of your
application.
"""
from flask import Module, url_for, render_template, request, redirect
from models import Article
from forms import ArticleForm
from utils import requires_auth, pygments_markdown

views = Module(__name__, 'views')


@views.route('/')
def index():
    """Render website's index page."""
    articles = Article.all().order('-added')
    articles = [x for x in articles if x.is_public]
    return render_template('index.html', articles=articles)


@views.route(r'/a/<number>/')
def get_aritle(number):
    """Render website's index page."""
    articles = Article.all()
    articles = articles.filter('number <=', int(number))
    articles = articles.filter('number >=', int(number))
    if articles.count() == 0:
        return render_template('404.html'), 404
    article = articles[0]
    if not article.is_public:
        return render_template('404.html'), 404
    return render_template('article.html', article=article, content=pygments_markdown(article.content))


@views.route('/article/add/', methods=["POST", "GET"])
@requires_auth
def add_article():
    """Add a article."""
    form = ArticleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the right number - the article ID
            number = 1
            articles = Article.all().order('-number')
            if articles.count() > 0:
                number = articles[0].number + 1

            article = Article(
                number=number,
                title=form.title.data,
                content=form.content.data,
                tags=form.tags.data,
                is_public=form.is_public.data,
            )
            article.save()
            return redirect(url_for('index'))
    return render_template('add_article.html', form=form)


@views.after_request
def add_header(response):
    """Add header to force latest IE rendering engine and Chrome Frame."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


