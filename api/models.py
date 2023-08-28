from django.db import models
from django.db.models import Avg, Sum

from account.models import User


class MainCategory(models.Model):
    name = models.CharField(max_length=255)
    appraiser = models.ManyToManyField(User, related_name='main_categories')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    main = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='catalogs')

    def __str__(self):
        return self.name


class Query(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    minimum = models.SmallIntegerField(default=1)
    maximum = models.SmallIntegerField(default=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='queries')

    def __str__(self):
        return self.title


class Article(models.Model):
    files = models.FileField(upload_to='files/uploads/')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='articles')
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    @property
    def positive(self):
        if self.positives.values('article').exists():
            return self.positives.values('article').annotate(Sum('score'))
        return [{'score__sum': 0}]

    @property
    def penalty(self):
        if self.penalties.values('article').exists():
            return self.penalties.values('article').annotate(Sum('score'))
        return [{'score__sum': 0}]

    def get_point(self):
        return self.positive[0]['score__sum'] + self.penalty[0]['score__sum']


    def __str__(self):
        return f"{self.author} for \"{self.query.title}\""


class PenaltyPoint(models.Model):
    score = models.SmallIntegerField()
    files = models.FileField(upload_to='files/feedBacks/')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='penalties')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_penalties')

    def __str__(self):
        return str(self.score)


class PositivePointQueryset(models.QuerySet):
    def get_avg_score(self, article_id):
        return PositivePoint.objects.values(article_id).annotate(Avg('score'))

    def get_sum_score(self, article_id):
        return PositivePoint.objects.values(article_id).annotate(Sum('score'))


class PositivePoint(models.Model):
    score = models.SmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='positives')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_positives', null=True)

    objects = PositivePointQueryset.as_manager()

    def __str__(self):
        return f'{self.score} by {self.user} for "{self.article.query}"'