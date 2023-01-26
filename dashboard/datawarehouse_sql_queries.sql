use data_warehouse_olist;

/*Se genera la dimension calendario*/
DROP TABLE IF EXISTS `calendario`;
CREATE TABLE calendario (
        id                      INTEGER PRIMARY KEY,  -- year*10000+month*100+day
        fecha                 	DATE NOT NULL,
        anio                    INTEGER NOT NULL,
        mes                   	INTEGER NOT NULL, -- 1 to 12
        dia                     INTEGER NOT NULL, -- 1 to 31
        trimestre               INTEGER NOT NULL, -- 1 to 4
        semana                  INTEGER NOT NULL, -- 1 to 52/53
        dia_nombre              VARCHAR(9) NOT NULL, -- 'Monday', 'Tuesday'...
        mes_nombre              VARCHAR(9) NOT NULL -- 'January', 'February'...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*---------------------------------------------------------------------------------------------------------------------*/
DROP PROCEDURE IF EXISTS `Llenar_dimension_calendario`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Llenar_dimension_calendario`(IN `startdate` DATE, IN `stopdate` DATE)
BEGIN
    DECLARE currentdate DATE;
    SET currentdate = startdate;
    WHILE currentdate < stopdate DO
        INSERT INTO calendario VALUES (
                        YEAR(currentdate)*10000+MONTH(currentdate)*100 + DAY(currentdate),
                        currentdate,
                        YEAR(currentdate),
                        MONTH(currentdate),
                        DAY(currentdate),
                        QUARTER(currentdate),
                        WEEKOFYEAR(currentdate),
                        DATE_FORMAT(currentdate,'%W'),
                        DATE_FORMAT(currentdate,'%M'));
        SET currentdate = ADDDATE(currentdate,INTERVAL 1 DAY);
    END WHILE;
END$$
DELIMITER ;

CALL Llenar_dimension_calendario('2015-01-01','2023-12-31');
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Se asigna Primary key a order_id 
*/
ALTER TABLE `data_warehouse_olist`.`order_items` 
ADD PRIMARY KEY (`order_id`);
;
/*---------------------------------------------------------------------------------------------------------------------*/


-- Venta agrupado por año, trimestre tipo de producto
SELECT c.anio, c.trimestre, tp.TipoProducto, SUM(v.Precio * v.Cantidad) as venta
FROM venta v
JOIN productos p ON(p.IdProducto = v.IdProducto)
JOIN tipo_producto tp ON(tp.IdTipoProducto = p.IdTipoProducto)
JOIN calendario c ON(c.Fecha = v.Fecha)
GROUP BY c.anio, c.trimestre, tp.TipoProducto
ORDER BY c.anio, c.trimestre, tp.TipoProducto;
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Genera los datos para la grafica de ingresos por año
*/
select year(o.purchase_timestamp) AS anio, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.order_id)
#JOIN calendario c ON(c.Fecha = o.purchase_timestamp) 
group by anio
order by anio asc
;

select c.anio, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.id)
JOIN ordes c ON(c.Fecha = o.purchase_timestamp)
group by c.anio
;

select c.anio, c.trimestre, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.id)
JOIN calendario c ON(c.Fecha = o.purchase_timestamp)
group by c.anio, c.trimestre
order by anio asc 
;
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Genera los datos para la grafica de ingresos por ciudad
*/
select g.city, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.order_id)
JOIN customers c ON(c.customer_id = o.customer_id )
JOIN geolocations g ON(g.zip_code = c.zip_code)
group by g.city
order by total desc
limit 20
;
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Genera la visualizacion de los productos categorizados
*/
select p.category_name, sum(oi.price) as total
from order_items oi
JOIN products p ON(oi.product_id = p.product_id)
group by p.category_name
order by total desc
limit 10
;
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Genera la visualizacion de vendedores y sus ventas por estado y ciudad
*/
select g.latitude, g.longitude, g.state, sum(oi.price) as total
from order_items oi
JOIN sellers s ON(s.seller_id = oi.seller_id) 
JOIN geolocations g ON(s.zip_code = g.zip_code)
group by g.latitude, g.longitude, g.state
order by total desc
;
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Genera la visualizacion de ingresos por estado
*/
select g.state, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.order_id)
JOIN customers c ON(c.customer_id = o.customer_id )
JOIN geolocations g ON(g.zip_code = c.zip_code)
group by g.state
order by total desc
limit 5
; 
/*---------------------------------------------------------------------------------------------------------------------*/
/*
columna de agregacion en orders_items. 
Se agrega la columna de purchase_timestamp

*/
/* Elimino la columna purchase_timesatmp me equivoque en el nombre. Luego la creo de nuevo*/
ALTER TABLE `data_warehouse_olist`.`order_items` 
DROP COLUMN `purchase_timesatmp`;

ALTER TABLE `order_items` ADD `purchase_timestamp` date AFTER `freight_value`;  # Se crea un nuevo campo de purchase_timestamp para la tabla

/*
EN ESTA PASO CON EL UPDATE ACTUALIZAMOS LA COLUMNA purchase_timestamp DE LA TABLA order items
UTILIZANDO UN JOIN ENTRE LAS TABLAS order_items Y orders CON LA COLUMNA id
Y AL FINAL CON EL SET ASIGNAMOS LOS VALORES

*/
UPDATE order_items oi
JOIN orders o ON (oi.order_id = o.id)
SET oi.purchase_timestamp = o.purchase_timestamp
;

/*

AREA DE CONSULTAS DE LOS KPIs

*/


/*
KPI - Variación porcentual del volumen de ventas por mes

Consulta de las ordenes agrupadas por mes del año 2017 y que calcula
el total de ventas para hallar la variacion

*/
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

SELECT s.purchase_timestamp AS fecha, sum(s.total) AS total
    FROM (
        SELECT o.purchase_timestamp, sum(i.price) AS total
        FROM orders AS o
        RIGHT JOIN order_items AS i ON (o.order_id = i.order_id)
        WHERE o.status != "canceled" AND o.status != "unavailable"
        GROUP BY o.order_id
    ) AS s
    GROUP BY year(s.purchase_timestamp), month(s.purchase_timestamp)
    HAVING year(s.purchase_timestamp) = 2017
    ;
/*
KPI - Variación porcentual del volumen de ventas por mes

Puntuación neta del promotor

*/
select score 
from order_reviews
where score > 3
;
select score 
from order_reviews
where score <= 3
;

/*
KPI - Fidelidad del cliente

Medir la tasa de clientes que vuelven a comprar dentro de un periodo determinado

*/
select o.purchase_timestamp AS fecha
from orders as o
join customers cu ON(cu.id = o.customer_id)


;
SELECT s.purchase_timestamp AS fecha, sum(s.total) AS total
    FROM (
        SELECT o.purchase_timestamp, sum(i.price) AS total
        FROM orders AS o
        RIGHT JOIN order_items AS i ON (o.order_id = i.order_id)
        WHERE o.status != "canceled" AND o.status != "unavailable"
        GROUP BY o.order_id
    ) AS s
    GROUP BY year(s.purchase_timestamp), month(s.purchase_timestamp)
    HAVING year(s.purchase_timestamp) = 2017
    order by fecha asc
    ;

/*
KPI - Tasa de Conversión

Medir la tasa de vendedores potenciales que se unen a la empresa

*/
select mql_id, max(won_date) as maximo
from closed_deals
;
select count(mql_id) as interesados
from marketing_qualified_leads
;
select count(mql_id) as cerrados
from closed_deals
;

/*
KPI - Puntualidad de la entrega

Medir el porcentaje de entregas que se realizan a tiempo en relación con el número total de entregas.

*/
select * 
from orders as o
where o.status = 'delivered'
;

select *
from orders
where estimated_delivery_date > delivered_customer_date 
having status = 'delivered'
;

select * from orders;

/*
KPI - Tiempo total del proceso (TTP)

Optimizar los tiempos de compra y envío.

*/

select *, (delivered_customer_date - purchase_timestamp) as tiempo_total
from orders
where status = 'delivered'
;

select *, avg(delivered_customer_date - purchase_timestamp) as tiempo_total
from orders
where status = 'delivered'
GROUP BY year(purchase_timestamp), month(purchase_timestamp)
;

select o.status, avg(o.delivered_customer_date - o.purchase_timestamp) as tiempo_total
from orders as o
GROUP BY year(o.purchase_timestamp), month(o.purchase_timestamp)
having status = 'delivered'
;
/*
Mapa de Vendedores

- Consulta para ubicar a los vendedores

*/
select g.latitude, g.longitude, g.state, g.city, sum(oi.price) as ventas
from order_items oi
JOIN sellers s ON(s.seller_id = oi.seller_id)
JOIN geolocations g ON(s.zip_code = g.zip_code)
group by g.latitude, g.longitude, g.state
order by ventas desc
limit 20
;
/*
Clientes por estado

- Consulta para de clientes por estado

*/
select g.state, count(c.customer_id) as nclientes
from customers c
JOIN geolocations g ON(c.zip_code = g.zip_code)
group by g.state
order by nclientes desc
limit 10;
/*
vendedores por estado

- Consulta para la cantidad de vendedores por estado

*/
select g.state, count(s.seller_id) as nvendedores
from sellers s
JOIN geolocations g ON(s.zip_code = g.zip_code)
group by g.state
order by nvendedores desc
limit 10;

/*
ventas por mes

- Consulta para la ventas por mes

*/
select month(o.approved_at) as mes, sum(oi.price) as ingresos
from order_items oi
JOIN orders o ON(oi.order_id = o.order_id)
group by mes
order by mes
;
/*
Relacion de status

- relacion del estado de las ordenes que fueron 
despachadas, canceladas y no disponibles

*/


select year(purchase_timestamp) as anio, status, count(status) as total
from orders
where status = 'delivered' or status='canceled' or status='unavailable'
group by anio, status
order by anio asc
;
/*
Metodo de pago

- Cantidad por tipo de metodo de pago

*/
select op.type, count(*) as total
from order_payments op
group by op.type
order by total desc
;
/*
Metodo de pago

- Distribucion de los cuotas diferidas y su valor 

*/
select installments, count(*) as diferido, sum(value) as total
from order_payments
group by installments
order by installments asc
;
select installments, count(*) as cantidad, sum(value) as total
from order_payments
group by installments
order by installments asc
;
/*
Metodo de pago

- Ingresos por tipo de metodo de pago 

*/
select type, sum(value) as total
from order_payments
group by type
order by total desc
;
/*
Delivery - Entregas

-  Analisis de Productos entregado en la fecha estimada

*/
SELECT count(d.dias) AS 'entregado',
CASE
WHEN d.dias  < 1 THEN 'Llego en fecha estimada'
ELSE 'LLego con retrazo'
END
AS Plazo_de_entrega
FROM (SELECT datediff(o.delivered_customer_date, o.estimated_delivery_date ) as dias
      FROM orders AS o
      WHERE o.status = 'delivered'
        ) AS d

GROUP BY Plazo_de_entrega
;
/*
Delivery - Entregas

-  Analisis de Productos entregado en un rango de dias

*/
SELECT count(d.dias) AS 'cantidad',
CASE
WHEN dias  < 4 THEN 'menos de 4'
WHEN dias < 7 THEN 'de 4 a 6'
WHEN dias < 11 THEN 'de 7 a 10'
WHEN dias < 16 THEN 'de 11 a 15'
ELSE 'más de 15'
END
AS rango_entregas
FROM (SELECT datediff(o.delivered_customer_date, o.purchase_timestamp ) as dias
      FROM orders AS o
      WHERE o.status = 'delivered'
        ) AS d

GROUP BY rango_entregas
;
/*
marketing - reviews

-  Serie de tiempo por volumen de primer contacto con el vendedor por año-mes

*/
select concat(year(first_contact_date), '-', month(first_contact_date)) as anio_mes, count(*) as volumen 
from marketing_qualified_leads
group by anio_mes
order by first_contact_date asc
;
 /*
marketing - reviews

-  Volumen por canal de mercadeo

*/
select origin, count(*) as volumen
from marketing_qualified_leads
group by origin
order by volumen desc
;
/*
marketing - reviews

-  Promedio de Flete por rango de peso

*/
SELECT avg(d.freight_value) AS 'promedio_flete',
CASE
WHEN d.weight_g  < 501 THEN 'menos de 500g'
WHEN d.weight_g < 1001 THEN 'de 500g a 1kg'
WHEN d.weight_g < 5001 THEN 'de 1kg a 5kg'
WHEN d.weight_g < 10001 THEN 'de 5kg a 10kg'
WHEN d.weight_g < 20001 THEN 'de 10kg a 20kg'
ELSE 'más de 20kg'
END
as rango_peso
FROM (SELECT i.product_id, i.freight_value, p.weight_g
      FROM order_items AS i
      LEFT JOIN products as p ON(i.product_id = p.product_id)
        ) AS d

GROUP BY rango_peso
;
/*
marketing - reviews

-  TOP 15 Promedio de score por categoria

*/
SELECT AVG(a.score) as prom_score, c.category_name AS categoria
      FROM order_reviews AS a
      INNER JOIN order_items AS b
      ON (a.order_id = b.order_id)
      INNER JOIN products AS c
      ON (b.product_id = c.product_id)
      GROUP BY categoria
      order by prom_score desc
      limit 15
      ;  
 /*
marketing - reviews

-  cierre de acuerdo por segmento

*/     
select business_segment, count(*) as volumen
from closed_deals
group by business_segment
order by volumen desc
limit 15
;

/*
marketing - reviews

-  top 20 Fechas que tiene el mayor # de cierres

*/     

;
select won_date as fecha, count(*) as volumen
from closed_deals
group by won_date
order by volumen desc
limit 20
;

/*
marketing - reviews

- Volumen de cierre por lead type

*/      
select lead_type, count(*) as volumen
from closed_deals
group by lead_type
order by volumen desc
limit 10;





