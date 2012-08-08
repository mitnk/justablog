"""
Flask Module Docs:  http://flask.pocoo.org/docs/api/#flask.Module

This file is used for both the routing and logic of your
application.
"""
from flask import Module, url_for, render_template, request, redirect
from models import Article
from forms import ArticleForm
from utils import requires_auth, pygments_markdown, get_aritle_by_number

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
    article = get_aritle_by_number(number)
    if article is None or not article.is_public:
        return render_template('404.html'), 404
    return render_template('article.html', article=article, content=pygments_markdown(article.content))


@views.route('/add/', methods=["POST", "GET"])
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
            return redirect(url_for('get_aritle', number=number))
    action_url = url_for('add_article')
    return render_template('add_article.html', form=form, action_url=action_url)


@views.route('/edit/<int:number>/', methods=["POST", "GET"])
@requires_auth
def edit_article(number):
    """Add a article."""
    article = get_aritle_by_number(number)
    if article is None:
        return render_template('404.html'), 404

    form = ArticleForm(
        title=article.title,
        content=article.content,
        is_public=article.is_public,
    )
    if request.method == 'POST':
        if form.validate_on_submit():
            article.title = form.title.data
            article.content = form.content.data
            article.is_public = form.is_public.data
            article.tags = form.tags.data
            article.save()
            return redirect(url_for('edit_list'))
    action_url = url_for('edit_article', number=number)
    return render_template('add_article.html', form=form, action_url=action_url)


@views.route('/edit/')
@requires_auth
def edit_list():
    """Render website's index page."""
    articles = Article.all().order('-added')
    return render_template('edit_list.html', articles=articles)


@views.after_request
def add_header(response):
    """Add header to force latest IE rendering engine and Chrome Frame."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


