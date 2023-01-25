import streamlit as st
import pandas as pd
import sqlalchemy as sql
import pickle as pkl


st.title('Forecasting Olist Sales')
st.header('1.-  ARIMA')

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

DF = pd.read_sql( 'select o.purchase_timestamp, oi.price from orders as o inner join order_items as oi on o.order_id = oi.order_id', con=engine)
DF['purchase_timestamp']=pd.to_datetime(DF['purchase_timestamp'])

DF.rename(columns= {'purchase_timestamp':'time', 'price':'sales'}, inplace = True)
DF.set_index('time', inplace =True)
Week_Data = DF['sales'].resample('W').sum()

Sales_per_Week = Week_Data.to_frame(name = 'sales')

from pandas.tseries.offsets import DateOffset
future_dates=[Sales_per_Week.index[-1]+ DateOffset(weeks=x)for x in range(0,32)]

future_dates_df=pd.DataFrame(index=future_dates[1:],columns=Sales_per_Week.columns)
future_df=pd.concat([Sales_per_Week,future_dates_df])

with open ('app/total_model.pkl','rb') as f:
    total_model = pkl.load(f)

date = st.select_slider('select the date', options=future_dates)

future_df['forecast'] = total_model.predict(start = 86, end = date , dynamic= True)  
prediction = st.line_chart(future_df[['sales', 'forecast']])#.plot(figsize=(12, 8))
st.write('the sales prediction is', future_df['forecast'].dropna())

st.header('2.-  Prophet')

st.header('3.-Modelo de recomendación-producto')

product = st.text_input("Field 1")

btn = st.button("predict")
def recommend_products(product_id):
        df_ml= pd.read_pickle('app/recomendacion_producto.pkl')
        filtro_aux = df_ml['product_id'] == product
        categoria = df_ml[filtro_aux]['category_name']
        group = df_ml[filtro_aux]['group']
        filtro = (df_ml['group'] == group.values[0]) & (df_ml['category_name'] == categoria.values[0]) & (df_ml['product_id']!= product)
        df =df_ml[filtro].sort_values(by='ventas_producto', ascending=False)
        return df.head(3)
if btn:
    st.write(recommend_products(product).head(3))


