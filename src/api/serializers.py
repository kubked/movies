from rest_framework import serializers

from api.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'details')


class MovieRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        instance['title'] = validated_data.get('title', instance['title'])

    def create(self, validated_data):
        return {
            'title': validated_data.get('title')
        }
