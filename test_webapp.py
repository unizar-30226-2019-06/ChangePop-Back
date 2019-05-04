import unittest
import warnings
from flask import json
import webapp
from config import TestingConfig, Config


class HomeViewTest(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        home = self.app.get('/')
        self.assertIn('Home Page', str(home.data))


class UserDataBase(unittest.TestCase):
    tmp_user_id = -1
    user_data = json.dumps({
        "id": 0,
        "nick": "Alice",
        "first_name": "Foo",
        "last_name": "Bar",
        "mail": "mail@email.com",
        "pass": "pass",
        "phone": "666999222",
        "is_mod": False,
        "ban_reason": "Razon expulsion",
        "points": 0,
        "avatar": "http://images.com/235gadfg",
        "fnac": "2019-04-07",
        "dni": "123456789",
        "place": "Madrid",
        "token": "2sf78gsf68hsf5asfh68afh68a58fha68f"
    })
    user_data2 = json.dumps({
        "id": 0,
        "nick": "Alice2",
        "first_name": "Foo",
        "last_name": "Bar",
        "mail": "mail2@email.com",
        "pass": "pass",
        "phone": "666999223",
        "is_mod": True,
        "ban_reason": "Razon expulsion",
        "points": 0,
        "avatar": "http://images.com/235gadfg",
        "fnac": "2019-04-07",
        "dni": "167666666",
        "place": "Madrid",
        "token": "2sf78gsf68hsf5asfh68afh6gha68f"
    })
    user_login = json.dumps({
        "nick": "Alice",
        "pass": "pass",
        "remember": True
    })
    user2_login = json.dumps({
        "nick": "Alice2",
        "pass": "pass",
        "remember": True
    })

    user_update = json.dumps({
        "nick": "Alice",
        "first_name": "FooFoo",
        "last_name": "Bar",
        "mail": "mail@email.com",
        "pass": "pass",
        "phone": "666999222",
        "is_mod": True,
        "ban_reason": "Razon expulsion",
        "points": 0,
        "avatar": "http://images.com/235gadfg",
        "fnac": "2019-04-07",
        "dni": "123456789",
        "place": "Madrid",
        "token": "2sf78gsf68hsf5asfh68afh68a58fha68f",
        "pass_hash": "s32uh5423j5h23jh52jh35"
    })

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_add_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/user', data=self.user_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            user_id = r_json["message"]
            self.__class__.tmp_user_id = user_id

            check = self.app.get('/profile/Alice')
            self.assertIn('666999222', str(check.get_json()))  # Check get info

            self.app.post('/login', data=self.user_login, content_type='application/json')
            self.app.delete('/user')

    def test_session_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/user', data=self.user_data, content_type='application/json')

            r_json = self.app.post('/login', data=self.user_login, content_type='application/json').get_json()
            self.assertIn('Alice', str(r_json))  # Check successful login

            r_json = self.app.get('/user').get_json()
            self.assertIn('Alice', str(r_json))  # Check get logged user info

            r_json = self.app.get('/logout').get_json()  # Logout
            self.assertIn('out', str(r_json))  # Check successful

            r_json = self.app.get('/user').get_json()  # Try get my info
            self.assertIn('Not logged in', str(r_json))  # Check successful

            self.app.post('/login', data=self.user_login, content_type='application/json')
            self.app.delete('/user')

    def test_update_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            id = self.app.post('/user', data=self.user_data, content_type='application/json').get_json()["message"]
            self.app.post('/login', data=self.user_login, content_type='application/json')

            self.app.post('/login', data=self.user_login, content_type='application/json')  # Login to set the session

            r_json = self.app.put('/user', data=self.user_update, content_type='application/json').get_json()
            msg = r_json["message"]
            self.assertIn(str(id), msg)  # Check successful update

            r = self.app.get('/user').get_json()
            self.assertIn("FooFoo", str(r))  # Check sucessful update

            self.app.delete('/user')

    def test_delete_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            id = self.app.post('/user', data=self.user_data, content_type='application/json').get_json()["message"]
            self.app.post('/login', data=self.user_login, content_type='application/json')

            r_json = self.app.delete('/user').get_json()
            msg = r_json["message"]
            self.assertIn(str(id), msg)  # Check successful deletion

            r = self.app.post('/login', data=self.user_login, content_type='application/json').get_json()
            self.assertIn("User not found", str(r))  # Check unsuccessful login

    def test_mod_users(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/user', data=self.user_data,
                                   content_type='application/json').get_json()  # User created
            user_id = r_json["message"]
            self.__class__.tmp_user_id = user_id

            r_json = self.app.put('/user/' + str(user_id) + '/mod').get_json()
            self.assertIn('Ok', str(r_json))  # Check set mod

            self.app.post('/login', data=self.user_login, content_type='application/json')  # Login to set the session

            r_json = self.app.get('/user/' + str(user_id)).get_json()
            self.assertIn('Alice', str(r_json))  # Check get user info

            r_json = self.app.put('/user/' + str(user_id), data=self.user_update,
                                  content_type='application/json').get_json()
            self.assertIn('updated', str(r_json))  # Check update user info

            r_json = self.app.delete('/user/' + str(user_id)).get_json()
            self.assertIn('deleted', str(r_json))  # Check delete user info

    def test_ban_users(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/user', data=self.user_data,
                                   content_type='application/json').get_json()  # User created
            mod_user_id = r_json["message"]

            r_json = self.app.post('/user', data=self.user_data2,
                                   content_type='application/json').get_json()  # User created
            ban_user_id = r_json["message"]

            self.app.put('/user/' + str(mod_user_id) + '/mod')

            self.app.post('/login', data=self.user_login, content_type='application/json')  # Login to set the session

            ban_data = json.dumps({
                "ban_reason": "Ban for example",
                "ban_until": "9999-04-13"
            })
            r_json = self.app.put('/user/' + str(ban_user_id) + '/ban', data=ban_data,
                                  content_type='application/json').get_json()
            self.assertIn('(' + str(ban_user_id) + ') banned', str(r_json))  # Check the ban

            r_json = self.app.post('/login', data=self.user2_login,
                                   content_type='application/json').get_json()  # Login to check
            self.assertIn("Ban for example", str(r_json))

            self.app.delete('/user/' + str(ban_user_id))
            self.app.delete('/user/' + str(mod_user_id))

    def test_list_search_users(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            id1 = self.app.post('/user', data=self.user_data, content_type='application/json').get_json()["message"]
            id2 = self.app.post('/user', data=self.user_data2, content_type='application/json').get_json()["message"]
            self.app.put('/user/' + str(id2) + '/mod')

            r_json = self.app.get('users').get_json()
            self.assertIn("\'length\'", str(r_json))

            r_json = self.app.get('/search/users?text=Alice').get_json()
            self.assertIn("\'length\'", str(r_json))

            self.app.post('/login', data=self.user2_login, content_type='application/json')
            self.app.delete('/user/' + str(id1)).get_json()
            self.app.delete('/user/' + str(id2)).get_json()


class ProductDataBase(unittest.TestCase):
    user_id: int = 1
    prod_data = json.dumps({
        "descript": "This product is wonderful",
        "price": 0,
        "categories": [
            "Moda"
        ],
        "title": "Producto Molongo",
        "bid_date": "1999-12-24 23:45:11",
        "boost_date": "1999-12-24 23:45:12",
        "visits": 0,
        "followers": 0,
        "publish_date": "2019-04-07",
        "main_img": "http://images.com/123af3",
        "photo_urls": [
            "http://images.com/123af3"
        ],
        "place": "Zaragoza",
        "is_removed": True,
        "ban_reason": "Razon Baneo"
    })

    prod_data2 = json.dumps({
        "descript": "This product is wonderful",
        "price": 0,
        "categories": [
            "Moda"
        ],
        "title": "Producto Molongo2",
        "bid_date": "1999-12-24 23:45:11",
        "boost_date": "1999-12-24 23:45:12",
        "visits": 0,
        "followers": 0,
        "publish_date": "2019-04-07",
        "main_img": "http://images.com/123af3",
        "photo_urls": [
            "http://images.com/123af3"
        ],
        "place": "Zaragoza",
        "is_removed": True,
        "ban_reason": "Razon Baneo"
    })

    prod_update = json.dumps({
        "descript": "This product is wonderful",
        "price": 0,
        "categories": [
            "Moda", "Complementeos"
        ],
        "title": "Producto Molongo",
        "bid_date": "1999-12-24 22:45:13",
        "main_img": "http://images.com/123af3",
        "photo_urls": [
            "http://images.com/123af3"
        ],
        "place": "Madrid"
    })

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_add_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            product_id = r_json["message"]
            check = self.app.get('/product/' + str(product_id))
            self.assertIn('Zaragoza', str(check.get_json()["place"]))  # Check get info

            self.app.delete('/user')

    def test_update_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            product_id = r_json["message"]
            r_json = self.app.put('/product/' + str(product_id), data=self.prod_update,
                                  content_type='application/json').get_json()
            self.assertIn('updated', str(r_json))  # Check successful insertion

            check = self.app.get('/product/' + str(product_id))
            self.assertIn('Madrid', str(check.get_json()))  # Check get info

            self.app.delete('/user')

    def test_delete_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            product_id = r_json["message"]

            r_json = self.app.delete('/product/' + str(product_id)).get_json()
            self.assertIn('info', str(r_json))  # Check successful deletion

            r_json = self.app.get('/product/' + str(product_id)).get_json()
            self.assertIn('not found', str(r_json))  # Check successful deletion

            self.app.delete('/user')

    def test_list_search_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            self.app.post('/product', data=self.prod_data, content_type='application/json')
            self.app.post('/product', data=self.prod_data2, content_type='application/json')

            r_json = self.app.get('/products').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful list

            r_json = self.app.get('/search/products?text=Molongo').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful search

            r_json = self.app.get('/products/' + str(self.user_id)).get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful list by user

            self.app.delete('/user')

    def test_follows_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            prod_id = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()[
                "message"]

            r_json = self.app.post('/product/' + str(prod_id) + '/follow').get_json()
            self.assertIn('follows', str(r_json))  # Check successful follow

            r_json = self.app.get('/user/follows').get_json()
            self.assertIn("Producto Molongo", str(r_json))  # Check the follows

            r_json = self.app.post('/product/' + str(prod_id) + '/unfollow').get_json()
            self.assertIn('unfollows', str(r_json))  # Check successful unfollow

            r_json = self.app.get('/user/follows').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check the follows

            self.app.delete('/user')

    def test_ban_products(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/user', data=UserDataBase.user_data,
                                   content_type='application/json').get_json()  # User created
            mod_user_id = r_json["message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.app.put('/user/' + str(mod_user_id) + '/mod', data=UserDataBase.user_data,
                         content_type='application/json')

            prod_id = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()[
                "message"]

            ban_data = json.dumps({
                "ban_reason": "Ban for example"
            })
            r_json = self.app.put('/product/' + str(prod_id) + '/ban', data=ban_data,
                                  content_type='application/json').get_json()

            self.assertIn('banned', str(r_json))  # Check successful ban

            self.app.delete('/user')


class ProductsBids(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_open_close_bid(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]

            data = json.dumps({"bid_until": "1999-12-24 23:45:10"})
            r_json = self.app.put('/product/' + str(product_id) + "/bidup", data=data,
                                  content_type='application/json').get_json()
            self.assertIn('1999-12-24 23:45:10', str(r_json))  # Check successful bid up

            r_json = self.app.get('/bids').get_json()
            self.assertIn('\'length\': ', str(r_json))  # Check bids

            r_json = self.app.get('/bid/' + str(product_id)).get_json()
            self.assertIn('1999-12-24 23:45:10', str(r_json))  # Check bid

            r_json = self.app.put('/product/' + str(product_id) + "/biddown", data=data,
                                  content_type='application/json').get_json()
            self.assertIn('finished', str(r_json))  # Check successful bid down

            self.app.delete('/user')

    def test_bid_prod(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]

            data = json.dumps({"bid_until": "2999-12-24 23:45:10"})
            self.app.put('/product/' + str(product_id) + "/bidup", data=data, content_type='application/json')

            data = json.dumps({"bid": "999.99"})
            r_json = self.app.post('/bid/' + str(product_id), data=data, content_type='application/json').get_json()
            self.assertIn('Successful bid with ' + str(999.99), str(r_json))  # Check bids

            r_json = self.app.get('/bid/' + str(product_id)).get_json()
            self.assertIn('999.99', str(r_json))  # Check bid with the bid

            self.app.delete('/user')


class TradesProducts(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_trades(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create users and login
            seller_id = self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(seller_id) + '/mod')
            buyer_id = self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data2, content_type='application/json').get_json()[
                    "message"]

            # Post product
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]
            self.app.get('/logout')

            # Create Trade from buyer
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            json_data = json.dumps({
                "seller_id": str(seller_id),
                "buyer_id": str(buyer_id),
                "product_id": str(product_id)
            })
            r_json = self.app.post('/trade', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check bid with the bid

            trade_id = r_json["message"]

            json_data = json.dumps({
                "price": "99.9",
                "products": [],
            })
            r_json = self.app.post('/trade/' + str(trade_id) + '/offer', data=json_data,
                                   content_type='application/json').get_json()
            self.assertIn('Successful new offer', str(r_json))  # Check create offer

            json_data = json.dumps({
                "price": "22.9",
                "products": [],
            })
            r_json = self.app.put('/trade/' + str(trade_id) + '/offer', data=json_data,
                                  content_type='application/json').get_json()
            self.assertIn('Successful offer update', str(r_json))  # Check update

            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.get('/trades').get_json()
            self.assertIn('\'length\': ', str(r_json))  # Check list trades

            r_json = self.app.get('/trade/' + str(trade_id)).get_json()
            self.assertIn('\'seller_id\': ' + str(seller_id), str(r_json))  # Check get info

            # Post test

            self.app.delete('/user/' + str(buyer_id))
            self.app.delete('/user/' + str(seller_id))


class CommentsAndMessages(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.seller_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(self.seller_id) + '/mod')
            self.buyer_id = \
                self.app.post('/user', data=UserDataBase.user_data2, content_type='application/json').get_json()[
                    "message"]

    def test_comments(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            json_data = json.dumps({
                "body": "ESRES UN CRACK",
                "points": "3",
            })
            r_json = self.app.post('/comment/' + str(self.seller_id), data=json_data,
                                   content_type='application/json').get_json()
            self.assertIn('comment created', str(r_json))  # Check successful creation

            r_json = self.app.get('/comments/' + str(self.seller_id)).get_json()
            self.assertIn('ESRES UN CRACK', str(r_json))  # Check successful get

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.app.delete('/user/' + str(self.buyer_id))
            self.app.delete('/user/' + str(self.seller_id))


if __name__ == "__main__":
    unittest.main()
