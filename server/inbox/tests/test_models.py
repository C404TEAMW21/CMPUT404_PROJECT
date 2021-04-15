from django.test import TestCase
from django.contrib.auth import get_user_model

from inbox.models import Inbox
from posts.models import Post
from posts.serializers import PostSerializer

class InboxTestCase(TestCase):
    def setUp(self):
        self.author_1 = get_user_model().objects.create_author(
            username='test001',
            password='testpwd'
        )

        self.author_2 = get_user_model().objects.create_author(
            username='test002',
            password='testpwd'
        )

        self.post_1 = Post.objects.create(
            title='Title',
            content='The actual content',
            author=self.author_1
        )

        self.post_2 = Post.objects.create(
            title='Title2',
            content='The actual content2',
            author=self.author_2
        )

    def create_inbox(self):
        self.inbox = Inbox.objects.create(
            author=self.author_1
        )
        return self.inbox

    def test_create_inbox(self):
        """Test creation of Inbox object"""
        inbox = self.create_inbox()
        self.assertTrue(isinstance(inbox, Inbox))

    def test_create_inbox_after_author(self):
        """Test automatic creation of Inbox object after creating Author"""
        self.assertEqual(Inbox.objects.count(), 2)
        inbox_count = Inbox.objects.filter(author=self.author_1).count()
        self.assertEqual(inbox_count, 1)
        inbox_count = Inbox.objects.filter(author=self.author_2).count()
        self.assertEqual(inbox_count, 1)

    def test_send_post_to_inbox(self):
        """Test adding a post to Inbox"""
        inbox = self.create_inbox()
        self.assertEqual(len(inbox.items), 0)

        post_1 = PostSerializer(self.post_1).data
        inbox.items.append(post_1)

        self.assertEqual(len(inbox.items), 1)

    def test_edit_post_after_sending(self):
        """Test editing Post after sending to Inbox"""
        inbox = self.create_inbox()
        post_1 = PostSerializer(self.post_1).data

        inbox.items.append(post_1)
        self.assertEqual(post_1, inbox.items[0])

        self.post_1.title = "Modified Title"
        modified_post_1 = PostSerializer(self.post_1).data

        self.assertEqual(post_1, inbox.items[0])
        self.assertNotEqual(modified_post_1, inbox.items[0])
        self.assertNotEqual(modified_post_1, post_1)

    def test_clear_inbox(self):
        """Test clearing items in Inbox"""
        inbox = self.create_inbox()
        post_1 = PostSerializer(self.post_1).data
        post_2 = PostSerializer(self.post_1).data

        inbox.items.append(post_1)
        inbox.items.append(post_2)
        self.assertEqual(len(inbox.items), 2)
        inbox.items.clear()
        self.assertEqual(len(inbox.items), 0)
