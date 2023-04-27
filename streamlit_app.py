
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My Mother New Healthy Dinner");
streamlit.header("Breakfast Menu");
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal");
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie");
streamlit.text("🐔 Hard-Boiled Free Range-Egg");
streamlit.text("🥑🍞 Avocado Toast");

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇'");
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");

# set Fruit column as new index in dropdown multiselect
my_fruit_list = my_fruit_list.set_index('Fruit');

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits", list(my_fruit_list.index),['Avocado','Strawberries']);
fruit_to_show = my_fruit_list.loc[fruits_selected];

# Display the table in the page
streamlit.dataframe(fruit_to_show);


streamlit.header("Fruityvice Fruit Advice!");

def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.");
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()


def get_fruit_load_list():
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    fruit_data =  my_cur.fetchall()
    return fruit_data

def insert_row_snowflake(newfruit):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("INSERT INTO pc_rivery_db.public.fruit_load_list(FRUIT_NAME) VALUES('from streamlit')")
    return "Thanks for adding " + newfruit

#Add button to load the fruit
if streamlit.button('Get fruit load list'):
    streamlit.header("The fruit load list contains:")
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)


add_my_fruit = streamlit.text_input("What fruit would you like to add?","");
if streamlit.button('Add fruit to the list'):
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)
streamlit.stop()

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

