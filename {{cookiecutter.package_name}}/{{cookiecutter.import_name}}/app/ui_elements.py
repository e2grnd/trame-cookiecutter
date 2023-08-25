from trame.widgets import vuetify
from .engine import mesh_Representations, colormap_Representations, background_Colors


def standard_footer():
    vuetify.VBtn(
        label="The Equity Engineering Group, Inc.",
        hide_details=True,
        dense=True,
    )


def Time_Dependent_buttons():
    vuetify.VCardSubtitle("Time:")

    vuetify.VTextField(
        v_model=("time_value", 0),
        disabled=True,
        hide_details=True,
        dense=True,
        style="max-width: 200px",
        outlined=True,
        classes="mx-2",
    )
    vuetify.VSlider(
        v_model=("time", 0),
        min=0,
        max=("times", 1),
        hide_details=True,
        dense=True,
        style="max-width: 200px",
    )
    vuetify.VCheckbox(
        v_model=("GoToStart", False),
        off_icon="mdi-skip-previous",
        on_icon="mdi-skip-previous",
        hide_details=True,
        dense=True,
        classes="mx-1",
    )
    vuetify.VCheckbox(
        v_model=("GoToPrevious", False),
        off_icon="mdi-rewind",
        on_icon="mdi-rewind-outline",
        hide_details=True,
        dense=True,
        classes="mx-1",
    )
    vuetify.VCheckbox(
        v_model=("play", False),
        off_icon="mdi-play",
        on_icon="mdi-stop",
        hide_details=True,
        dense=True,
        classes="mx-1",
    )
    vuetify.VCheckbox(
        v_model=("GoToNext", False),
        off_icon="mdi-fast-forward",
        on_icon="mdi-fast-forward-outline",
        hide_details=True,
        dense=True,
        classes="mx-1",
    )
    vuetify.VCheckbox(
        v_model=("skipToEnd", False),
        off_icon="mdi-skip-next",
        on_icon="mdi-skip-next",
        hide_details=True,
        dense=True,
        classes="mx-1",
    )


def standard_buttons():
    with vuetify.VTooltip("Screen Shot", bottom=True):
        with vuetify.Template(v_slot_activator="{on, attrs}"):
            with vuetify.VBtn(
                icon=True,
                click="utils.download('ScreenCapture.png',trigger('download_screenshot'),'image/png')",
                classes="ml-2",
                v_bind="attrs",
                v_on="on",
            ):
                vuetify.VIcon("mdi-camera")
    # vuetify.VCheckbox(
    #     v_model=("viewMode", "remote"),
    #     true_value="remote",
    #     false_value="local",
    #     off_icon="mdi-rotate-3d",
    #     on_icon="mdi-video-image",
    #     hide_details=True,
    #     dense=True,
    #     classes="mx-2",
    # )


# update_color_by


def ui_card(title, ui_name):
    with vuetify.VCard():
        vuetify.VCardTitle(
            title,
            classes="grey lighten-1 py-1 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            hide_details=True,
            dense=True,
        )
        content = vuetify.VCardText(classes="py-2")
    return content


#
def interact_card():
    with ui_card(title="Contours", ui_name="Controls"):
        vuetify.VSpacer()
        vuetify.VSpacer()
        vuetify.VSelect(
            # Color Map
            label="Colormap",
            v_model=("contour_color_preset", colormap_Representations.Jet),
            items=(
                "colormaps",
                [
                    {"text": "Rainbow Jet", "value": 0},
                    {"text": "hsv", "value": 1},
                    {"text": "Blue to Red Rainbow", "value": 2},
                    {"text": "Greyscale", "value": 3},
                    {"text": "Cool to Warm", "value": 4},
                ],
            ),
            hide_details=True,
            dense=True,
            outlined=True,
            classes="pt-1",
        )
        vuetify.VSpacer()
        vuetify.VSpacer()
        with vuetify.VRow(classes="pt-2", dense=True):
            with vuetify.VCol(cols="6"):
                vuetify.VSelect(
                    v_model=("active_array", 0),
                    items=("fields", []),
                    style="max-width: 200px",
                    hide_details=True,
                    dense=True,
                )
            with vuetify.VCol(cols="6"):
                vuetify.VSelect(
                    v_model=("active_component", 0),
                    items=("components", []),
                    style="max-width: 200px",
                    hide_details=True,
                    dense=True,
                )
        # vuetify.VSelect(
        #     v_model=("active_array", 0),
        #     items=("fields", []),
        #     # style="max-width: 200px",
        #     hide_details=True,
        #     dense=True,
        #     outlined=True,
        #     classes="pt-1",
        # )
    with ui_card(title="Mesh Representations", ui_name="Controls"):
        vuetify.VSpacer()
        vuetify.VSpacer()
        vuetify.VSelect(
            # Representation
            v_model=("mesh_representation", mesh_Representations.Surface),
            items=(
                "representations",
                [
                    {"text": "Points", "value": 0},
                    {"text": "Wireframe", "value": 1},
                    {"text": "Surface", "value": 2},
                    {"text": "SurfaceWithEdges", "value": 3},
                ],
            ),
            # label="Mesh Representations",
            hide_details=True,
            dense=True,
            outlined=True,
            classes="pt-1",
        )

    with ui_card(title="Background Color", ui_name="Controls"):
        vuetify.VSpacer()
        vuetify.VSpacer()
        vuetify.VSelect(
            # Representation
            v_model=("background_color", background_Colors.CornflowerBlue),
            items=(
                "backgroundcolor",
                [
                    {"text": "AliceBlue", "value": 0},
                    {"text": "White", "value": 1},
                    {"text": "LightSlateGray", "value": 2},
                    {"text": "LemonChiffon", "value": 3},
                    {"text": "CornflowerBlue", "value": 4},
                ],
            ),
            # label="Mesh Representations",
            hide_details=True,
            dense=True,
            outlined=True,
            classes="pt-1",
        )
