from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post

class PostTest(TestCase):
    def test_create_post(self):
        # Create the post
        post = Post()

        # Set the attributes
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()

        # Save it
        post.save()

        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Check attributes
        self.assertEquals(only_post.title, 'My first post')
        self.assertEquals(only_post.text, 'This is my first blog post')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        self.assertEquals(only_post.pub_date.month, post.pub_date.month)
        self.assertEquals(only_post.pub_date.year, post.pub_date.year)
        self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)

class AdminTest(LiveServerTestCase):
    fixtures = ['blog_users.json']
        
    def setUp(self):
        self.client = Client()
        
    def test_login(self):
        # Get login page
        response = self.client.get('/admin/')
        
        # Check response code
        self.assertEquals(response.status_code, 200)
        
        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)
        
        # Log the user in
        self.client.login(username='bob', password="password")
        
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)
            
    def test_logout(self):
        # Log in
        self.client.login(username='bob', password="password")
        
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)
        
        # Log out
        self.client.logout()
        
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        
        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)
            
    def test_create_post(self):
        # Log in
        self.client.login(username='bob', password="password")
        
        # Check response code
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEquals(response.status_code, 200)
        
        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', {
        	'title': 'My first post',
        	'text': 'This is my first post',
        	'pub_date_0': '2013-12-28',
        	'pub_date_1': '22:00:04'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)
        
        # Check added successfully
        self.assertTrue('added successfully' in response.content)
        
        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
            
    def test_edit_post(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()
    
        # Log in
        self.client.login(username='bob', password="password")
    
        # Edit the post
        response = self.client.post('/admin/blogengine/post/1/', {
            'title': 'My second post',
            'text': 'This is my second blog post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)
    
        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)
    
        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My second post')
        self.assertEquals(only_post.text, 'This is my second blog post')
                
    def test_delete_post(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()
    
        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
    
        # Log in
        self.client.login(username='bob', password="password")
    
        # Delete the post
        response = self.client.post('/admin/blogengine/post/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
    
        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)
    
        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

class PostViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content)

        # Check the post text is in the response
        self.assertTrue(post.text in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)        		