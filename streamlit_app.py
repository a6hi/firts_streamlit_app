
import streamlit
import pandas
import snowflake.connector
import requests

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruite Advice')

def get_fruityvice_data(fruit_choice):
  fruityvise_respone = requests.get('https://fruityvice.com/api/fruit/'+fruit_choice)
  fruityvise_normalized =  pandas.json_normalize(fruityvise_respone.json())
  return fruityvise_normalized
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    result =  get_fruityvice_data(fruit_choice)
    streamlit.dataframe(result)

except URLError as e:
  streamlit.error()

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.header("Fruit load list contains:")
  streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for adding "+new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button("Add a Fruit to the List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  response = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(response)
