CREATE TABLE Categories
(
   cat_name    VARCHAR(255)       PRIMARY KEY
);

CREATE TABLE Users
(
   id          INTEGER        PRIMARY KEY,
   last_name   VARCHAR(255)       NOT NULL,
   nick        VARCHAR(255)       NOT NULL,
   first_name  VARCHAR(255)       NOT NULL,
   ban_reason        VARCHAR(255),
   points      FLOAT          NOT NULL,
   mail           VARCHAR(255)   UNIQUE   NOT NULL,
   is_mod        BOOLEAN        NOT NULL,
   dni         VARCHAR(255)       UNIQUE NOT NULL,
   avatar      VARCHAR(255)       NOT NULL,
   fnac        DATE           NOT NULL,
   place       VARCHAR(255)       NOT NULL,
   pass_hash   VARCHAR(255)       NOT NULL,
   INDEX       (nick ASC),
   INDEX       (first_name ASC),
   token       VARCHAR(255),
   time_token  TIMESTAMP,
   ts_create   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   ts_edit     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Products
(
   id             INTEGER        PRIMARY KEY,
   title          VARCHAR(255)       NOT NULL,
   descript       VARCHAR(255)       NOT NULL,
   price          FLOAT          NOT NULL,
   publish_date   TIMESTAMP 		DEFAULT CURRENT_TIMESTAMP NOT NULL,
   ban_reason          VARCHAR(255),
   bid_date           DATE,
   num_visits     INTEGER        NOT NULL,
   boost_date       DATE,
   followers      INTEGER        NOT NULL,
   is_removed       BOOLEAN			 NOT NULL,
   place          VARCHAR(255)       NOT NULL,
   user_id        INTEGER        NOT NULL,
   FOREIGN KEY (user_id) REFERENCES Users(id),
   INDEX          (title ASC),
   INDEX          (publish_date ASC),
   INDEX          (boost_date ASC),
   ts_edit     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Images
(
   iamge_url      VARCHAR(255),
   product_id     INTEGER,
   PRIMARY KEY (iamge_url,product_id),
   FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Reports
(
   id             INTEGER        PRIMARY KEY,
   reason         VARCHAR(255)       NOT NULL,
   user_id        INTEGER        NOT NULL,
   product_id     INTEGER, 
   report_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   
   FOREIGN KEY (user_id) REFERENCES Users(id),
   FOREIGN KEY (product_id) REFERENCES Products(id),
   INDEX          (report_date ASC)
);

CREATE TABLE Payments
(
   id             INTEGER        PRIMARY KEY,
   pay_date       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   amount         FLOAT          NOT NULL,
   iban           VARCHAR(255)       NOT NULL,
   boost_date     DATE           NOT NULL,
   product_id     INTEGER        NOT NULL,
   FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Coments
(
   id             INTEGER        PRIMARY KEY,
   publish_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   body           VARCHAR(255)       NOT NULL,
   user_to        INTEGER        NOT NULL,
   user_from      INTEGER        NOT NULL,
   FOREIGN KEY (user_to) REFERENCES Users(id),
   FOREIGN KEY (user_from) REFERENCES Users(id),
   INDEX          (publish_date ASC)
);

CREATE TABLE CatProducts
(
   cat_name       VARCHAR(255),
   product_id     INTEGER,
   PRIMARY KEY (cat_name,product_id),
   FOREIGN KEY (cat_name) REFERENCES Categories(cat_name),
   FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Interests
(
   cat_name       VARCHAR(255),
   user_id        INTEGER,
   PRIMARY KEY (cat_name,user_id),
   FOREIGN KEY (cat_name) REFERENCES Categories(cat_name),
   FOREIGN KEY (user_id) REFERENCES Users(id),
   INDEX          (user_id ASC)
);

CREATE TABLE Follows
(
   user_id        INTEGER,
   product_id     INTEGER,
   PRIMARY KEY (user_id,product_id),
   FOREIGN KEY (user_id) REFERENCES Users(id),
   FOREIGN KEY (product_id) REFERENCES Products(id),
   INDEX          (user_id ASC)
);

CREATE TABLE Bids
(
   bid            FLOAT          NOT NULL,
   user_id        INTEGER,
   product_id     INTEGER,
   PRIMARY KEY (user_id,product_id),
   FOREIGN KEY (user_id) REFERENCES Users(id),
   FOREIGN KEY (product_id) REFERENCES Products(id),
   INDEX          (user_id ASC),
   INDEX          (product_id ASC),
   ts_create   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   ts_edit     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Trades
(
   id             INTEGER        PRIMARY KEY,
   closed         BOOLEAN        NOT NULL,
   user_sell      INTEGER        NOT NULL,
   product_id     INTEGER        NOT NULL,
   user_buy       INTEGER        NOT NULL,
   price          FLOAT          NOT NULL,
   FOREIGN KEY (user_buy) REFERENCES Users(id),
   FOREIGN KEY (product_id) REFERENCES Products(id),
   FOREIGN KEY (user_sell) REFERENCES Users(id),
   INDEX          (product_id ASC),
   ts_create   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   ts_edit     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Messages
(
   id             INTEGER        PRIMARY KEY,
   msg_date       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   body           VARCHAR(255)       NOT NULL,
   user_to        INTEGER        NOT NULL,
   user_from      INTEGER        NOT NULL,
   trade_id       INTEGER        NOT NULL,
   FOREIGN KEY (user_to) REFERENCES Users(id),
   FOREIGN KEY (user_from) REFERENCES Users(id),
   FOREIGN KEY (trade_id) REFERENCES Trades(id),
   INDEX          (msg_date ASC)
);

CREATE TABLE TradesOffers
(
   trade_id        INTEGER,
   product_id      INTEGER,
   PRIMARY KEY (trade_id,product_id),
   FOREIGN KEY (trade_id) REFERENCES Trades(id),
   FOREIGN KEY (product_id) REFERENCES Products(id),
   INDEX          (product_id ASC),
   ts_create   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

