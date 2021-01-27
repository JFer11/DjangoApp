from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import ListView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from polls.models import Question, Choice
from .serializers import QuestionSerializer


# OLD VIEWS -- BEGIN.
def old_old_index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


def old_index(request):
    """
    One way to code view functions (with loader):

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    """

    """Another more common way, with render (No loader or HttpResponse must be imported): """

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def old_detail(request, question_id):
    """return HttpResponse("You're looking at question %s." % question_id)"""
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    """

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def old_results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
# OLD VIEWS -- END


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """
    def get_queryset(self):
        # ""Return the last five published questions.""
        return Question.objects.order_by('-pub_date')[:5]
    """

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class DetailView(generic.CreateView):
    pass


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def myself_2(request):
    print(request)
    import pdb
    pdb.set_trace()
    return HttpResponse("YES!")


def myself(request):
    question = Question.objects.create(question_text='New question', pub_date=timezone.now())
    serializer = QuestionSerializer(question)
    data = serializer.data
    content = JSONRenderer().render(serializer.data)
    print("--------------")
    print("data: ", data)
    print("type: ", type(data))
    print("--------------")
    print("content: ", content)
    print("type: ", type(content))
    print("--------------")
    """
    PILLO
    4 niveles:
        - View normales que se necesita paersear los Json
        - Views con decorators que no precisa pareseo la Request y Rrsponse
        - APIView class que es lo mismo que lo anterior pero con classes
        - Generic y Mixins, en 2 lineas hace todo lo anterior.
    """
    return HttpResponse(content)



"""
There is something called Generic Views. 
Read Here:
https://docs.djangoproject.com/en/1.11/intro/tutorial04/#amend-views
"""