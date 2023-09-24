from flask import Flask, render_template_string, request
import pandas as pd

from dashboard_builder import get_dashboard_template  # noqa: E402
from dashboard_builder.config import Config # noqa: E402
from dashboard_builder.components.inputs import InputDropdown, InputSlider_Categorical, InputRadio # noqa: E402, E501
from dashboard_builder.components.outputs import OutputText, OutputChart_Matplotlib, OutputTable_HTML, OutputImage, OutputMarkdown # noqa: E501, E402
from dashboard_builder.components.managers import ComponentManager, FormGroup # noqa: E402, E501

app = Flask(__name__)

dashboard_settings = Config(
    footer_text="Built by Hants Williams, PhD, RN - Clinical Assistant Professor - Stony Brook University, School of Health Professions - Applied Health Informatics" # noqa: E501
    )

df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/dashboard-builder/main/example_dashboards/app2/ny_suffolk_nassau.csv')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    manager = ComponentManager(request)

    # Step 1: Initialize the component manager for this request/endpoint
    manager = ComponentManager(request)

    # Step 2: Registering and capturing inputs for this request
    # We can separate these into distinct groups, so here is the first group: 
    # In this below example, we are adding/registering multiple inputs to a group 
    hospital_form_group = FormGroup(action_url='/', markdown_top="""### Select a Specific Hospital""", markdown_bottom="""*Use this section to filter by a specific hospital.*""") # noqa: E501
    input2_dropdown = InputDropdown(name='hospital_selection', label='Select a hospital:', values=(df, 'Hospital Name')) # noqa: E501
    hospital_form_group.add_inputs(input2_dropdown)
    manager.register_inputs(input2_dropdown)
    manager.register_form_groups(hospital_form_group)

    # Step 2b: Lets now create a second group of inputs
    # This one will have a dropdown based on the Number of Beds,
    #  where we have a list of <100, or >100
    # In this examle below, we are just registering a single input to a group
    hospital_form_group2 = FormGroup(action_url='/', markdown_top="""### Group by Hospital Bed Count""", markdown_bottom="""*Use this section to filter by a number of beds.*""") # noqa: E501
    input2_slider = InputSlider_Categorical(name='bed_selection', label='Select a number of beds:', categories=['Select All', 'hospitals < 100 beds', '100 beds >= hospitals < 300 beds', 'hospitals >= 300 beds']) # noqa: E501
    hospital_form_group2.add_inputs(input2_slider)
    manager.register_inputs(input2_slider)
    manager.register_form_groups(hospital_form_group2)

    # Step 2c: Lets create a dropdown that can filter if the net 
    # income is positive or negative. In this examle below, we are just registering 
    # a single input to a group
    hospital_form_group3 = FormGroup(action_url='/', markdown_top="""### Group by Net Income""", markdown_bottom="""*Use this section to filter by a net income.*""") # noqa: E501
    input2_radio = InputRadio(name='net_income_selection', label='Select a net income:', options=['Positive', 'Negative']) # noqa: E501
    hospital_form_group3.add_inputs(input2_radio)
    manager.register_inputs(input2_radio)
    manager.register_form_groups(hospital_form_group3)

    # Step 3: Do the normal python processing stuff of your data:

    # Step 4: Create the outputs for this request
    output1 = OutputMarkdown("""*Powered by [School of Health Professions - Applied Health Informatics](https://healthprofessions.stonybrookmedicine.edu/programs/ahi)* """) # noqa: E501

    # Step 5: Register the outputs to the manager
    manager.register_outputs(output1)

    # Step 6: Render the template with the inputs and outputs
    return render_template_string(
        get_dashboard_template('base'),
        form_groups=manager.render_form_groups(), 
        output_components=manager.render_outputs(),
        settings=Config()
    )

@app.route('/about')
def about():
    return 'About'
