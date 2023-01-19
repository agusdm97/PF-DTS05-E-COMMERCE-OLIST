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
select c.anio, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.id)
JOIN calendario c ON(c.Fecha = o.purchase_timestamp)
group by c.anio
;
/*---------------------------------------------------------------------------------------------------------------------*/
/*
Genera los datos para la grafica de ingresos por ciudad
*/
select g.city, sum(oi.price) as total
from order_items oi
JOIN orders o ON(oi.order_id = o.id)
JOIN customers c ON(c.id = o.customer_id )
JOIN geolocations g ON(g.zip_code = c.zip_code)
group by g.city
order by total desc
limit 20
;
/*---------------------------------------------------------------------------------------------------------------------*/
/*

*/

