--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

--task13 (lesson3)
--Компьютерная фирма: Вывести список всех продуктов и производителя с указанием типа продукта (pc, printer, laptop). Вывести: model, maker, type

select l.model, maker, type from (select model,price
from pc p  
union all 
select model,price from printer p2  
union all 
select model,price from laptop) as l
join 
product
on 
l.model = product.model



--task14 (lesson3)
--Компьютерная фирма: При выводе всех значений из таблицы printer дополнительно вывести для тех, у кого цена вышей средней PC - "1", у остальных - "0"

with avg_pc as(
	select avg(price)
	from pc
	)
select *,
case when price > (select * from avg_pc)
then 1
else 0
end flag
from printer


--task15 (lesson3)
--Корабли: Вывести список кораблей, у которых class отсутствует (IS NULL)

with all_ships as(
	select * from ships s 
	full join
	outcomes o 
	on
	s.name = o.ship
	)
select ship from all_ships
where class is null


--task16 (lesson3)
--Корабли: Укажите сражения, которые произошли в годы, не совпадающие ни с одним из годов спуска кораблей на воду.


with date_laun as(
	select launched 
	from ships s 
	)
select name from battles b
where extract(year from date) not in (select * from date_laun)


--task17 (lesson3)
--Корабли: Найдите сражения, в которых участвовали корабли класса Kongo из таблицы Ships.

select battle from outcomes o
left join
ships s 
on
s.name = o.ship
where class = 'Kongo'


--task1  (lesson4)
-- Компьютерная фирма: Сделать view (название all_products_flag_300) для всех товаров (pc, printer, laptop) с флагом, если стоимость больше > 300. Во view три колонки: model, price, flag

create view all_products_flag_300 as
select model, price,
case when price > 300
then 1
else 0
end flag
from 
(select model m,price
from pc p  
union all 
select model m,price from printer p2  
union all 
select model m,price from laptop) as l
join
product
on 
l.m = product.model

--task2  (lesson4)
-- Компьютерная фирма: Сделать view (название all_products_flag_avg_price) для всех товаров (pc, printer, laptop) с флагом, если стоимость больше cредней . Во view три колонки: model, price, flag

create view all_products_flag_avg_price as
with all_product as(
	select model, price
	from pc p  
	union all 
	select model, price 
	from printer p2  
	union all 
	select model, price 
	from laptop
	)
select model, price,
case when price > (select avg(price) from all_product)
then 1
else 0
end flag
from all_product

--task3  (lesson4)
-- Компьютерная фирма: Вывести все принтеры производителя = 'A' со стоимостью выше средней по принтерам производителя = 'D' и 'C'. Вывести model

select p.model from printer p 
join
product pr
on 
p.model = pr.model
where 
price > (select avg(price) from printer where maker = 'D' or maker = 'C')
and 
maker = 'A'

--task4 (lesson4)
-- Компьютерная фирма: Вывести все товары производителя = 'A' со стоимостью выше средней по принтерам производителя = 'D' и 'C'. Вывести model

with all_product as(
	select model m, price
	from pc p  
	union all 
	select model m, price 
	from printer p2  
	union all 
	select model m, price 
	from laptop
	)
select model from all_product p
join
product pr
on 
p.m = pr.model
where 
price > (select avg(price) from printer where maker = 'D' or maker = 'C')
and 
maker = 'A'

--task5 (lesson4)
-- Компьютерная фирма: Какая средняя цена среди уникальных продуктов производителя = 'A' (printer & laptop & pc)

with all_product as(
	select model m, price
	from pc p  
	union all 
	select model m, price 
	from printer p2  
	union all 
	select model m, price 
	from laptop
	)
select avg(price) from all_product p
join
product pr
on 
p.m = pr.model
where maker = 'A'

--task6 (lesson4)
-- Компьютерная фирма: Сделать view с количеством товаров (название count_products_by_makers) по каждому производителю. Во view: maker, count

