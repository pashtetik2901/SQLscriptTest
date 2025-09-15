WITH last_month_orders AS (
    SELECT id FROM orders
    WHERE order_date >= date('now', '-1 month')
),
product_sales AS (
    SELECT
        oi.product_id,
        SUM(oi.quantity) AS total_quantity
    FROM order_items oi
    JOIN last_month_orders lmo ON oi.order_id = lmo.id
    GROUP BY oi.product_id
),
product_with_root_category AS (
    SELECT
        p.id AS product_id,
        p.name AS product_name,
        COALESCE(
            -- выбираем категорию 1-го уровня (если parent_id IS NULL)
            CASE WHEN c.parent_id IS NULL THEN c.name
            ELSE pc.name END,
            'Без категории'
        ) AS root_category
    FROM products p
    JOIN categories c ON p.category_id = c.id
    LEFT JOIN categories pc ON c.parent_id = pc.id
)
SELECT
    pwr.product_name,
    pwr.root_category AS category_1_level,
    ps.total_quantity
FROM product_sales ps
JOIN product_with_root_category pwr ON ps.product_id = pwr.product_id
ORDER BY ps.total_quantity DESC

