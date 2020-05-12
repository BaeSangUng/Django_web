from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
import time
from django.contrib.auth.models import User

class TestView(TestCase):
    def setUp(self):
        self.client = Client()      # django에서 제공하는 것중 하나로, Client 객체? 를 만들어서 Test할 수 있도록 함
        self.author_test = User.objects.create(
            username = 'admin',
            password = '1234'
        )
    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)     # 페이지가 잘 나오는지 확인

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        # Client를 새롭게 setUp한 것이기 때문에(test), 게시물이 없는 상태로 시작한다.
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('게시물 없음', soup.body.text)

        post_new = Post.objects.create(
            title='The First Post',
            content='Hello world',
            author=self.author_test,
            created=timezone.now()
        )

        self.assertGreater(Post.objects.count(), 0)


        # 생성 후에 refresh
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 페이지가 잘 나오는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body

        self.assertNotIn('게시물 없음', body.text)
        self.assertIn(post_new.title, body.text)