create view count_products_by_makers as
with all_product as(
	select model m, price
	from pc p  
	union all 
	select model m, price 
	from printer p2  
	union all 
	select model m, price 
	from laptop
	)
select maker, count(model) c from all_product p
join
product pr
on 
p.m = pr.model
group by maker

--task7 (lesson4)
-- По предыдущему view (count_products_by_makers) сделать график в colab (X: maker, y: count)


request = """
select * from count_products_by_makers

"""
df = pd.read_sql_query(request, conn)
fig = px.bar(x=df.maker.to_list(), y=df.c.to_list(), labels={'x':'maker', 'y':'count'})
fig.show()



--task8 (lesson4)
-- Компьютерная фирма: Сделать копию таблицы printer (название printer_updated) и удалить из нее все принтеры производителя 'D'

create table printer_updated as
select * from printer p 
where model not in (
	select p2.model from printer p2
	join
	product p3 on
	p2.model = p3.model 
	where maker = 'D'
	)

--task9 (lesson4)
-- Компьютерная фирма: Сделать на базе таблицы (printer_updated) view с дополнительной колонкой производителя (название printer_updated_with_makers)
-- другого способа не нашел пока

create view printer_updated_with_makers as
select code, p.model, color, p.type, price, maker
from printer_updated p
join
product pr 
on
p.model = pr.model


--task10 (lesson4)
-- Корабли: Сделать view c количеством потопленных кораблей и классом корабля (название sunk_ships_by_classes). Во view: count, class (если значения класса нет/IS NULL, то заменить на 0)

create view sunk_ships_by_classes as
with sunk_ships as(
select count(name) c, coalesce (class, '0') as class from outcomes o 
left join
ships s 
on
o.ship = s.name
where result = 'sunk'
group by class)
SELECT *
FROM sunk_ships

--или так, не понял что нужно на 0 заменить =), если count, то получилось так
   
with sunk_ships as(
select count(name) c, class from outcomes o 
left join
ships s 
on
o.ship = s.name
where result = 'OK'
group by class)
SELECT class,
case when class is null 
then 0
else c
end
FROM sunk_ships  


--task11 (lesson4)
-- Корабли: По предыдущему view (sunk_ships_by_classes) сделать график в colab (X: class, Y: count)

request = """
select * from sunk_ships_by_classes
"""
df = pd.read_sql_query(request, conn)
fig = px.bar(x=df['class'].to_list(), y=df.c.to_list(), labels={'x':'class', 'y':'count'})
fig.show()


--task12 (lesson4)
-- Корабли: Сделать копию таблицы classes (название classes_with_flag) и добавить в нее flag: если количество орудий больше или равно 9 - то 1, иначе 0

create table classes_with_flag as
select *, 
case when numguns >= 9
then 1
else 0
end flag
from classes c 


--task13 (lesson4)
-- Корабли: Сделать график в colab по таблице classes с количеством классов по странам (X: country, Y: count)

request = """
select country, count(class) c
from classes
group by country 
"""
df = pd.read_sql_query(request, conn)
fig = px.bar(x=df.country.to_list(), y=df.c.to_list(), labels={'x':'country', 'y':'count'})
fig.show()


--task14 (lesson4)
-- Корабли: Вернуть количество кораблей, у которых название начинается с буквы "O" или "M".

select count(name) from ships s 
where name like 'O%' or name like 'M%'


--task15 (lesson4)
-- Корабли: Вернуть количество кораблей, у которых название состоит из двух слов.

select count(name) from ships s 
where name like '% %'


--task16 (lesson4)
-- Корабли: Построить график с количеством запущенных на воду кораблей и годом запуска (X: year, Y: count)

request = """
select launched, count(name) c 
from ships
group by launched
"""
df = pd.read_sql_query(request, conn)
fig = px.bar(x=df.launched.to_list(), y=df.c.to_list(), labels={'x':'year', 'y':'count'})
fig.show()