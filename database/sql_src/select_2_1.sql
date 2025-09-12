SELECT clients.name, SUM(products.quantity * products.price) AS сумма 
FROM clients
JOIN orders ON orders.client_id = clients.id
JOIN order_items ON order_items.order_id = orders.id
JOIN products ON products.id = order_items.product_id
GROUP BY clients.name
