--task1  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/the-report/problem

-- вы решали на уроке, последнее задание задвоено с данным

--task2  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/occupations/problem

-- разобрался, хотел попробовать сделать в PG на нашей базе, нагуглил, что нужно поставить расширение в ДБ, но прав таких нет
-- с pivot какое то не очевидное решение

select doctor, professor, singer, actor from
(select * from
(select name, occupation, row_number() over(partition by occupation order by name) as rn 
from Occupations)
pivot 
(max(name) for occupation in ('Doctor' as doctor, 'Professor' as professor, 'Singer' as singer, 'Actor' as actor)) order by rn);


--task3  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-9/problem

SELECT DISTINCT city FROM STATION
WHERE UPPER(SUBSTR(city,1,1)) NOT IN ('A','E','I','O','U');


--task4  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-10/problem

select distinct city from station 
where substr(city, LENGTH (city), length(city)) NOT IN ('a','e','i','o','u');


--task5  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-11/problem

SELECT DISTINCT city FROM STATION
WHERE UPPER(SUBSTR(city,1,1)) NOT IN ('A','E','I','O','U') or substr(city, LENGTH (city), length(city)) NOT IN ('a','e','i','o','u');


--task6  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-12/problem

SELECT DISTINCT city FROM STATION
WHERE UPPER(SUBSTR(city,1,1)) NOT IN ('A','E','I','O','U') and substr(city, LENGTH (city), length(city)) NOT IN ('a','e','i','o','u');


--task7  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/salary-of-employees/problem

select name from employee
where salary > 2000 and months < 10
order by employee_id;


--task8  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/the-report/problem
