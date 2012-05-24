from django import forms
from hotclub.topics.models import Topic


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('title', 'content')


