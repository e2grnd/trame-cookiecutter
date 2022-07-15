from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import trame, vuetify, vtk
{%- if cookiecutter.include_components %}
from {{cookiecutter.import_name}}.widgets import {{cookiecutter.import_name}} as my_widgets
{%- endif %}


# Create single page layout type
# (FullScreenPage, SinglePage, SinglePageWithDrawer)
def initialize(server, renderWindow, default_resolution):
    state, ctrl = server.state, server.controller
    state.trame__title = "{{cookiecutter.project_name}}"

    with SinglePageWithDrawerLayout(server) as layout:
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                view = vtk.VtkRemoteView(renderWindow, interactive_ratio=(1,))
                ctrl.view_reset_camera = view.reset_camera
                ctrl.view_update = view.update

    with layout:
        trame.ClientStateChange(
            value="window.location.href",
            change=(ctrl.get_href, "[window.location.href]"),
            trigger_on_create=True,
        )
        layout.title.set_text("TBreak")
        with layout.toolbar:
            vuetify.VSpacer()
            vuetify.VDivider(vertical=True, classes="mx-2")
            vuetify.VSlider(
                v_model=("resolution", default_resolution),
                min=3,
                max=60,
                step=1,
                hide_details=True,
                dense=True,
                style="max-width: 300px",
            )
            vuetify.VDivider(vertical=True, classes="mx-2")
            with vuetify.VBtn(icon=True, click=ctrl.update_reset_resolution):
                vuetify.VIcon("mdi-undo-variant")

        with layout.drawer as drawer:
            drawer.width = 325
            vuetify.VDivider(classes="mb-2")
