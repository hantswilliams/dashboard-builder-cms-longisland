from flask import Flask, request
import plotly.express as px # noqa
import pandas as pd
import altair as alt
from helper_functions import process_data # noqa
from dashboard_builder import ComponentManager as dbcm # noqa
from dashboard_builder import DashboardOutput # noqa 

df = pd.read_csv('ny_suffolk_nassau.csv') # noqa

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    index_manager = dbcm(request)

    # Step1b: Configure anything you want configured
    index_manager.template_defaults(
        page_title="CMS 2019 Data",
        footer_text="Built by Hants Williams - Condition Frequency Count Dashboard - Powered by Dashboard Builder", # noqa
        theme='light',
    )

    # Create example intput group 1 
    input_group_one = dbcm.create_input_group(
        manager_instance=index_manager,
        markdown_top='## From Group 1',
        inputs=[
            dbcm.Inputs.dropdown('hospital_selection', 'Select a condition', (df, 'Hospital Name')) # noqa
        ]
    )

    # Create example intput group 2
    input_group_two = dbcm.create_input_group(
        manager_instance=index_manager,
        markdown_top='## From Group 2',
        inputs=[
            dbcm.Inputs.slider_categorical('bed_selection', 'Select a number of beds:', ['Select All', 'hospitals < 100 beds', '100 beds >= hospitals < 300 beds', 'hospitals >= 300 beds']) # noqa
        ]
    )

    # Create example intput group 3
    intput_group_three = dbcm.create_input_group(
        manager_instance=index_manager,
        markdown_top='## From Group 3',
        inputs=[
            dbcm.Inputs.radio('net_income_selection', 'Select a net income: ', ['Positive', 'Negative']) # noqa
        ]
    )

    # Step 2: Get the user selected intput from each of the three groups 
    user_selected_1 = input_group_one.get_input('hospital_selection').value      
    user_selected_2 = input_group_two.get_input('bed_selection').value
    user_selected_3 = intput_group_three.get_input('net_income_selection').value

    # Take the user data and process the underlining dataframe based on the user selected values # noqa
    table, fig = process_data(df, [user_selected_1, user_selected_2, user_selected_3]) # noqa

    # Create dummy altair chart for testing altair parameters 
    altair_sample_chart = alt.Chart(df, width=500, height=500).mark_bar().encode(x='Hospital Name',y='Net Income') # noqa

    # Step 3: Create the output group

    ## Create 2 column test for output
    columnSection1 = dbcm.Layouts.column(2)
    columnSection1.add_to_column(0, 
                             dbcm.Outputs.text("This is some placeholder text for the first row in column 1"), # noqa 
                             dbcm.Outputs.markdown("""<br />"""),
                             dbcm.Outputs.text("Now we are in row 2 for column 1, and this is some more example text")) #noqa 
    columnSection1.add_to_column(1, dbcm.Outputs.text("Column 2 begins here. This is text for populating the only and only row that exists in Column 2")) #noqa

    dbcm.create_output_group(
        manager_instance=index_manager,
        outputs=[
            dbcm.Outputs.markdown("""#CMS Hospital Provider Cost Report 2019"""), #noqa 
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###Expander Example Section"""),
            dbcm.Layouts.expander(
                label = 'About the Dataset...1',
                id = 'dataset_description_1',
                components=[
                    dbcm.Outputs.markdown("""The following data originates from [data.cms.gov](https://data.cms.gov/provider-compliance/cost-report/hospital-provider-cost-report), and is a subset of the data for Suffolk and Nassau County. The data is from 2019 and is the most recent data available. This data is gathered from the hospital annual cost report information maintained in the Healthcare Provider Cost Reporting Information System (HCRIS). The data does not contain all measures reported in the HCRIS, but rather includes a subset of commonly used measures."""), # noqa: E501,
                    dbcm.Outputs.markdown("""In this example, we show how visualization can be a powerful tool when exploring data. The government provides a lot of data, but it can be difficult to understand and interpret. By using visualization, we can quickly see the distribution of the data. Using  the dropdowns below, you can filter the data by hospital, number of beds, and net income. The bar chart will update to show the filtered data. The table below the chart will show the filtered data as well. The table can be sorted by clicking on the column headers."""), # noqa: E501
                    dbcm.Outputs.markdown("""Please be aware that this data is for 2019 (pre-covid). Since we focus on net income, it is calculated by: subtracting Total Other Expenses (G3-Line-28-Column-1) from Total Income (G3-Line-26-Column-1) reported on the Statement of Revenues and Expenses (Worksheet-G-3).The complete data dictionary can be found [here](https://data.cms.gov/resources/hospital-provider-cost-report-data-dictionary).""") # noqa: E501)
                ]
            ),
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###Column Example Section"""),
            columnSection1, 
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###Markdown Example Section"""),
            dbcm.Outputs.markdown(f"""**Form Group 1 Selection**: {user_selected_1} 
                                  <br /> 
                                  **Form Group 2 Selection**: {user_selected_2} 
                                  <br />
                                  **Form Group 3 Selection**: {user_selected_3}"""),
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###Matplotlib Example Section"""),
            dbcm.Outputs.matplotlib(fig),
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###Altair Example Section"""),
            dbcm.Outputs.altair(altair_sample_chart, 'Altair Chart: Default View for DF', 'altair321'), # noqa
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###Table Example Section"""),
            dbcm.Outputs.table_html(table),
            dbcm.Outputs.markdown("""---"""),
            dbcm.Outputs.markdown("""###More Expander Examples Section"""),
            dbcm.Layouts.expander(
                label = 'About the Dataset Part...2',
                id = 'dataset_description_part_2',
                components=[
                    dbcm.Outputs.markdown("""This is a test for unique text 2a"""), # noqa: E501,
                    dbcm.Outputs.markdown("""This is a test for unique text 2b"""), # noqa: E501
                    dbcm.Outputs.markdown("""This is a test for unique text 2c""") # noqa: E501)
                ]
            ),
        ] 
    )

    dbcm.create_output_group(
        manager_instance=index_manager,
        outputs=[
            dbcm.Layouts.expander(
                label = 'About the Dataset Part...3',
                id = 'dataset_description_part_3',
                components=[
                    dbcm.Outputs.markdown("""This is a test for unique text 3a"""), # noqa: E501,
                    dbcm.Outputs.markdown("""This is a test for unique text 3b"""), # noqa: E501
                    dbcm.Outputs.markdown("""This is a test for unique text 3c""") # noqa: E501)
                ]
            ),
        ]
    )

    # Step 4: Return the user the outputted dashboard to show values
    return DashboardOutput(
        manager=index_manager,
        # template_name='base_nosidebar',
        ).render() # noqa

if __name__ == '__main__':
    app.run(debug=True)