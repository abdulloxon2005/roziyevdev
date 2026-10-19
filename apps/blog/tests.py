from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from apps.blog.models import BlogCategory, Tag, Post, Comment


class BlogTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="author_test",
            email="author_test@example.com",
            password="password123"
        )
        self.category = BlogCategory.objects.create(name="Backend", slug="backend")
        self.tag = Tag.objects.create(name="Python", slug="python")
        self.post = Post.objects.create(
            title="Django REST Tips",
            slug="django-rest-tips",
            author=self.user,
            category=self.category,
            summary="Tips for DRF",
            content="## Markdown Heading\n\nSome great tips here.",
            is_published=True
        )
        self.post.tags.add(self.tag)

    def test_blog_list_and_search(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django REST Tips")

        # Kategoriya bo'yicha filter
        response = self.client.get(reverse('blog_list'), {'category': 'backend'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django REST Tips")

        # Qidiruv
        response = self.client.get(reverse('blog_list'), {'search': 'Tips'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django REST Tips")

    def test_blog_detail_and_views_count(self):
        initial_views = self.post.views_count
        response = self.client.get(reverse('blog_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django REST Tips")
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial_views + 1)

    def test_comment_submission(self):
        response = self.client.post(
            reverse('blog_comment', args=[self.post.slug]),
            {
                'author_name': 'Ali',
                'content': 'Ajoyib maqola, rahmat!'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first().content, 'Ajoyib maqola, rahmat!')
