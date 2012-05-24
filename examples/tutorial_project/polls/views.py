from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from .models import Choice, Poll

app_label = __package__.split('.')[-1]

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response(app_label + '/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(p.get_results_url())

