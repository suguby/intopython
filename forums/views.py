from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView

from forums.forms import TopicCreateForm
from forums.models import Category, Topic, Forum, Post


class CategoryListView(ListView):
    model = Category


class ForumDetailView(DetailView):
    model = Forum


class TopicDetailView(DetailView):
    model = Topic


class TopicCreateView(FormView):
    template_name = 'forums/topic_create.html'
    form_class = TopicCreateForm

    def __init__(self):
        self.forum = ''

    def dispatch(self, request, *args, **kwargs):
        self.forum = Forum.objects.get(id=kwargs.get('forum_id', None))
        if self.forum.is_closed and not request.user.is_staff:
            messages.error(request, "У вас нет прав на создание топика")
            return HttpResponseRedirect(reverse_lazy('forum:forum_detail', args=[self.forum.id]))
        return super(TopicCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        topic_name = form.cleaned_data['topic']
        post_body = form.cleaned_data['message']
        user = self.request.user

        topic = Topic(forum=self.forum, name=topic_name)
        topic.save()
        post = Post(topic=topic, body=post_body, user=user)
        post.save()
        topic.save()

        self.success_url = reverse('forum:topic_detail', args=[topic.id])

        return super(TopicCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TopicCreateView, self).get_context_data(**kwargs)
        context['forum'] = Forum.objects.get(id=self.kwargs.get('forum_id', None))
        return context