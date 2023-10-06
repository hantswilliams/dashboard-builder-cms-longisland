from flask import Flask, request
import plotly.express as px
import pandas as pd
from dashboard_builder import ComponentManager, DashboardOutput # noqa

app = Flask(__name__)

df = pd.DataFrame({
    'condition': ['Rheumatoid arthritis', 'Osteoarthritis', 'Osteoporosis', 'Fibromyalgia'], # noqa
    'frequency': [10, 15, 8, 7]
})

@app.route('/', methods=['GET', 'POST'])
def index():

    index_manager = ComponentManager(request)

    index_manager.template_defaults(
        page_title="Plotly Test Data",
        footer_text="Built by Hants Williams - Plotly Example - Powered by Dashboard Builder", # noqa
        theme='dark',
    )

    input_group = ComponentManager.create_input_group(
        manager_instance=index_manager,
        inputs=[
            ComponentManager.Inputs.dropdown('condition_selection', 'Select a condition: ', (df, 'condition')) # noqa 
        ]
    )

    user_selected_1 = input_group.get_input('condition_selection').value

    selected_condition = df['condition'] == user_selected_1 if user_selected_1 != 'Select All' else None # noqa

    if selected_condition is not None:
        colors = ['Selected' if cond else 'Not Selected' for cond in selected_condition]
    else:
        colors = ['Not Selected'] * len(df)

    fig = px.bar(
        df,
        x='condition',
        y='frequency',
        color=colors,
        color_discrete_map={"Not Selected": "#A0AEC0", "Selected": "#48BB78"}  
    )

    ComponentManager.create_output_group(
        manager_instance=index_manager,
        outputs=[
            ComponentManager.Outputs.text(f"Value selected: {user_selected_1}"),
            ComponentManager.Outputs.plotly(fig)
        ]
    )

    return DashboardOutput(manager=index_manager).render()

if __name__ == "__main__":
    app.run(debug=True)
