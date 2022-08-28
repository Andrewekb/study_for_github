--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

-- Задание 1: Вывести name, class по кораблям, выпущенным после 1920
--
select name, class 
from ships
where launched > 1920

-- Задание 2: Вывести name, class по кораблям, выпущенным после 1920, но не позднее 1942
--
select name, class 
from ships
where launched > 1920 
and launched <= 1942

-- Задание 3: Какое количество кораблей в каждом классе. Вывести количество и class
--

select class, count(name)
from ships s 
group by class;

-- Задание 4: Для классов кораблей, калибр орудий которых не менее 16, укажите класс и страну. (таблица classes)
--

select class, country
from classes
where bore >= 16;


-- Задание 5: Укажите корабли, потопленные в сражениях в Северной Атлантике (таблица Outcomes, North Atlantic). Вывод: ship.
--

select ship from outcomes
where result = 'sunk'
and battle = 'North Atlantic';


-- Задание 6: Вывести название (ship) последнего потопленного корабля


select ship 
from outcomes o 
join
battles b 
on
o.battle = b.name
where result = 'sunk'
and 
date = (select max(date) from outcomes o 
join
battles b 
on
o.battle = b.name
where result = 'sunk');


-- Задание 7: Вывести название корабля (ship) и класс (class) последнего потопленного корабля
-- Здесь отсутствует наименование класса у кораблей, в обоих случаях class = NONE


select ship, class from battles b 
join
(select * from outcomes o 
left join
ships s
on o.ship  = s.name ) as l
on 
b.name = l.battle
where 
date = (select max(date) from outcomes o2 
join
battles b2 
on
o2.battle = b2.name)
and
result = 'sunk'




-- Задание 8: Вывести все потопленные корабли, у которых калибр орудий не менее 16, и которые потоплены. Вывод: ship, class
--

select * from outcomes o 
join
(
select * from ships s 
join
classes c 
on
s.class = c.class
) as l 
on 
o.ship  = l.name
where 
result = 'sunk'
and bore >= 16


-- Задание 9: Вывести все классы кораблей, выпущенные США (таблица classes, country = 'USA'). Вывод: class
--

select class from classes c 
where country = 'USA'

-- Задание 10: Вывести все корабли, выпущенные США (таблица classes & ships, country = 'USA'). Вывод: name, class


select s.class, s.name from ships s 
join
classes c 
on
s.class = c.class
where country = 'USA'
