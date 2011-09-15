from django.views.generic import TemplateView, DetailView, ListView

from cb.models import Article


class HomeView(TemplateView):
    template_name = 'cb/home.html'

    def get_context_data(self):
        main_article = Article.objects.all().order_by('-date_created')[0]
        other_articles = Article.objects.all().order_by('-date_created')[1:5]
        return {'main_article': main_article,
                'other_articles': other_articles}
        
        
class ArticleListView(ListView):
    model = Article
    template_name = 'cb/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        return self.model.objects.all().exclude(date_published=None)
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleListView, self).get_context_data(**kwargs)
        ctx['unpublished_articles'] = self.model.objects.filter(date_published=None)
        return ctx
    

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'cb/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetailView, self).get_context_data(**kwargs)
        
        article = self.object
        ctx['related_articles'] = Article.tagged.related_to(article)
        
        # We need to use a different date field for comparison depending on
        # if the article is published
        if article.is_published:
            previous = Article.objects.filter(date_published__lt=article.date_published)
            next = Article.objects.filter(date_published__gt=article.date_published)
        else:
            previous = Article.objects.filter(date_created__lt=article.date_created)
            next = Article.objects.filter(date_created__gt=article.date_created)
        
        ctx['previous_article'] = previous[0] if len(previous) > 0 else None
        ctx['next_article'] = next[0] if len(next) > 0 else None
        return ctx
    
class AboutView(TemplateView):
    template_name = 'about.html'


class ProjectsView(TemplateView):
    template_name = 'projects.html'

    
class TalksView(TemplateView):
    template_name = 'talks.html'
