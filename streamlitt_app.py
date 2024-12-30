# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your Custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be: ', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list = st.multiselect('Choose up to 5 ingredients:', 
                                 my_dataframe,
                                max_selections = 5)

if ingredient_list:
    ingredients_string = ''

    for fruit in ingredient_list:
        ingredients_string += fruit + ' '


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""


    time_to_insert = st.button('Submit')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
