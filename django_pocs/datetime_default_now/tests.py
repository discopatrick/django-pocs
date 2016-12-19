from django.test import TestCase
from django.utils import timezone

from datetime import datetime
from unittest import skip

from .models import Post
from .admin import PostAdminForm

class TestCaseBase(TestCase):
    party_like_its_1999 = timezone.make_aware(datetime(year=1999, month=12, day=31, hour=23, minute=59, second=59))
    the_morning_after = timezone.make_aware(datetime(year=2000, month=1, day=1, hour=11, minute=00, second=00))

class PostModelTest(TestCaseBase):

    def test_saving_and_retriving_a_post(self):

        post = Post()
        post.datetime = self.party_like_its_1999
        post.save()

        self.assertEqual(Post.objects.count(), 1)

class PostAdminFormTest(TestCaseBase):

    def test_form_is_bound(self):

        form = PostAdminForm()
        self.assertFalse(form.is_bound)

        form2 = PostAdminForm(data={})
        self.assertTrue(form2.is_bound)

    def test_empty_form_does_not_validate(self):

        form = PostAdminForm(data={})
        self.assertFalse(form.is_valid())

    def test_valid_form_saves_an_object(self):

        form = PostAdminForm(
            data={
                'datetime': self.party_like_its_1999,
            }
        )

        self.assertTrue(form.is_valid())

        post = form.save()
        saved_post = Post.objects.get(id=post.id)

        self.assertEqual(saved_post.datetime, self.party_like_its_1999)

    def test_changing_date_via_form(self):

        form = PostAdminForm(
            data={
                'datetime': self.party_like_its_1999,
            }
        )

        self.assertTrue(form.is_valid())        

        post = form.save()
        form2 = PostAdminForm(data={'datetime': self.the_morning_after}, instance=post)

        self.assertTrue(form2.is_valid())

        form2.save()
        saved_post = Post.objects.get(id=post.id)
        
        self.assertEqual(saved_post.datetime, self.the_morning_after)
