from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Article, Category, Query
from api.serializers import (ArticleSerializer, CategorySerializer,
                             PositivePointSerializer, PenaltyPointSerializer,
                             ArticleCreateSerializer, QuerySerializer)


class HomeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class QueriesApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, cat_id):
        queryset = Query.objects.filter(category=cat_id)
        serializer = QuerySerializer(queryset, many=True)
        return Response(data=serializer.data, status=200)


class ArticleCreateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ArticleCreateSerializer(
            data=request.data,
            context={'files': request.FILES.get('files')}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)


class ArticleApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, cat_id):
        queryset = Article.objects.filter(query__category=cat_id)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)


class GradeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        score = request.data.get('score', None)
        if score is None:
            return Response({'Error': '"score" is missing'})
        score = request.data.get('score')
        if int(score) > 0:
            serializer = PositivePointSerializer(data=request.data, context={
                'user': request.user
            })
        else:
            serializer = PenaltyPointSerializer(
                data=request.data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)
