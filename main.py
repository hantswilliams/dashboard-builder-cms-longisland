from flask import Flask, render_template_string, request

from dashboard_builder import get_dashboard_template  # noqa: E402
from dashboard_builder.config import Config # noqa: E402
from dashboard_builder.components.inputs import InputDropdown, InputSlider_Categorical, InputRadio # noqa: E402, E501
from dashboard_builder.components.outputs import OutputMarkdown # noqa: E501, E402
from dashboard_builder.components.managers import ComponentManager, FormGroup # noqa: E402, E501

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    manager = ComponentManager(request)

    # Step 2: Registering and capturing inputs for this request
    basic_group = FormGroup(action_url='/', markdown_top="""### Basic Inputs""", markdown_bottom="""*Test Markdown.*""")
    input1_dropdown = InputDropdown(name='dropdown1', label='Select a value:', values=['A', 'B', 'C'])
    input2_slider = InputSlider_Categorical(name='slider1', label='Select a value:', categories=['A', 'B', 'C'])
    input3_radio = InputRadio(name='radio1', label='Select a value:', options=['A', 'B', 'C'])
    basic_group.add_inputs(input1_dropdown, input2_slider, input3_radio)
    manager.register_inputs(input1_dropdown, input2_slider, input3_radio)
    manager.register_form_groups(basic_group)

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
