from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context["view"].action in ["create", "update",
                                           "partial_update"]:
            new_status = data.get('status')
            if new_status:
                if not self.instance or self.instance.status != new_status:
                    if new_status == 'OPEN':
                        number_open = Advertisement.objects.filter(
                            creator=self.context["request"].user)
                        number_open = number_open.filter(status='OPEN').count()
                        if number_open >= 10:
                            raise serializers.ValidationError(
                                "У одного пользователя не может быть "
                                "больше 10 открытых объявлений!")
        return data
