from quintette.views.generic import ListView, DetailView
from hotclub.answers.models import Question


class list_questions(ListView):
    extra_context = {'navbar_selected': 'answers'}
    context_object_name = 'topic_list'
    queryset = Question.objects.all()
    template_name = 'hotclub/topics/list-topics.html' 


class view_question(DetailView):
    extra_context = {'navbar_selected': 'answers'}
    model = Question
    pk_url_kwarg = 'question_id'
    template_name = 'hotclub/answers/view-question.html'

