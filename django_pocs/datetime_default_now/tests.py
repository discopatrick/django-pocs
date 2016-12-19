from django.test import TestCase

from datetime import datetime
from django.utils import timezone

from .models import Post

class PostModelTest(TestCase):

    def test_saving_and_retriving_a_post(self):

        post = Post()
        post.datetime = timezone.make_aware(datetime(year=1999, month=12, day=31, hour=23, minute=59, second=59))
        post.save()

        self.assertEqual(Post.objects.count(), 1)
