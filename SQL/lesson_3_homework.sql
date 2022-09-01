--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing

--task1
--Корабли: Для каждого класса определите число кораблей этого класса, потопленных в сражениях. Вывести: класс и число потопленных кораблей.


select class, count(ship)
from
ships s 
left join
(select * from outcomes o 
where result = 'sunk') as l
on 
s.name = l.ship
group by class



--task2
--Корабли: Для каждого класса определите год, когда был спущен на воду первый корабль этого класса. Если год спуска на воду головного корабля неизвестен, определите минимальный год спуска на воду кораблей этого класса. Вывести: класс, год.

with min_launched as(
	select class, min(launched) as m
	from ships s 
	group by class
	)
select c.class, m
from classes as c
left join
min_launched
on
min_launched.class = c.class

--task3
--Корабли: Для классов, имеющих потери в виде потопленных кораблей и не менее 3 кораблей в базе данных, вывести имя класса и число потопленных кораблей.
-- по ощущениям, все должно быть проще, нагородил :)

with ships_outc as (select * 
	from ships s 
	left join outcomes o 
	on s.name = o.ship
	),
	count_name as(
	select count(name) as n, class 
	from ships s2 
	group by class
	)
select ships_outc.class, count(name) as l
from count_name
left join
ships_outc
on
count_name.class = ships_outc.class
where n >= 3
and 
result = 'sunk'
group by ships_outc.class



--task4
--Корабли: Найдите названия кораблей, имеющих наибольшее число орудий среди всех кораблей такого же водоизмещения (учесть корабли из таблицы Outcomes).

with class_gun as(
	select distinct displacement, max(numguns) as l 
	from classes c 
	group by displacement 
	),
	max_num as(
	select * from ships s 
	left join
	classes c2 
	on 
	s.class = c2.class
	)
select * 
from class_gun
join
max_num
on
class_gun.displacement = max_num.displacement

--task5
--Компьютерная фирма: Найдите производителей принтеров, которые производят ПК с наименьшим объемом RAM и с самым быстрым процессором среди всех ПК, имеющих наименьший объем RAM. Вывести: Maker


with data_pr as (select distinct maker as m from printer p 
join product p2 
on
p.model = p2.model),
data_pc as (select * from pc p 
join product p2 
on
p.model = p2.model),
data_total as (select * from data_pc join data_pr on data_pc.maker = data_pr.m)
select maker from data_total
where ram = (select min(ram) from data_total)
and 
speed = (select max(speed) from data_total where ram = (select min(ram) from data_total))