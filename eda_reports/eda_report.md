# Reporte del análisis exploratorio de datos

## 1. Tablas maestro

### Tabla: geolocations

#### Features

- **geolocation_zip_code_prefix**: Prefijo del código postal
- **geolocation_lat**: Latitud de la ubicación
- **geolocation_lng**: Longitud de la ubicación
- **geolocation_city**: Ciudad de la ubicación
- **geolocation_state**: Estado de la ubicación

#### Conclusiones

- **geolocation_lat**: Se detectaron latitudes que no pertenecen al territorio brasileño
- **geolocation_lng**: Se detectaron longitudes que no pertenecen al territorio brasileño
- **geolocation_city**: Se detectó baja normalización en los nombres de las ciudades

### Tabla: customers

#### Features

- **customer_id**: Identificador único del cliente
- **customer_unique_id**: Significado desconocido
- **customer_zip_code_prefix**: Prefijo del código postal del cliente
- **customer_city**: Ciudad del cliente
- **customer_state**: Estado del cliente

#### Conclusiones

No se detectaron problemas en los datos.

### Tabla: sellers

#### Features

- **seller_id**: Identificador único del vendedor
- **seller_zip_code_prefix**: Prefijo del código postal del vendedor
- **seller_city**: Ciudad del vendedor
- **seller_state**: Estado del vendedor

#### Conclusiones

No se detectaron problemas en los datos.

### Tabla: products

#### Features

- **product_id**: Identificador único del producto
- **product_category_name**: Categoría del producto
- **product_name_lenght**: Longitud del nombre del producto
- **product_description_lenght**: Longitud de la descripción del producto
- **product_photos_qty**: Cantidad de fotos del producto
- **product_weight_g**: Peso del producto en gramos
- **product_length_cm**: Longitud del producto en centímetros
- **product_height_cm**: Altura del producto en centímetros
- **product_width_cm**: Ancho del producto en centímetros

#### Conclusiones

- **product_name_lenght**: Se detectaron valores nulos
- **product_description_lenght**: Se detectaron valores nulos
- **product_photos_qty**: Se detectaron valores nulos

### Tabla: marketing_qualified_leads

#### Features

- **mql_id**: Identificador único del marketing qualified lead
- **first_contact_date**: Fecha del primer contacto
- **landing_page_id**: Identificador de la landing page
- **origin**: Origen del marketing qualified lead

#### Conclusiones

No se detectaron problemas en los datos.

## 2. Tablas de hechos

### Tabla: closed_deals

#### Features

- **mql_id**: Identificador único del marketing qualified lead
- **seller_id**: Identificador único del vendedor
- **sdr_id**: Identificador único del representante de desarrollo de ventas
- **sr_id**: Identificador único del representante de ventas
- **won_date**: Fecha de cierre de acuerdo
- **business_segment**: Segmento del negocio
- **lead_type**: Categoría del negocio
- **lead_behaviour_profile**: Significado desconocido
- **has_company**: El negocio es un compañía
- **has_gtin**: El producto tiene global trade item number
- **average_stock**: Stock promedio
- **business_type**: Tipo de negocio
- **declared_product_catalog_size**: Tamaño del catalogo
- **declared_monthly_revenue**: Ingresos mensuales

#### Conclusiones

- **declared_monthly_revenue**: Se detectaron valores outliers

### Tabla: orders

#### Features

- **order_id**: Identificador único de la orden
- **customer_id**: Identificador único del cliente
- **order_status**: Estado de la orden
- **order_purchase_timestamp**: Fecha de compra de la orden
- **order_approved_at**: Fecha de aprobación de la orden
- **order_delivered_carrier_date**: Fecha de entrega al transportista
- **order_delivered_customer_date**: Fecha de entrega al cliente
- **order_estimated_delivery_date**: Fecha estimada de entrega

#### Conclusiones

No se detectaron problemas en los datos.

### Tabla: orders_items

#### Features

- **order_id**: Identificador único de la orden
- **order_item_id**: Numero del item dentro de la orden
- **product_id**: Identificador único del producto
- **seller_id**: Identificador único del vendedor
- **shipping_limit_date**: Fecha limite de envío
- **price**: Precio del producto
- **freight_value**: Flete del producto

#### Conclusiones

No se detectaron problemas en los datos.

### Tabla: orders_payments

#### Features

- **order_id**: Identificador único de la orden
- **payment_sequential**: Cantidad de pagos secuenciales
- **payment_type**: Medio de pago
- **payment_installments**: Cantidad de pagos en cuotas
- **payment_value**: Total de la orden

#### Conclusiones

No se detectaron problemas en los datos.

### Tabla: orders_reviews

#### Features

- **review_id**: Identificador único de la reseña
- **order_id**: Identificador único de la orden
- **review_score**: Puntaje de la reseña
- **review_comment_title**: Titulo de la reseña
- **review_comment_message**: Mensaje de la reseña
- **review_creation_date**: Fecha de creación de la reseña
- **review_answer_timestamp**: Fecha de finalización de la reseña

#### Conclusiones

- **review_comment_title**: Se detectaron valores nulos
- **review_comment_message**: Se detectaron valores nulos
