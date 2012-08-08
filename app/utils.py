import markdown
import settings

from flask import Response, request
from functools import wraps
from libs.BeautifulSoup import BeautifulSoup
from models import Article
from pygments import lexers, formatters, highlight

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == settings.USER and password == settings.PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def pygments_markdown(content):
    _lexer_names = reduce(lambda a,b: a + b[2], lexers.LEXERS.itervalues(), ())
    _formatter = formatters.HtmlFormatter(cssclass='highlight')

    html = markdown.markdown(content)
    # Using html.parser to prevent bs4 adding <html> tag
    soup = BeautifulSoup(html)
    for pre in soup.findAll('pre'):
        if pre.code:
            txt = unicode(pre.code.text)
            lexer_name = "text"
            if txt.startswith(':::'):
                lexer_name, txt = txt.split('\n', 1)
                lexer_name = lexer_name.split(':::')[1]

            if lexer_name not in _lexer_names:
                lexer_name = "text"
            lexer = lexers.get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
            highlighted = highlight(txt, lexer, _formatter)
            div_code = BeautifulSoup(highlighted).div
            if not div_code:
                return content
            pre.replaceWith(div_code)
    return unicode(soup)


def get_aritle_by_number(number):
    articles = Article.all()
    articles = articles.filter('number <=', int(number))
    articles = articles.filter('number >=', int(number))
    if articles.count() == 0:
    	return None
    return articles[0]
