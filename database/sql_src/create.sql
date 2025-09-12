CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,             -- Уникальный идентификатор категории
    name VARCHAR(255) NOT NULL,          -- Название категории
    parent_id INT NULL,                  -- Ссылка на родительскую категорию (NULL для корневых)
    CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES categories(id) -- Внешний ключ на саму таблицу для построения иерархии
);
CREATE INDEX idx_categories_parent_id ON categories(parent_id);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- Уникальный идентификатор товара
    name VARCHAR(255) NOT NULL,          -- Наименование товара
    quantity INT NOT NULL CHECK (quantity >= 0), -- Количество товара на складе, неотрицательное
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0), -- Цена за единицу товара, неотрицательная
    category_id INT NOT NULL,            -- Ссылка на категорию товара
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(id) -- Внешний ключ на категорию
);
CREATE INDEX idx_products_category ON products(category_id);

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- Уникальный идентификатор клиента
    name VARCHAR(255) NOT NULL,          -- Наименование (имя) клиента
    address TEXT                        -- Адрес клиента (может быть NULL)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- Уникальный идентификатор заказа
    client_id INT NOT NULL,              -- Ссылка на клиента, сделавшего заказ
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата и время заказа (по умолчанию текущие)
    CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES clients(id) -- Внешний ключ на клиента
);
CREATE INDEX idx_orders_client ON orders(client_id);
CREATE INDEX idx_orders_date ON orders(order_date);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- Уникальный идентификатор позиции заказа
    order_id INT NOT NULL,               -- Ссылка на заказ
    product_id INT NOT NULL,             -- Ссылка на товар (номенклатуру)
    quantity INT NOT NULL CHECK (quantity > 0), -- Количество товара в позиции заказа (обязательно больше 0)
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id), -- Внешний ключ на заказ
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id), -- Внешний ключ на товар
    CONSTRAINT unq_order_product UNIQUE (order_id, product_id) -- Ограничение уникальности, чтобы товар не дублировался в одном заказе
);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
