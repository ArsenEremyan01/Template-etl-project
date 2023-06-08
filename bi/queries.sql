-- Total Quantity per Product
SELECT dim_product_name.name, SUM(total_qty ) as total_qty
FROM fact_sales
LEFT JOIN dim_product_name ON fact_sales.product_name_id=dim_product_name.id
GROUP BY dim_product_name.name
ORDER BY 2 DESC;


-- Total Quantity per Product Category
SELECT dim_product_group.group_name , SUM(total_qty ) as total_qty
FROM fact_sales
LEFT JOIN dim_product_group ON fact_sales.product_group_id=dim_product_group.id
GROUP BY dim_product_group.group_name
ORDER BY 2 DESC;
