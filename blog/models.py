from articles.models import Article, ArticleByTypeManager


class Blog(Article):

    class Meta:
        proxy = True

    objects = ArticleByTypeManager(type=Article.TYPES.blog)
