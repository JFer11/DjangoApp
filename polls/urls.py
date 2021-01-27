from django.conf.urls import url

from . import views

"""
What is the role of app_name:

In real Django projects, there might be five, ten, twenty apps or more. How does Django differentiate the URL names
between them? For example, the polls app has a detail view, and so might an app on the same project that is for a blog.
How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag?

The answer is to add namespaces to your URLconf. In the polls/urls.py file, go ahead and add an app_name to set the
application namespace:

Now change your polls/index.html template:
From:
    <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
To:
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li
"""
app_name = 'polls'


"""
The keyword "name" in url, is, for example, for the {% url %} html template engine tag. 
Example: <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>

Instead set the link manually like that: <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>,
we call the function by its name. This approach become less challenging when we want to change URLs on projects 
with a lot of templates.
"""

"""
Regular way to bind view functions with URLs:

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/old
    url(r'^old/$', views.old_index, name='old index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
"""
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^example/$', views.myself, name='yoyo'),
    url(r'^example/2/$', views.myself_2, name='m2'),
]
# La vista genérica DetailView espera que el valor de la clave primaria capturado desde la URL sea denominado "pk",
# por lo que hemos cambiado``question_id`` a pk para las vistas genéricas.
import django.contrib.admin.templates