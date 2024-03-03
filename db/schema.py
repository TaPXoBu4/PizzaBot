DB_NAME = 'delivery.db'

CREATE_SCRIPT = '''
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT
    );
CREATE TABLE IF NOT  EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
    );
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP,
    location INTEGER,
    address TEXT,
    courier INTEGER,
    price INTEGER,
    paytype TEXT,
    FOREIGN KEY (location) REFERENCES locations (id),
    FOREIGN KEY (courier) REFERENCES users (id)
    );
'''