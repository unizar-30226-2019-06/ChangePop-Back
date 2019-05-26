import os
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
        "mail": "alice1@yopmail.com",
        "pass": "pass",
        "phone": "666999222",
        "is_mod": False,
        "ban_reason": "Razon expulsion",
        "points": 0,
        "avatar": "http://images.com/235gadfg",
        "fnac": "2019-04-07",
        "dni": "123456789",
        "place": "Madrid",
        "desc": "Hi I am the fuking Alice",
        "token": "2sf78gsf68hsf5asfh68afh68a58fha68f"
    })
    user_data2 = json.dumps({
        "id": 0,
        "nick": "Alice2",
        "first_name": "Foo",
        "last_name": "Bar",
        "mail": "alice2@yopmail.com",
        "pass": "pass",
        "phone": "666999223",
        "is_mod": True,
        "ban_reason": "Razon expulsion",
        "points": 0,
        "avatar": "http://images.com/235gadfg",
        "fnac": "2019-04-07",
        "dni": "167666666",
        "place": "Madrid",
        "desc": "Hi I am the fuking Alice2",
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
        "first_name": "Foo",
        "last_name": "BarBar",
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
        "desc": "Hi I am the fuking Alice updated",
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
            self.assertIn("BarBar", str(r))  # Check sucessful update

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
        "price": 34,
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
        "price": 55,
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
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

    def test_add_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            product_id = r_json["message"]
            check = self.app.get('/product/' + str(product_id))
            self.assertIn('Zaragoza', str(check.get_json()["place"]))  # Check get info

    def test_update_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            product_id = r_json["message"]
            r_json = self.app.put('/product/' + str(product_id), data=self.prod_update,
                                  content_type='application/json').get_json()
            self.assertIn('updated', str(r_json))  # Check successful insertion

            check = self.app.get('/product/' + str(product_id))
            self.assertIn('Madrid', str(check.get_json()))  # Check get info

    def test_delete_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            product_id = r_json["message"]

            r_json = self.app.delete('/product/' + str(product_id)).get_json()
            self.assertIn('info', str(r_json))  # Check successful deletion

            r_json = self.app.get('/product/' + str(product_id)).get_json()
            self.assertIn('not found', str(r_json))  # Check successful deletion

    def test_list_search_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/product', data=self.prod_data, content_type='application/json')
            self.app.post('/product', data=self.prod_data2, content_type='application/json')

            r_json = self.app.get('/products').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful list

            r_json = self.app.get('/search/products?text=Molongo').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful search

            r_json = self.app.get('/products/' + str(self.user_id)).get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful list by user

    def test_list_search_product_adv(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/product', data=self.prod_data, content_type='application/json')
            self.app.post('/product', data=self.prod_data2, content_type='application/json')

            r_json = self.app.get('/products').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful list

            prod_search = json.dumps({
                "descript": "wonderful",
                "price_max": 35,
                "price_min": 33,
                "category": "Moda",
                "title": "Producto Molongo",
                "place": "Zaragoza"
            })
            r_json = self.app.get('/search/products/adv', data=prod_search, content_type='application/json').get_json()
            self.assertIn('Producto Molongo', str(r_json))  # Check successful search

    def test_follows_product(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            prod_id = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()[
                "message"]

            r_json = self.app.post('/product/' + str(prod_id) + '/follow').get_json()
            self.assertIn('follows', str(r_json))  # Check successful follow

            r_json = self.app.get('/user/follows').get_json()
            self.assertIn("Producto Molongo", str(r_json))  # Check the follows

            r_json = self.app.post('/product/' + str(prod_id) + '/unfollow').get_json()
            self.assertIn('unfollows', str(r_json))  # Check successful unfollow

            r_json = self.app.get('/user/follows').get_json()
            self.assertNotIn('Producto Molongo', str(r_json)) # Check the unfollows

    def test_ban_products(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.put('/user/' + str(self.user_id) + '/mod', data=UserDataBase.user_data,
                         content_type='application/json')

            prod_id = self.app.post('/product', data=self.prod_data, content_type='application/json').get_json()[
                "message"]

            ban_data = json.dumps({
                "ban_reason": "Ban for example"
            })
            r_json = self.app.put('/product/' + str(prod_id) + '/ban', data=ban_data,
                                  content_type='application/json').get_json()

            self.assertIn('banned', str(r_json))  # Check successful ban

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.delete('/user')


class ProductsBids(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create user and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            self.product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]

    def test_open_close_bid(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            data = json.dumps({"bid_until": "1999-12-24 23:45:10"})
            r_json = self.app.put('/product/' + str(self.product_id) + "/bidup", data=data,
                                  content_type='application/json').get_json()
            self.assertIn('1999-12-24 23:45:10', str(r_json))  # Check successful bid up

            r_json = self.app.get('/bids').get_json()
            self.assertIn('\'length\': ', str(r_json))  # Check bids

            r_json = self.app.get('/bid/' + str(self.product_id)).get_json()
            self.assertIn('1999-12-24 23:45:10', str(r_json))  # Check bid

            r_json = self.app.put('/product/' + str(self.product_id) + "/biddown", data=data,
                                  content_type='application/json').get_json()
            self.assertIn('finished', str(r_json))  # Check successful bid down

    def test_bid_prod(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            data = json.dumps({"bid_until": "2999-12-24 23:45:10"})
            self.app.put('/product/' + str(self.product_id) + "/bidup", data=data, content_type='application/json')

            data = json.dumps({"bid": "999.99"})
            r_json = self.app.post('/bid/' + str(self.product_id), data=data, content_type='application/json').get_json()
            self.assertIn('Successful bid with ' + str(999.99), str(r_json))  # Check bids

            r_json = self.app.get('/bid/' + str(self.product_id)).get_json()
            self.assertIn('999.99', str(r_json))  # Check bid with the bid

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.delete('/user')


class TradesProducts(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.seller_id = self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(self.seller_id) + '/mod')
            self.buyer_id = self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data2, content_type='application/json').get_json()[
                    "message"]

            # Post product
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]
            self.app.get('/logout')

    def test_trades(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create Trade from buyer
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            json_data = json.dumps({
                "seller_id": str(self.seller_id),
                "buyer_id": str(self.buyer_id),
                "product_id": str(self.product_id)
            })
            r_json = self.app.post('/trade', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful trade created

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

            r_json = self.app.get('/trades').get_json()
            self.assertIn('\'length\': ', str(r_json))  # Check list trades

            r_json = self.app.get('/trade/' + str(trade_id)).get_json()
            self.assertIn('\'seller_id\': ' + str(self.seller_id), str(r_json))  # Check get info

            r_json = self.app.put('/trade/' + str(trade_id) + '/confirm').get_json()
            self.assertIn('Success confirm', str(r_json))  # Check get info

            r_json = self.app.put('/trade/' + str(trade_id) + '/confirm').get_json()
            self.assertIn('Success unconfirm', str(r_json))  # Check get info

            r_json = self.app.put('/trade/' + str(trade_id) + '/confirm').get_json()
            self.assertIn('Success confirm', str(r_json))  # Check get info

            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.put('/trade/' + str(trade_id) + '/confirm').get_json()
            self.assertIn('Success confirm and close', str(r_json))  # Check get info

    def test_trades_delete(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create Trade from buyer
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            json_data = json.dumps({
                "seller_id": str(self.seller_id),
                "buyer_id": str(self.buyer_id),
                "product_id": str(self.product_id)
            })
            r_json = self.app.post('/trade', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful trade created

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
            self.assertIn('\'seller_id\': ' + str(self.seller_id), str(r_json))  # Check get info

            self.app.put('/trade/' + str(trade_id) + '/confirm').get_json()

            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.put('/trade/' + str(trade_id) + '/delete').get_json()
            self.assertIn('Success delete', str(r_json))  # Check get info

            r_json = self.app.get('/trades').get_json()
            self.assertNotIn('22.9', str(r_json))  # Check get info

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Post test
            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.app.delete('/user/' + str(self.buyer_id))
            self.app.delete('/user/' + str(self.seller_id))


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

    def test_messages(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Post product
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]
            self.app.get('/logout')

            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            json_data = json.dumps({
                "seller_id": str(self.seller_id),
                "buyer_id": str(self.buyer_id),
                "product_id": str(self.product_id)
            })
            trade_id = self.app.post('/trade', data=json_data, content_type='application/json').get_json()["message"]

            json_data = json.dumps({
                "body": "HELLO THERE!"
            })
            r_json = self.app.post('/msgs/' + str(trade_id), data=json_data, content_type='application/json').get_json()
            self.assertIn('Message created', str(r_json))  # Check successful creation

            self.app.get('/logout')

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "body": "HELLO HERE!"
            })
            r_json = self.app.post('/msgs/' + str(trade_id), data=json_data, content_type='application/json').get_json()
            self.assertIn('Message created', str(r_json))  # Check successful creation

            r_json = self.app.get('/msgs/' + str(trade_id)).get_json()
            self.assertIn('HELLO HERE!', str(r_json))  # Check successful get

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.get('/logout').get_json()
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json').get_json()
            self.app.delete('/user/' + str(self.buyer_id)).get_json()
            self.app.delete('/user/' + str(self.seller_id)).get_json()


class Notifications(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(self.user_id) + '/mod')

    def test_delete_all_notifications(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "user_id": self.user_id,
                "product_id": 0,
                "category": "null",
                "text": "Nuevo producto en categoria e interés"

            })
            self.app.post('/notification', data=json_data, content_type='application/json').get_json()

            json_data = json.dumps({
                "user_id": self.user_id,
                "product_id": 0,
                "category": "null",
                "text": "Otra cosa"

            })
            self.app.post('/notification', data=json_data, content_type='application/json').get_json()

            json_data = json.dumps({
                "user_id": self.user_id,
                "product_id": 0,
                "category": "null",
                "text": "Otra cosa 2"

            })
            self.app.post('/notification', data=json_data, content_type='application/json').get_json()

            r_json = self.app.delete('/notifications').get_json()
            self.assertIn('Successful delete', str(r_json))  # Check successful

            r_json = self.app.get('/notifications').get_json()
            self.assertIn('0', str(r_json))  # Check successful get 0 elements

    def test_create_get_notification(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "user_id": self.user_id,
                "product_id": 0,
                "category": "null",
                "text": "Otra cosa 2"

            })
            r_json = self.app.post('/notification', data=json_data, content_type='application/json').get_json()
            self.assertIn('Notification pushed', str(r_json))  # Check successful creation

            r_json = self.app.get('/notifications').get_json()
            self.assertIn('Otra cosa', str(r_json))  # Check successful get

    def test_follow_notify(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            user_2 = \
                self.app.post('/user', data=UserDataBase.user_data2, content_type='application/json').get_json()[
                    "message"]

            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            r_json = self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()
            product_id = r_json["message"]

            # Follow
            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.app.post('/product/' + str(product_id) + '/follow')

            # Update
            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')
            r_json = self.app.put('/product/' + str(product_id), data=ProductDataBase.prod_update,
                                  content_type='application/json').get_json()

            # Check
            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            r_json = self.app.get('/notifications').get_json()
            self.assertIn('precio', str(r_json))  # Check successful get

            r_json = self.app.delete('/user/' + str(user_2)).get_json()


    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.delete('/user')


class UploadFiles(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]

    def test_upload(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            f = open('./test/jake.jpg', 'rb')

            data = {'file': f}
            r_json = self.app.post('/upload', content_type='multipart/form-data', data=data).get_json()
            file_url = r_json["message"]
            f.close()

            self.assertIn('info', str(r_json))  # Check successful upload

            r = self.app.get(file_url)
            self.assertIn("[200 OK]", str(r))

            r.close()

            file = file_url.split('/')[2]
            os.remove("./images/" + file)

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.delete('/user')


class Reports(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(self.user_id) + '/mod')

    def test_new_report(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "user_id": self.user_id,
                "reason": "Porque si y punto en boca"
            })
            r_json = self.app.post('/report', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful upload

            product_id = self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()["message"]
            json_data = json.dumps({
                "user_id": self.user_id,
                "product_id": product_id,
                "reason": "Porque si y punto en boca otra vez"
            })
            r_json = self.app.post('/report', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful upload

    def test_get_reports(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "user_id": self.user_id,
                "reason": "Porque si y punto en boca"
            })
            self.app.post('/report', data=json_data, content_type='application/json')

            r_json = self.app.get('/reports').get_json()
            self.assertIn('Porque si y punto en boca', str(r_json))  # Check successful get

    def test_delete_report(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "user_id": self.user_id,
                "reason": "Porque si y punto en boca"
            })
            id = self.app.post('/report', data=json_data, content_type='application/json').get_json()["message"]

            r_json = self.app.delete('/report/'+str(id)).get_json()
            self.assertIn('deleted', str(r_json))  # Check successful upload

            r_json = self.app.get('/reports').get_json()
            self.assertNotIn('Porque si y punto en boca', str(r_json))

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.delete('/user')


class Interest(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(self.user_id) + '/mod')

    def test_delete_all_interests(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            json_data = json.dumps({
                "user_id": self.user_id,
                "product_id": 0,
                "category": "null",
                "text": "Nuevo producto en categoria e interés"

            })
            self.app.post('/categories/interest', data=json_data, content_type='application/json').get_json()

            json_data = json.dumps({
                "list": ["moda"]

            })
            r_json = self.app.post('/categories/interest', data=json_data, content_type='application/json').get_json()

            json_data = json.dumps({
                "list":["electronica"]
            })

            self.app.post('/categories/interest', data=json_data, content_type='application/json').get_json()

            self.app.get('/categories/interest').get_json()

            r_json = self.app.delete('/categories/interest', data=json_data, content_type='application/json' ).get_json()
            self.assertIn('Successful delete', str(r_json))  # Check successful

            r_json = self.app.get('/categories/interest').get_json()
            self.assertIn('0', str(r_json))  # Check successful get 0 elements

    def test_get_categories(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.get('/categories').get_json()
            self.assertIn('Moda', str(r_json))  # Check successful upload

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.delete('/user')


class PaymentsTest(unittest.TestCase):

    def setUp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app = webapp.app.test_client()
            self.app.testing = True

            # Create users and login
            self.modder = \
                self.app.post('/user', data=UserDataBase.user_data, content_type='application/json').get_json()[
                    "message"]
            self.app.put('/user/' + str(self.modder) + '/mod')
            self.user = self.user_id = \
                self.app.post('/user', data=UserDataBase.user_data2, content_type='application/json').get_json()[
                    "message"]

            # Post product
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')
            self.product_id = \
                self.app.post('/product', data=ProductDataBase.prod_data, content_type='application/json').get_json()[
                    "message"]
            self.app.get('/logout')

    def test_new_pay(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create Trade from buyer
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            iban = "ES809999123125412535"
            json_data = json.dumps({
                "amount": 9.99,
                "iban": iban,
                "boost_date": "1999-12-24",
                "product_id": int(self.product_id)
            })
            r_json = self.app.post('/payment', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful pay created

    def test_delete_pay(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create Trade from buyer
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            iban = "ES809999123125412535"
            json_data = json.dumps({
                "amount": 9.99,
                "iban": iban,
                "boost_date": "1999-12-24",
                "product_id": int(self.product_id)
            })
            r_json = self.app.post('/payment', data=json_data, content_type='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful pay created

            pay_id = r_json["message"]

            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.put('/payment/check/' + str(pay_id), data=json_data, content_type='application/json').get_json()
            self.assertIn('deleted', str(r_json))  # Check deleted offer

            r_json = self.app.put('/payment/check/' + str(pay_id), data=json_data,
                                  content_type='application/json').get_json()
            self.assertIn('not found', str(r_json))  # Check deleted offer

    def test_list_pays(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Create Trade from buyer
            self.app.post('/login', data=UserDataBase.user2_login, content_type='application/json')

            iban = "ES809999123125412535"
            json_data = json.dumps({
                "amount": 9.99,
                "iban": iban,
                "boost_date": "1999-12-24",
                "product_id": int(self.product_id)
            })
            self.app.post('/payment', data=json_data, content_type='application/json').get_json()

            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')

            r_json = self.app.get('/payments').get_json()
            self.assertIn(iban, str(r_json))  # Check deleted offer

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            # Post test
            self.app.get('/logout')
            self.app.post('/login', data=UserDataBase.user_login, content_type='application/json')
            self.app.delete('/user/' + str(self.user))
            self.app.delete('/user/' + str(self.modder))

if __name__ == "__main__":
    unittest.main()
