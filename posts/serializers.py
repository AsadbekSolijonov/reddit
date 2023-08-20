from rest_framework import serializers
from posts import models
from django.contrib.auth.models import User, Group


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = ['id', 'post', 'url', 'poster', 'poster_id', 'created', 'votes']

    def get_votes(self, post):
        return models.Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = ['id']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'password', 'username', 'is_staff', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']
