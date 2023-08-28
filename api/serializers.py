from rest_framework import serializers

from account.models import User
from .models import (Article, Query,
                     Category, MainCategory,
                     PositivePoint, PenaltyPoint)


class QuerySerializer( serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Query
        fields = ('title', 'description', 'minimum', 'maximum', 'category')


class PositivePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositivePoint
        fields = ('score', 'article', 'user')

    def create(self, validated_data):
        positive, _ = PositivePoint.objects.update_or_create(
            article=validated_data['article'],
            user=self.context.get('user'),
            defaults={
                'score': validated_data['score']
            }
        )
        return positive


class PenaltyPointSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.filter(position=3))

    class Meta:
        model = PenaltyPoint
        fields = ('score', 'files', 'article', 'user')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    positives = PositivePointSerializer(many=True, read_only=True)
    point = serializers.SerializerMethodField(method_name='get_point')
    penalties = PenaltyPointSerializer(many=True, read_only=True)
    query = QuerySerializer()

    class Meta:
        model = Article
        fields = ('id', 'files', 'author', 'query', 'penalties', 'positives', 'point')

    def get_point(self, instance):
        return instance.get_point()


class ArticleCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Article
        fields = ('id', 'files', 'author', 'query', )

    def create(self, validated_data):
        article, _ = Article.objects.update_or_create(
            author = validated_data['author'],
            query=validated_data['query'],
            files=self.context.get('files'),

            defaults={
                'files': self.context.get('files')
            }
        )
        return article


class CategorySerializer(serializers.ModelSerializer):
    queries = QuerySerializer(many=True)
    main = serializers.SlugRelatedField(slug_field='name', queryset=MainCategory.objects.all())

    class Meta:
        model = Category
        fields = ('name', 'queries', 'main')


class MinCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class MainCategorySerializer(serializers.ModelSerializer):
    catalogs = MinCategorySerializer(many=True)

    class Meta:
        model = MainCategory
        fields = ('name', 'appraiser', 'catalogs')