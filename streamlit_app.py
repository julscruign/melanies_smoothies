# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app.
st.title(":cup_with_straw: Customize You Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be; ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fuit_chosen in ingredients_list:
        ingredients_string += fuit_chosen + ' '
        st.subheader(fuit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.ORDERS(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered! '+name_on_order , icon="✅")



