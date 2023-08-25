from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import trame, vuetify, paraview
{%- if cookiecutter.include_components %}
from {{cookiecutter.import_name}}.widgets import {{cookiecutter.import_name}} as my_widgets
{%- endif %}
from .ui_elements import interact_card, standard_buttons, Time_Dependent_buttons

# Create single page layout type
# (FullScreenPage, SinglePage, SinglePageWithDrawer)
def initialize(server, view, timeDependence):
    state, ctrl = server.state, server.controller
    state.trame__title = "{{cookiecutter.project_name}}"

    with SinglePageWithDrawerLayout(server) as layout:
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                view = paraview.VtkRemoteView(view, ref="view", interactive_quality=60)
                ctrl.view_reset_camera = view.reset_camera
                ctrl.view_update = view.update
                ctrl.view_update_image = view.update

    with layout:
        trame.ClientStateChange(
            value="window.location.href",
            change=(ctrl.get_href, "[window.location.href]"),
            trigger_on_create=True,
        )
        layout.title.set_text("Trame")
        with layout.toolbar:
{%- if cookiecutter.include_components %}
            my_widgets.CustomWidget(
                attribute_name="Hello",
                py_attr_name="World",
                click=self.ctrl.widget_click,
                change=self.ctrl.widget_change,
            )
            vuetify.VSpacer()
{%- endif %}
            vuetify.VSpacer()
            vuetify.VDivider(vertical=True, classes="mx-2")
            if timeDependence == "Transient":
                    Time_Dependent_buttons()

            standard_buttons()
            with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera):
                vuetify.VIcon("mdi-crop-free")

        with layout.drawer as drawer:
            drawer.width = 325
            vuetify.VDivider(classes="mb-2")
            interact_card()

        vuetify.VProgressLinear(
            indeterminate=True,
            absolute=True,
            bottom=True,
            active=("trame__busy",),
        )
