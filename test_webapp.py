import unittest
import warnings

from flask import json

import webapp


# from webapp import app
# from webapp import home


class HomeViewTest(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        home = self.app.get('/')
        self.assertIn('Home Page', str(home.data))


class UserDataBase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_add_user(self):
        data = {
            "id": 0,
            "nick": "Alice",
            "first_name": "Foo",
            "last_name": "Bar",
            "mail": "mail@email.com",
            "pass_hash": "2sf78gsf68hsf5asfh68afh68a58fha68f",
            "phone": "666999222",
            "is_mod": True,
            "ban_reason": "Razon expulsion",
            "points": 0,
            "avatar": "http://images.com/235gadfg",
            "fnac": "2019-04-07",
            "dni": "123456789",
            "place": "Madrid",
            "token": "2sf78gsf68hsf5asfh68afh68a58fha68f"
        }

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            data_send = json.dumps(data)
            response = self.app.post('/user', data=data_send, mimetype='application/json')

            r_json = response.get_json()
            self.assertIn('info', str(response.get_json()))  # Check successful insertion

            user_id = r_json["message"]
            ProductDataBase.user_id = user_id
            check = self.app.get('/user/' + str(user_id))
            self.assertIn('666999222', str(check.get_json()))  # Check get info


class ProductDataBase(unittest.TestCase):
    user_id: int = 1

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_add_product(self):
        data = {
            "id": 0,
            "descript": "This product is wonderful",
            "user_id": self.user_id,
            "price": 0,
            "categories": [
                "Moda"
            ],
            "title": "Producto Molongo",
            "bid": "2019-04-07",
            "boost_date": "2019-04-07",
            "visits": 0,
            "followers": 0,
            "publish_date": "2019-04-07",
            "photo_urls": [
                "http://images.com/123af3"
            ],
            "place": "Zaragoza",
            "is_removed": True,
            "ban_reason": "Razon Baneo"
        }

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            data_send = json.dumps(data)
            response = self.app.post('/product', data=data_send, mimetype='application/json')

            r_json = response.get_json()
            self.assertIn('info', str(response.get_json()))  # Check successful insertion

            product_id = r_json["message"]
            check = self.app.get('/product/' + str(product_id))
            self.assertIn('Zaragoza', str(check.get_json()))  # Check get info


if __name__ == "__main__":
    unittest.main()
