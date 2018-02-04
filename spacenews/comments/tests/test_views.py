import json
import pytest

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from mixer.backend.django import mixer

from comments.models import Comment


User = get_user_model()


@mixer.middleware(User)
def encrypt_password(user):
    user.set_password('test')
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_list_comments(client):

    mixer.cycle(3).blend(Comment)

    response = client.get('/api/comments/')
    assert response.status_code == 200

    data = json.loads(response.content)
    assert len(data) == 3


@pytest.mark.django_db
def test_retrieve_comments(client):

    comment = mixer.blend(Comment)
    response = client.get(f'/api/comments/{comment.id}/')
    assert response.status_code == 200

    data = json.loads(response.content)
    assert data['content'] == comment.content
    assert data['author']['username'] == comment.author.username


@pytest.mark.django_db
def test_update_comment(client):

    comment = mixer.blend(Comment)

    data = {
        'content': 'testing',
    }

    client.login(username=comment.author.username, password='test')

    response = client.put(f'/api/comments/{comment.id}/', data, format='json')
    assert response.status_code == 200

    comment.refresh_from_db()
    assert comment.content == 'testing'


@pytest.mark.django_db
def test_delete_comment(client):

    comment = mixer.blend(Comment)

    client.login(username=comment.author.username, password='test')
    response = client.delete(f'/api/comments/{comment.id}/')

    assert response.status_code == 204
    assert not Comment.objects.exists()
