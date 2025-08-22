-- List of countries from which customers originate
SELECT DISTINCT country FROM dbo.dim_customers
where country!='n/a'
ORDER BY country;

-- List of categories, subcategories, and products
SELECT DISTINCT 
    category, 
    subcategory, 
    product_name 
FROM dbo.dim_products
ORDER BY category, subcategory, product_name;