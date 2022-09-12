--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

--task1  (lesson6, дополнительно)
-- SQL: Создайте таблицу с синтетическими данными (10000 строк, 3 колонки, все типы int) и заполните ее случайными данными от 0 до 1 000 000. 
--Проведите EXPLAIN операции и сравните базовые операции.

drop table sint_test 

create table sint_test (one int, two int, four int, five int);

select max(two) from sint_test 

insert into sint_test (one, two, four, five) 
values (generate_series(1,10000),random() * 1000000 , random() * 1000000, random() * 1000000);

explain select distinct two from sint_test 

explane select max(two) from sint_test 

--task2 (lesson6, дополнительно)
-- GCP (Google Cloud Platform): Через GCP загрузите данные csv в базу PSQL по личным реквизитам 
--(используя только bash и интерфейс bash) 

-- я пока не разобрался с типами данных, и способ долго реализуется, наверно,
-- есть более простой вариант
-- как верно выбрать тип данных пока не разобрался, везде текст

(base) andrejmironov@MacBook-Air-Andrej ~ % psql
psql (14.5 (Homebrew))
Type "help" for help.

andrejmironov=# \l
                                      List of databases
     Name      |     Owner     | Encoding | Collate | Ctype |        Access privileges        
---------------+---------------+----------+---------+-------+---------------------------------
 andrejmironov | andrejmironov | UTF8     | C       | C     | 
 postgres      | andrejmironov | UTF8     | C       | C     | 
 template0     | andrejmironov | UTF8     | C       | C     | =c/andrejmironov               +
               |               |          |         |       | andrejmironov=CTc/andrejmironov
 template1     | andrejmironov | UTF8     | C       | C     | =c/andrejmironov               +
               |               |          |         |       | andrejmironov=CTc/andrejmironov


create table avocado(
id int, Date varchar(30), 
AveragePrice varchar(30), 
Total_Volume varchar(30),
a_4046 varchar(30),
a_4225 varchar(30),
a_4770 varchar(30),
Total_Bags varchar(30),
Small_Bags varchar(30),
Large_Bags varchar(30),
XLarge_Bags varchar(30),
type varchar(30),year varchar(30),
region varchar(30))

andrejmironov=# \copy avocado FROM 'downloads/6/avocado.csv' csv;
