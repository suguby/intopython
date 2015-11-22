from django.views.generic import ListView, DetailView, FormView


from forums.models import Category, Topic, Forum, Post


class CategoryListView(ListView):
    model = Category


class ForumDetailView(DetailView):
    model = Forum


class TopicDetailView(DetailView):
    model = Topic
