import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from libs.gameplay import make_move, post_move, flatten_board


class TestGamePlay(TestCase):

    def setUp(self):
        response = self.client.get(reverse('tictic.index'))
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(str(response.content, encoding='utf8'))
        self.assertIn('gid', response_content.keys())
        self.gid = response_content['gid']

    def test_post_to_start(self):
        response = self.client.post(reverse('tictic.index'))
        self.assertEqual(response.status_code, 405)

    def test_get_to_move(self):
        response = self.client.get(reverse('tictic.move'))
        self.assertEqual(response.status_code, 405)

    def test_flatten_board(self):
        self.assertEqual(flatten_board([]), [])
        self.assertEqual(flatten_board([[1], [2, 3], [4]]), [1, 2, 3, 4])
        self.assertNotEqual(flatten_board([1, 2, [3, 4]]), [1, 2, 3, 4])
        self.assertIn('error', flatten_board([1, 2, [3, 4]]))
