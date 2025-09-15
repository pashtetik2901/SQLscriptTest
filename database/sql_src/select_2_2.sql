SELECT categories.id, categories.name, COUNT(child.id) AS Дочерних FROM categories
LEFT JOIN categories child ON categories.id = child.parent_id
GROUP BY categories.name
ORDER BY categories.id ASC