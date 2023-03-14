
import streamlit
import pandas

streamlit.title("My Mother New Healthy Dinner");
streamlit.header("Breakfast Menu");
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal");
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie");
streamlit.text("🐔 Hard-Boiled Free Range-Egg");
streamlit.text("🥑🍞 Avocado Toast");

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇'");
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits", list(my_fruit_list));

# set Fruit column as new index in dropdown multiselect
my_fruit_list = my_fruit_list.set_index('Fruit');

# Display the table in the page
streamlit.dataframe(my_fruit_list);



