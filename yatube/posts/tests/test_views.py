# deals/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from ..models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='test group',
            slug='test_slug',
            description='test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test text',
            group=cls.group
        )
        cls.group2 = Group.objects.create(
            title='test group2',
            slug='test_slug2',
            description='test description2',
        )

    def setUp(self):
        self.user = self.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_gruop_show_correct_context(self):
        index_list_pk = []
        response_index = self.authorized_client.get(reverse('posts:index'))
        index_object = response_index.context['page_obj']
        for i in index_object:
            pk_i = i.pk
            index_list_pk.append(pk_i)
        self.assertIn(self.post.pk, index_list_pk)
        group_list_pk = []
        response_group = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}
        ))
        group_object = response_group.context['page_obj']
        for i in group_object:
            pk_i = i.pk
            group_list_pk.append(pk_i)
        self.assertIn(self.post.pk, group_list_pk)
        profile_list_pk = []
        response_profile = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': self.post.author}
        ))
        profile_object = response_profile.context['page_obj']
        for i in profile_object:
            pk_i = i.pk
            profile_list_pk.append(pk_i)
        self.assertIn(self.post.pk, profile_list_pk)
        group_list_pk = []
        response_group = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group2.slug}
        ))
        group_object = response_group.context['page_obj']
        for i in group_object:
            pk_i = i.pk
            group_list_pk.append(pk_i)
        self.assertNotIn(self.post.pk, group_list_pk)

    def test_pages_uses_correct_template(self):
        pages_names_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in pages_names_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        index_author_0 = first_object.author
        index_text_0 = first_object.text
        ind = first_object.pk
        self.assertEqual(index_author_0, self.user)
        self.assertEqual(index_text_0, 'Test text')
        self.assertEqual(ind, 1)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}
        ))
        first_object = response.context['page_obj'][0]
        group_list_author_0 = first_object.author
        group_list_text_0 = first_object.text
        group_list_group_0 = first_object.group.title
        self.assertEqual(group_list_author_0, self.user)
        self.assertEqual(group_list_text_0, 'Test text')
        self.assertEqual(group_list_group_0, 'test group')

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': self.post.author}
        ))
        first_object = response.context['page_obj'][0]
        profile_author_0 = first_object.author
        profile_text_0 = first_object.text
        profile_group_0 = first_object.group.title
        self.assertEqual(profile_author_0, self.user)
        self.assertEqual(profile_text_0, 'Test text')
        self.assertEqual(profile_group_0, 'test group')

    def test_post_detail_pages_show_correct_context(self):
        response = (self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}
        )))
        self.assertEqual(response.context.get('post').author, self.user)
        self.assertEqual(response.context.get('post').text, 'Test text')

    def test_post_create_edit_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response1 = self.authorized_client.get(reverse('posts:post_create'))
        response2 = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': self.post.pk}
        ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response1.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response2.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_detail_pages_show_correct_context(self):
        response = (self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}
        )))
        self.assertEqual(response.context.get('post').author, self.user)
        self.assertEqual(response.context.get('post').text, 'Test text')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='test group',
            slug='test_slug',
            description='test description',
        )
        for i in range(13):
            cls.post = Post.objects.create(
                author=cls.user,
                text='Test text',
                group=cls.group
            )

    def test_index_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        # Проверка: на второй странице должно быть три поста.
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}
        ))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_records(self):
        # Проверка: на второй странице должно быть три поста.
        response = self.client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:profile',
            kwargs={'username': self.post.author}
        ))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_three_records(self):
        response = self.client.get(reverse(
            'posts:profile',
            kwargs={'username': self.post.author}) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)
