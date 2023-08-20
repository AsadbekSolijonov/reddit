from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from posts import models
from posts import serializers
from django.contrib.auth.models import User, Group
import logging

logging.basicConfig(format=u'%(filename)s [LINE: %(lineno)d]:  #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        logging.info(self.request.data)
        logging.info(self.kwargs)
        logging.info(self.args)
        logging.info(serializer)
        serializer.save(poster=self.request.user)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=self.kwargs['pk'], poster=self.request.user)
        if post.exists():
            self.destroy(request, *args, **kwargs)
            return Response(data={'status': 204, 'message': 'Your post deleted!'})
        else:
            raise ValidationError('This is not your post to delete, BRUH!')


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post :)')
        user = self.request.user
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(voter=user, post=post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={
                'status': 204,
                'message': 'You just deleted this vote :( '
            })
        else:
            raise ValidationError('You never voted for this post...silly.')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
