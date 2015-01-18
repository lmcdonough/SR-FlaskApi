from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    #ensure flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #make sure page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue('Please login' in response.data)

if __name__ == '__main__':
    unittest.main()
