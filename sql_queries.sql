USE ecommerce_analysis;

-- Q1: Total Revenue & Orders by Product Category
SELECT 
    `Product Category`,
    ROUND(SUM(`Total Revenue`), 2)        AS Total_Revenue,
    COUNT(DISTINCT `Transaction ID`)       AS Total_Orders,
    ROUND(AVG(`Total Revenue`), 2)         AS Avg_Order_Value
FROM sales_data
GROUP BY `Product Category`
ORDER BY Total_Revenue DESC;

-- Q2: Monthly Revenue Trend
SELECT 
    YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d'))  AS Year,
    MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')) AS Month,
    MONTHNAME(STR_TO_DATE(`Date`, '%Y-%m-%d')) AS Month_Name,
    ROUND(SUM(`Total Revenue`), 2)         AS Monthly_Revenue,
    COUNT(DISTINCT `Transaction ID`)        AS Total_Orders
FROM sales_data
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;

-- Q3: Revenue by Region
SELECT 
    Region,
    ROUND(SUM(`Total Revenue`), 2)         AS Total_Revenue,
    COUNT(DISTINCT `Transaction ID`)        AS Total_Orders,
    ROUND(AVG(`Total Revenue`), 2)          AS Avg_Order_Value
FROM sales_data
GROUP BY Region
ORDER BY Total_Revenue DESC;

-- Q4: KPI Summary Dashboard
SELECT
    ROUND(SUM(`Total Revenue`), 2)          AS Total_Revenue,
    COUNT(DISTINCT `Transaction ID`)         AS Total_Orders,
    ROUND(AVG(`Total Revenue`), 2)           AS Avg_Order_Value,
    SUM(`Units Sold`)                        AS Total_Units_Sold,
    COUNT(DISTINCT `Product Category`)       AS Total_Categories,
    COUNT(DISTINCT `Region`)                 AS Total_Regions
FROM sales_data;