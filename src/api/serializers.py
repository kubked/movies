from rest_framework import serializers

from api.models import Comment, Movie


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for retrieving movies list."""
    class Meta:
        model = Movie
        fields = ('id', 'title', 'details')


class MovieRequestSerializer(serializers.Serializer):
    """Serialize /movies POST request which consists of title only."""
    title = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        instance['title'] = validated_data.get('title', instance['title'])

    def create(self, validated_data):
        return {
            'title': validated_data.get('title')
        }


class CommentSerializer(serializers.ModelSerializer):
    """Serialize Comment objects. Allows creating and retrieving comments."""
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment')
