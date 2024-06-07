from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FeaturedAds
from advertisements.permissions import IsAdminOrOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        queryset = super(AdvertisementViewSet, self).get_queryset()
        user = self.request.user
        if user and user.id:
            query = queryset.filter(~Q(status='DRAFT') | Q(creator=user))
        else:
            query = queryset.filter(~Q(status='DRAFT'))
        return query

    @action(detail=False, permission_classes=[IsAuthenticated])
    def favorites(self, request):
        ads = Advertisement.objects.filter(favourite_by=request.user)
        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def add_favorites(self, request, pk=None):
        ads = self.get_object()
        if ads.creator == request.user:
            return Response({'message': 'Добавлять в избраное можно только '
                                        'чужие обьявления!'})
        else:
            FeaturedAds.objects.create(ads=ads, user=request.user)
            return Response({'message': 'Обьявление добавлено в избраное!'})

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def del_favorites(self, request, pk=None):
        ads = self.get_object()
        featured_ads = FeaturedAds.objects.filter(ads=ads).filter(
            user=request.user)
        featured_ads.delete()
        return Response({'message': 'Обьявление удалено из избраных!'})

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminOrOwner()]
        return []
