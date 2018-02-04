from rest_framework import viewsets

from .models import Comment
from .permissions import CommentPermission
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.select_related('author')
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission, )
