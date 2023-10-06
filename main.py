from flask import Flask, request
from dashboard_builder import ComponentManager, DashboardOutput # noqa

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    index_manager = ComponentManager(request)

    index_manager.template_defaults(
        page_title="Plotly Test Data",
        footer_text="Built by Hants Williams - Plotly Example - Powered by Dashboard Builder", # noqa
        theme='dark',
    )

    ComponentManager.create_output_group(
        manager_instance=index_manager,
    )

    return DashboardOutput(manager=index_manager).render()

if __name__ == "__main__":
    app.run(debug=True)
