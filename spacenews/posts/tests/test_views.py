import json
import pytest

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from mixer.backend.django import mixer

from posts.models import Post


User = get_user_model()


@mixer.middleware(User)
def encrypt_password(user):
    user.set_password('test')
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_posts(client):

    mixer.cycle(5).blend(Post)

    response = client.get('/api/posts/')
    assert response.status_code == 200

    data = json.loads(response.content)
    assert len(data) == 5


@pytest.mark.django_db
def test_get_post(client):

    post = mixer.blend(Post)
    response = client.get(f'/api/posts/{post.id}/')
    assert response.status_code == 200

    data = json.loads(response.content)
    assert data['title'] == post.title
    assert data['author']['username'] == post.author.username


@pytest.mark.django_db
def test_update_post(client):

    post = mixer.blend(Post)

    data = {
        'title': 'testing...',
        'url': 'https://reddit.com',
    }

    client.login(username=post.author.username, password='test')

    response = client.put(f'/api/posts/{post.id}/', data, format='json')
    assert response.status_code == 200

    post.refresh_from_db()

    assert post.title == 'testing...'
    assert post.url == 'https://reddit.com'


@pytest.mark.django_db
def test_delete_post(client):

    post = mixer.blend(Post)

    client.login(username=post.author.username, password='test')
    response = client.delete(f'/api/posts/{post.id}/')

    assert response.status_code == 204
    assert not Post.objects.exists()
