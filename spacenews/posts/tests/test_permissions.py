from unittest import mock

from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

from posts.models import Post
from posts.permissions import PostPermission


def test_get_all_if_anonymous():

    req = HttpRequest()
    req.method = 'GET'
    req.user = AnonymousUser()

    perm = PostPermission()
    assert perm.has_permission(req, mock.Mock())


def test_post_if_anonymous():

    req = HttpRequest()
    req.method = 'POST'
    req.user = AnonymousUser()

    perm = PostPermission()
    assert not perm.has_permission(req, mock.Mock())


def test_get_instance_if_anonymous():

    req = HttpRequest()
    req.method = 'GET'
    req.user = AnonymousUser()

    perm = PostPermission()
    assert perm.has_object_permission(req, mock.Mock(), Post())


def test_put_instance_if_anonymous():

    req = HttpRequest()
    req.method = 'PUT'
    req.user = AnonymousUser()

    perm = PostPermission()
    assert not perm.has_object_permission(req, mock.Mock(), Post())


def test_delete_instance_if_anonymous():

    req = HttpRequest()
    req.method = 'DELETE'
    req.user = AnonymousUser()

    perm = PostPermission()
    assert not perm.has_object_permission(req, mock.Mock(), Post())

