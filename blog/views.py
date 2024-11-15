from django.shortcuts import redirect, render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from rest_framework_simplejwt.authentication import JWTAuthentication
from permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PostApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, *args, **kwargs):
        data = {
            'title': "Realism", 
            'text': "Realism is an artistic movement that emerged in the mid-19th century, significantly influencing literature, painting, theater, and other art forms.", 
            'author': request.user.id
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(user = request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
class PostDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    
    def get_object(self, post_id, user_id):
        try:
            return Post.objects.get(id=post_id, user = user_id)
        except Post.DoesNotExist:
            return None


    def get(self, request, post_id, *args, **kwargs):
        post_instance = self.get_object(post_id, request.user.id)
        if not post_instance:
            return Response(
                {"res": "Text with post id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PostSerializer(post_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, post_id, *args, **kwargs):
        post_instance = self.get_object(post_id, request.user.id)
        if not post_instance:
            return Response(
                {"res": "Text with post id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': "Realism", 
            'text': "Realism is an artistic movement that emerged in the mid-19th century, significantly influencing literature, painting, theater, and other art forms.", 
            'author': request.user.id
        }
        serializer = PostSerializer(instance = post_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, post_id, *args, **kwargs):
        post_instance = self.get_object(post_id, request.user.id)
        if not post_instance:
            return Response(
                {"res": "Text with post id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        post_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

    
    

    



