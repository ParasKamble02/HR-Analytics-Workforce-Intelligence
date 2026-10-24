SELECT VERSION() AS mysql_version;
SHOW DATABASES;
CREATE DATABASE IF NOT EXISTS hr_analytics;

USE hr_analytics;
SELECT DATABASE() AS current_database;

SELECT COUNT(*) AS total_rows FROM hr_employee_attrition;

USE hr_analytics;

-- Check column names and data types
DESCRIBE hr_employee_attrition;

-- Count employees by attrition status
SELECT Attrition, COUNT(*) AS employee_count FROM hr_employee_attrition GROUP BY Attrition;

-- Preview the first 10 records
SELECT * FROM hr_employee_attrition LIMIT 10;

-- Column name changing
ALTER TABLE hr_employee_attrition RENAME COLUMN `ï»¿Age` TO Age;

-- overall attrition rate
SELECT COUNT(*) AS total_employees, SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS employees_retained,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition;

-- attrition by department
SELECT Department, COUNT(*) AS total_employees, SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2 ) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY Department ORDER BY attrition_rate_pct DESC;

-- impact of overtime
SELECT OverTime, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY OverTime ORDER BY attrition_rate_pct DESC;

-- attrition by job role
SELECT JobRole, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY JobRole ORDER BY attrition_rate_pct DESC;

-- attrition by age group
SELECT
    CASE
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN Age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '56-65'
    END AS age_group,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)/ COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY age_group ORDER BY MIN(Age);

-- monthly income and attrition
SELECT Attrition,
    COUNT(*) AS total_employees,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    ROUND(MIN(MonthlyIncome), 2) AS min_monthly_income,
    ROUND(MAX(MonthlyIncome), 2) AS max_monthly_income
FROM hr_employee_attrition
GROUP BY Attrition;

-- attrition by job satisfaction
SELECT JobSatisfaction, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY JobSatisfaction ORDER BY JobSatisfaction;

-- attrition by work life balance
SELECT WorkLifeBalance, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY WorkLifeBalance ORDER BY WorkLifeBalance;

-- attrition by years at company
SELECT
    CASE
        WHEN YearsAtCompany BETWEEN 0 AND 1 THEN '0-1 years'
        WHEN YearsAtCompany BETWEEN 2 AND 3 THEN '2-3 years'
        WHEN YearsAtCompany BETWEEN 4 AND 5 THEN '4-5 years'
        WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
        ELSE '11+ years'
    END AS tenure_group,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY tenure_group ORDER BY MIN(YearsAtCompany);

-- atttrition by business travel
SELECT BusinessTravel, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY BusinessTravel ORDER BY attrition_rate_pct DESC;

-- attrition by job level
SELECT JobLevel, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY JobLevel ORDER BY JobLevel;

-- attrition by gender
SELECT Gender, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),2) AS attrition_rate_pct
FROM hr_employee_attritionn GROUP BY Gender ORDER BY attrition_rate_pct DESC;

-- attrition by number of companies worked
SELECT NumCompaniesWorked, COUNT(*) AS total_employees, 
	SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY NumCompaniesWorked ORDER BY NumCompaniesWorked;

-- attrition by year since last promotion
SELECT YearsSinceLastPromotion, COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY YearsSinceLastPromotion ORDER BY YearsSinceLastPromotion;

-- employees earning below the company average
SELECT EmployeeNumber, Age, Department, JobRole, MonthlyIncome, Attrition
FROM hr_employee_attrition
WHERE MonthlyIncome < (SELECT AVG(MonthlyIncome) FROM hr_employee_attrition)
ORDER BY MonthlyIncome ASC
LIMIT 20;

-- to rank job roles from highest to lowest attrition rate
WITH role_stats AS (
    SELECT JobRole, COUNT(*) AS total_employees,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
        ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
    FROM hr_employee_attrition GROUP BY JobRole)
SELECT JobRole, total_employees, employees_left, attrition_rate_pct,
    RANK() OVER ( ORDER BY attrition_rate_pct DESC) AS attrition_rank
FROM role_stats
ORDER BY attrition_rank;

-- to find departments with an attrition rate higher than the company-wide rate
WITH department_stats AS (
    SELECT Department, COUNT(*) AS total_employees,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left
    FROM hr_employee_attrition GROUP BY Department),
company_stats AS (
    SELECT 100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*) AS company_attrition_rate
    FROM hr_employee_attrition)
SELECT d.Department, d.total_employees, d.employees_left,
    ROUND(100.0 * d.employees_left / d.total_employees, 2) AS department_attrition_rate,
    ROUND(c.company_attrition_rate, 2) AS company_attrition_rate
FROM department_stats d
CROSS JOIN company_stats c
WHERE 100.0 * d.employees_left / d.total_employees > c.company_attrition_rate
ORDER BY department_attrition_rate DESC;