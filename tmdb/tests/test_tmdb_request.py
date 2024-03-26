import unittest

from .. import *


class TestTMDbRequest(unittest.TestCase):

    # tests for the get() method
    def test_response(self):
        """ Check whether the get() method returns a requests.models.Response instance. """

        response = Request.get()

        self.assertIsInstance(response, requests.models.Response)

    def test_home_page(self):
        """ Check whether the TMDb home page <www.themoviedb.org> can be retrieved. """

        response = Request.get()

        self.assertTrue(response)

    def test_search_page(self):
        """ Check whether the TMDb search page <www.themoviedb.org/search> can be retrieved. """

        response = Request.get(path="/search")

        self.assertTrue(response)

    def test_invalid_page(self):
        """ Check whether requesting invalid TMDb pages <www.themoviedb.org/invalid_error_xy> throws an exception. """

        self.assertRaises(Exception, lambda: Request.get(path="/invalid_error_xy"))

    # tests for the image() method
    def test_download_image(self):
        """ Check whether the image() method returns an io.BytesIO instance. """
        file_path = "/t/p/w94_and_h141_bestv2/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg"

        self.assertIsInstance(Request.image(file_path=file_path), io.BytesIO)

    def test_invalid_image(self):
        """ Check whether the image() method returns an io.BytesIO instance. """
        file_path = "/t/p/w94_and_h141_bestv2/invalid_image.jpg"

        self.assertRaises(Exception, lambda: Request.image(file_path=file_path))


if __name__ == '__main__':
    unittest.main()
