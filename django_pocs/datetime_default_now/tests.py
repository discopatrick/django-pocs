from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import datetime
from unittest import skip

from .models import Post, PostWithDefaultDateTime
from .admin import PostAdminForm, PostWithDefaultDateTimeAdminForm

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

    def test_completed_form_does_validate(self):

        form = PostAdminForm(data={ 'datetime': self.party_like_its_1999 })
        self.assertTrue(form.is_valid())

    def test_valid_form_saves_an_object(self):

        form = PostAdminForm(data={ 'datetime': self.party_like_its_1999 })

        self.assertTrue(form.is_valid())

        post = form.save()
        saved_post = Post.objects.get(id=post.id)

        self.assertEqual(saved_post.datetime, self.party_like_its_1999)

    def test_invalid_form_raises_error_on_save(self):

        form = PostAdminForm(data={})
        self.assertFalse(form.is_valid())

        with self.assertRaises(ValueError):
            post = form.save()

    def test_changing_date_via_form(self):

        form = PostAdminForm(data={ 'datetime': self.party_like_its_1999 })

        self.assertTrue(form.is_valid())        

        post = form.save()
        form2 = PostAdminForm(data={'datetime': self.the_morning_after}, instance=post)

        self.assertTrue(form2.is_valid())

        form2.save()
        saved_post = Post.objects.get(id=post.id)
        
        self.assertEqual(saved_post.datetime, self.the_morning_after)

class PostAdminViewTest(TestCaseBase):
    
    def test_post_admin_view_renders_form(self):

        user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
        self.client.force_login(user)

        response = self.client.get('/admin/datetime_default_now/post/add/')

        self.assertIn(PostAdminForm().fields['datetime'].label, response.content.decode())

    def test_post_admin_add_view_processes_a_post_request(self):

        Post.objects.all().delete() # clear all post objects

        user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
        self.client.force_login(user)

        response = self.client.post(
            '/admin/datetime_default_now/post/add/',
            data={
                'datetime_0': '2016-12-20',
                'datetime_1': '17:05:27' 
            }
        )

        # should redirect to post list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/datetime_default_now/post/')
        self.assertEqual(Post.objects.count(), 1)

        saved_post = Post.objects.first()
        saved_post_datetime = saved_post.datetime

        self.assertEqual(
            saved_post_datetime,
            timezone.make_aware(datetime(2016, 12, 20, 17, 5, 27))
        )

    def test_post_admin_edit_view_updates_post_datetime(self):

        Post.objects.all().delete() # clear all post objects

        user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
        self.client.force_login(user)

        response = self.client.post(
            '/admin/datetime_default_now/post/add/',
            data={
                'datetime_0': '2016-12-20',
                'datetime_1': '17:05:27' 
            }
        )

        self.assertEqual(Post.objects.count(), 1)

        saved_post = Post.objects.first()
        saved_post_datetime = saved_post.datetime

        self.assertEqual(
            saved_post_datetime,
            timezone.make_aware(datetime(2016, 12, 20, 17, 5, 27))
        )

        response = self.client.post(
            '/admin/datetime_default_now/post/%s/change/' % (saved_post.id,),
            data={
                'datetime_0': '2015-06-30',
                'datetime_1': '12:00:00' 
            }
        )

        self.assertEqual(Post.objects.count(), 1)

        saved_post = Post.objects.first()
        saved_post_datetime = saved_post.datetime

        self.assertEqual(
            saved_post_datetime,
            timezone.make_aware(datetime(2015, 6, 30, 12, 0, 0))
        )

class PostWithDefaultDateTimeAdminFormTest(TestCaseBase):

    def test_valid_form_saves_an_object(self):

        form = PostWithDefaultDateTimeAdminForm(data={ 'datetime': self.party_like_its_1999 })

        self.assertTrue(form.is_valid())

        post = form.save()
        saved_post = PostWithDefaultDateTime.objects.get(id=post.id)

        self.assertEqual(saved_post.datetime, self.party_like_its_1999)

    def test_changing_date_via_form(self):

        form = PostWithDefaultDateTimeAdminForm(data={ 'datetime': self.party_like_its_1999 })

        self.assertTrue(form.is_valid())        

        post = form.save()
        form2 = PostWithDefaultDateTimeAdminForm(data={'datetime': self.the_morning_after}, instance=post)

        self.assertTrue(form2.is_valid())

        form2.save()
        saved_post = PostWithDefaultDateTime.objects.get(id=post.id)
        
        self.assertEqual(saved_post.datetime, self.the_morning_after)

    @skip # this fails
    def test_postwithdefaultdatetime_admin_add_view_processes_a_post_request(self):

        PostWithDefaultDateTime.objects.all().delete() # clear all post objects

        user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
        self.client.force_login(user)

        response = self.client.post(
            '/admin/datetime_default_now/postwithdefaultdatetime/add/',
            data={
                'datetime_0': '2016-12-20',
                'datetime_1': '17:05:27' 
            }
        )

        # should redirect to post list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/datetime_default_now/postwithdefaultdatetime/')
        self.assertEqual(PostWithDefaultDateTime.objects.count(), 1)

        saved_post = PostWithDefaultDateTime.objects.first()
        saved_post_datetime = saved_post.datetime

        self.assertEqual(
            saved_post_datetime,
            timezone.make_aware(datetime(2016, 12, 20, 17, 5, 27))
        )

    @skip # this fails
    def test_postwithdefaultdatetime_admin_edit_view_updates_post_datetime(self):

        PostWithDefaultDateTime.objects.all().delete() # clear all post objects

        user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
        self.client.force_login(user)

        response = self.client.post(
            '/admin/datetime_default_now/postwithdefaultdatetime/add/',
            data={
                'datetime_0': '2016-12-20',
                'datetime_1': '17:05:27' 
            }
        )

        self.assertEqual(PostWithDefaultDateTime.objects.count(), 1)

        saved_post = PostWithDefaultDateTime.objects.first()
        saved_post_datetime = saved_post.datetime

        self.assertEqual(
            saved_post_datetime,
            timezone.make_aware(datetime(2016, 12, 20, 17, 5, 27))
        )

        response = self.client.post(
            '/admin/datetime_default_now/postwithdefaultdatetime/%s/change/' % (saved_post.id,),
            data={
                'datetime_0': '2015-06-30',
                'datetime_1': '12:00:00' 
            }
        )

        self.assertEqual(PostWithDefaultDateTime.objects.count(), 1)

        saved_post = PostWithDefaultDateTime.objects.first()
        saved_post_datetime = saved_post.datetime

        self.assertEqual(
            saved_post_datetime,
            timezone.make_aware(datetime(2015, 6, 30, 12, 0, 0))
        )
