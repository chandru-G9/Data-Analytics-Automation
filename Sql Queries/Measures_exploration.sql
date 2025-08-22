-- Key metrics of the business
SELECT 'Total Sales' AS measure_name, SUM(sales_amount) AS measure_value FROM dbo.fact_sales
UNION ALL
SELECT 'Total Quantity', SUM(quantity) FROM dbo.fact_sales
UNION ALL
SELECT 'Average Price', AVG(price) FROM dbo.fact_sales
UNION ALL
SELECT 'Total Orders', COUNT(DISTINCT order_number) FROM dbo.fact_sales
UNION ALL
SELECT 'Total Products', COUNT(DISTINCT product_name) FROM dbo.dim_products
UNION ALL
SELECT 'Total Customers',COUNT(DISTINCT customer_key) AS total_customers FROM dbo.fact_sales;
