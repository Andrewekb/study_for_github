--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

--task1 (lesson5)
-- Компьютерная фирма: Сделать view (pages_all_products), в которой будет постраничная разбивка всех продуктов (не более двух продуктов на одной странице). Вывод: все данные из laptop, номер страницы, список всех страниц


select page_num, position from
(select *,
case when rn % 2 = 0 then rn / 2 else rn / 2 + 1 end  as page_num, 
case when rn % 2 = 0 then 2 else 1 end as position
from (
  select *, row_number(*) over (order by price desc) as rn
  from laptop 
) a) l


--task2 (lesson5)
-- Компьютерная фирма: Сделать view (distribution_by_type), в рамках которого будет процентное соотношение всех товаров по типу устройства. Вывод: производитель, тип, процент (%)


with l_p as
	(select maker, type, count(m) m  
	from (select price, model m from pc
	union all
	select price, model m from printer
	union all
	select price, model m from laptop) l
	join
	product p
	on
	l.m = p.model
	group by type, maker
	order by type )
select type, maker, percent
from(select *,
round(m / sum(m) over() * 100, 2) as percent
from l_p) p


--task3 (lesson5)
-- Компьютерная фирма: Сделать на базе предыдущенр view график - круговую диаграмму. Пример https://plotly.com/python/histograms/


request = """
select * from distribution_by_type
"""
df = pd.read_sql_query(request, conn)
fig = px.pie(values=df.percent.to_list(), names=df.type.to_list())
fig.show()


--task4 (lesson5)
-- Корабли: Сделать копию таблицы ships (ships_two_words), но название корабля должно состоять из двух слов


create table ships_two_words as
select * from ships s 
where name like '% %'


--task5 (lesson5)
-- Корабли: Вывести список кораблей, у которых class отсутствует (IS NULL) и название начинается с буквы "S"


select * from
(select name, s.class from ships s
join 
classes c
on
s.class = c.class) l
left join 
outcomes o 
on
l.name = o.ship 
where class is null 
and
name like 'S%'


--task6 (lesson5)
-- Компьютерная фирма: Вывести все принтеры производителя = 'A' со стоимостью выше средней по принтерам производителя = 'C' и три самых дорогих (через оконные функции). Вывести model


with p_pr as(
	select maker, price, p.model m
	from printer p 
	join
	product pr 
	on 
	p.model = pr.model 
	),
avg_c as (
	select avg(price) 
	from 
	p_pr
	where maker = 'C'
	)
select m from p_pr 
where price > (select * from avg_c)
union all
select m from 
(select *,
rank() over(order by price)
from p_pr) l
where rank in (1, 2, 3)