from django.test import TestCase
from django.urls import reverse


class BlogIndexViewTest(TestCase):
    def test_index_view_status_code(self):
        url = reverse('blog-home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
