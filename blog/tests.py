from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User

def create_post(title, content, author):
    post_new = Post.objects.create(
        title=title,
        content=content,
        author=author,
        created=timezone.now()
    )
    return post_new

class TestView(TestCase):
    def setUp(self):
        self.client = Client()      # django에서 제공하는 것중 하나로, Client 객체? 를 만들어서 Test할 수 있도록 함
        self.author_test = User.objects.create(
            username = 'admin',
            password = '1234'
        )

    def check_navbar(self, soup):
        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)     # 페이지가 잘 나오는지 확인

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        self.check_navbar(soup)

        # Client를 새롭게 setUp한 것이기 때문에(test), 게시물이 없는 상태로 시작한다.
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('게시물 없음', soup.body.text)

        post_new = create_post(
            title='The First Post',
            content='Hello world',
            author=self.author_test,
        )

        self.assertGreater(Post.objects.count(), 0)


        # 생성 후에 refresh
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 페이지가 잘 나오는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body

        self.assertNotIn('게시물 없음', body.text)
        self.assertIn(post_new.title, body.text)

        # read more buttton Test
        post_new_read_more_btn = body.find('a', id='read-more-post-{}'.format(post_new.pk))
        print(post_new_read_more_btn['href'])
        self.assertEqual(post_new_read_more_btn['href'], post_new.get_absolute_url())

    def test_post_detail(self):
        post_new = create_post(
            title='The First Post',
            content='Hello world',
            author=self.author_test,
        )

        self.assertGreater(Post.objects.count(), 0)
        post_new_url = post_new.get_absolute_url()
        self.assertEqual(post_new_url, '/blog/{}/'.format(post_new.pk))

        response = self.client.get(post_new_url)
        self.assertEqual(response.status_code, 200)  # 페이지가 잘 나오는지 확인

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, '{} - Blog'.format(post_new.title))

        self.check_navbar(soup)

        body = soup.body
        main_div = body.find('div', id='main_div')
        self.assertIn(post_new.title, main_div.text)
        self.assertIn(post_new.author.username, main_div.text)

        self.assertIn(post_new.content, main_div.text)