from flask import Flask, request
import plotly.express as px # noqa
import pandas as pd
from helper_functions import process_data # noqa
from dashboard_builder import ComponentManager, DashboardOutput # noqa

app = Flask(__name__)

df = pd.read_csv('ny_suffolk_nassau.csv')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    index_manager = ComponentManager(request)

    # Create example intput group 1 
    input_group_one = ComponentManager.create_input_group(
        manager_instance=index_manager,
        markdown_top='## From Group 1',
        inputs=[
            ComponentManager.Inputs.dropdown('hospital_selection', 'Select a condition', (df, 'Hospital Name')) # noqa
        ]
    )

    # Create example intput group 2
    input_group_two = ComponentManager.create_input_group(
        manager_instance=index_manager,
        markdown_top='## From Group 2',
        inputs=[
            ComponentManager.Inputs.slider_categorical('bed_selection', 'Select a number of beds:', ['Select All', 'hospitals < 100 beds', '100 beds >= hospitals < 300 beds', 'hospitals >= 300 beds']) # noqa
        ]
    )

    # Create example intput group 3
    intput_group_three = ComponentManager.create_input_group(
        manager_instance=index_manager,
        markdown_top='## From Group 3',
        inputs=[
            ComponentManager.Inputs.radio('net_income_selection', 'Select a net income: ', ['Positive', 'Negative']) # noqa
        ]
    )

    # Step 2: Get the user selected intput from each of the three groups 
    user_selected_1 = input_group_one.get_input('hospital_selection').value      
    user_selected_2 = input_group_two.get_input('bed_selection').value
    user_selected_3 = intput_group_three.get_input('net_income_selection').value

    # Take the user data and process the underlining dataframe based on the user selected values # noqa
    table, fig = process_data(df, [user_selected_1, user_selected_2, user_selected_3]) # noqa

    # Step 3: Create the output group
    ComponentManager.create_output_group(
        manager_instance=index_manager,
        outputs=[
            ComponentManager.Outputs.text(f"Form 1: {user_selected_1}; Form 2: {user_selected_2}; Form 3: {user_selected_3}"), # noqa
            ComponentManager.Outputs.matplotlib(fig),
            ComponentManager.Outputs.table_html(table)
        ] 
    )

    # Step 4: Return the user the outputted dashboard to show values
    return DashboardOutput(manager=index_manager).render()

if __name__ == '__main__':
    app.run(debug=True)