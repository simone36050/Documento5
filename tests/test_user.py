from unittest import TestCase, main
from requests import get
from datetime import datetime as Datetime, timedelta as Timedelta

URL = 'https://mechahome.simone36050.it/'
# URL = 'http://localhost:5000/'

class GetUserTests(TestCase):
    def test_correct(self):
        try:
            response = get(URL + '/api/user/1')
            self.assertEqual(response.status_code, 200)

            output = response.json()
            self.assertEqual(output, {
               "email": "hello@example.com",
                "firstname": "Hello",
                "lastname": "World",
                "telephone": "3052268512",
                "username": "hello.world"
            })
            
        except Exception:
            self.fail("Get user ha lanciato un'eccezione")


    def test_missing(self):
        try:
            response = get(URL + '/api/user/5')
            self.assertEqual(response.status_code, 404)
            
        except Exception:
            self.fail("Get user ha lanciato un'eccezione")

    # requisito non funzionale 5.1
    def test_timeout(self):
        start = Datetime.now()

        # run code
        get(URL + '/api/user/2')

        end = Datetime.now()

        self.assertLessEqual(end - start, Timedelta(seconds=1.5))

if __name__ == '__main__':
    main()
    # GetUserTests().test_correct()
