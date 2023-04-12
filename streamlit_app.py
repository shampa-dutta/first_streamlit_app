import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLRrror

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

# New Section to display fruityjuice api response

#BEFORE

# streamlit.header("Fruityvice Fruit Advice!")
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)

# #import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

# # streamlit.text(fruityvice_response.json()) #just writes the data to the screen # removing this line

# # take the json version of the response and normalise it
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# # output it the screen as a table
# streamlit.dataframe(fruityvice_normalized)

#AFTER- adding try except
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
  else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
        
 except URLError as e:
    streamlit.error()

#end of after

#dont run anything past here while we throubleshoot
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#fetch one data
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)

#fetch one data in a table
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_row)

#fetch all the rows(commenting the line with fetchone and adding fetchall)
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


#allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)


#this will not work correctly, just go with it for now
my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
