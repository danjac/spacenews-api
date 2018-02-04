from rest_framework import viewsets

from .models import Post
from .permissions import PostPermission
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = (PostPermission, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
