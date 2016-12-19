from django.test import TestCase

from datetime import datetime
from django.utils import timezone

from .models import Post
from .admin import PostAdminForm

class TestCaseBase(TestCase):
    party_like_its_1999 = timezone.make_aware(datetime(year=1999, month=12, day=31, hour=23, minute=59, second=59))

class PostModelTest(TestCaseBase):

    def test_saving_and_retriving_a_post(self):

        post = Post()
        post.datetime = self.party_like_its_1999
        post.save()

        self.assertEqual(Post.objects.count(), 1)

class PostAdminFormTest(TestCaseBase):

    def test_empty_form_does_not_validate(self):

        form = PostAdminForm()
        self.assertFalse(form.is_valid())

    def test_form_saves_an_object(self):

        form = PostAdminForm(
            data={
                'datetime': self.party_like_its_1999,
            }
        )

        self.assertTrue(form.is_valid())

        post = form.save()
        saved_post = Post.objects.get(id=post.id)

        self.assertEqual(saved_post.datetime, self.party_like_its_1999)
