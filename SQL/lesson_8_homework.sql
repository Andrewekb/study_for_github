--task1  (lesson8)
-- oracle: https://leetcode.com/problems/department-top-three-salaries/

with all_data as(
    select d.name department, salary, e.name from Department d
    join
    employee e
    on
    e.departmentId = d.id)
select department, salary, name from(
select *,
row_number() over(partition by department order by salary desc) as l
from all_data) pr
where l in (1, 2, 3)


--task2  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/17

select member_name, status, sum(unit_price * amount) as costs
from FamilyMembers
JOIN 
Payments
ON 
member_id = family_member 
WHERE date LIKE '2005%'
group by member_name, status


--task3  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/13

select name from 
(select name, count(*) as c from passenger group by name) l
where c > 1


--task4  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/38

select count(first_name ) as count 
from Student
where first_name  = 'Anna'


--task5  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/35

select count(distinct classroom) as count 
from Schedule
where date like '2019-09-02%'


--task7  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/32
--this is very bad task =)

select floor(avg(DATEDIFF
(now(),birthday)/365)) as age
from FamilyMembers


--task8  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/27

with g_t as(select good_id, good_type_name
    from Goods g
    JOIN 
    GoodTypes gt
    on 
    gt.good_type_id = g.type)
select good_type_name, sum(amount * unit_price) costs 
from g_t
JOIN 
Payments p
ON 
p.good = g_t.good_id
where date like '2005%'
group by good_type_name 


--task9  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/37

select min(floor(DATEDIFF
(now(),birthday)/365)) as year
from Student


--task10  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/44

with t_ex as(
select * from
(select student, class, birthday
from Student_in_class sc
join 
Student s
ON 
sc.student = s.id) l
JOIN 
class c
ON 
c.id = l.class
where name like '10%')
select max(floor(DATEDIFF
(now(),birthday)/365)) as max_year
from t_ex


--task11 (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/20

with one as(
    select good, member_name, status, 
    (unit_price * amount) as costs
    from FamilyMembers
    JOIN 
    Payments
    ON 
    member_id = family_member
),
    type_g as(
    select good_type_name, good_id 
    from Goods
    JOIN 
    GoodTypes
    ON 
    type = good_type_id
)
select status, member_name, sum(costs) costs from 
one 
JOIN 
type_g
ON 
good_id = good
where good_type_name = 'entertainment'
group by member_name, status  


--task12  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/55

with c_trip as(
    select company, count(*) c
    FROM Trip
    group by company 
    ),
    c_trip_min as(
    select company from c_trip 
    where  c = (select min(c) from c_trip))
delete from Company id 
where id in (select * from c_trip_min)


--task13  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/45

with c_cr as (
    select classroom, count(date) c 
    from Schedule
    group by classroom)
select classroom from c_cr
where c = (select max(c) from c_cr)


--task14  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/43

select last_name  from
(select last_name, subject  
from Teacher
join Schedule
ON
Teacher.id = teacher) l
JOIN 
Subject
on 
subject = id
where name = 'Physical Culture'
order by last_name 


--task15  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/63

-- Марат, я не понимаю, за что он ругается, на мой взгляд вывод такой, какой просит задание

select 
CONCAT(left(last_name, 1), 
lower(SUBSTRING(last_name, 2, LENGTH(last_name))),
'.',
left(first_name,1), '.',
LEFT(middle_name,1), '.') as name
from Student
order by last_name
