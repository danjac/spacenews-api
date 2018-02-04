from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from comments.serializers import CommentSerializer

from .models import Post
from .permissions import PostPermission
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.select_related('author').order_by('-created')
    serializer_class = PostSerializer
    permission_classes = (PostPermission, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @detail_route(
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            post=self.get_object(),
            author=self.request.user,
        )
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
