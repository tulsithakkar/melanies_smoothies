# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose The fruits you want you in custom Snoothie!.
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on smoothie will be:", name_on_order)


#session = get_active_session()
cnx=st.connection("snowflake")
session= cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert the snowpark dataframe to a pandas so we can use LOC location
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'choose up to 5 ingredient',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string=''
    for choosen_fruit in ingredients_list:
        ingredients_string += choosen_fruit + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == choosen_fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', choosen_fruit,' is ', search_on, '.')
        st.subheader(choosen_fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ search_on)
        fv_df = st.dataframe(data=fruityvice_response.json() , use_container_width=True)
    st.write(ingredients_string); 
    #insert into smoothies.public.orders(name_on_order,ingredients) values('abc','abc guava cherry');
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients) values
    ('""" + name_on_order + """','""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('submit order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")
        

