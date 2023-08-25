r"""
Define your classes and create the instances that you need to expose
"""
import logging
from urllib.parse import parse_qs, urlparse
from trame.app import get_server
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch #noqa
import vtkmodules.vtkRenderingOpenGL2 #noqa
from paraview import simple # type: ignore # noqa

from .render_view import RenderView
from . import engine, ui
from .data import download

{%- if cookiecutter.include_components %}
from {{cookiecutter.import_name}}.widgets import {{cookiecutter.import_name}} as my_widgets
{%- endif %}



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine:
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        self._server = server
        self._renderView = simple.GetActiveViewOrCreate("RenderView")
        self._renderView.MakeRenderWindowInteractor(True)

        # initialize state + controller
        state, ctrl = server.state, server.controller
        state.update(
            {
                "job_id": None,
            }
        )

        # Set state variable
        state.trame__title = "{{cookiecutter.project_name}}"
        state.timeDependence = "Transient"

        # Bind instance methods to controller
        ctrl.on_server_reload = self.ui
        ctrl.get_href = self.get_href
        ctrl.render = self.render
{%- if cookiecutter.include_components %}
        ctrl.widget_click = self.widget_click
        ctrl.widget_change = self.widget_change
{%- endif %}

        # Bind instance methods to state change
        state.change("job_id")(self.reload)

        # Generate UI
        self.ui()

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def show_in_jupyter(self, **kwargs):
        from trame.app import jupyter

        logger.setLevel(logging.WARNING)
        jupyter.show(self.server, **kwargs)


{%- if cookiecutter.include_components %}

    def widget_click(self):
        logger.info(">>> ENGINE(a): Widget Click")

    def widget_change(self):
        logger.info(">>> ENGINE(a): Widget Change")

{%- endif %}

    def ui(self, *args, **kwargs):
        ui.initialize(self._server, self._renderView, self.state.timeDependence)

    def get_href(self, href):
        parsed_path = urlparse(href)
        qs = parse_qs(parsed_path.query)
        if "job_id" in qs and qs["job_id"] is not None:
            job_id = qs["job_id"][0]
            self.state.job_id = job_id

    async def reload(self, job_id, **kwargs):
        self.ctrl.view_update()
        await self.ctrl.render()
        self._renderView.ResetCamera(False)
        if self.state.flag2D == "2D":
            self._renderView.InteractionMode = "2D"

    async def render(self):
        if self.state.job_id is not None:
            fileData = await download(self.state.job_id)
            rv = RenderView(fileData)
            self.state.timeDependence = rv.dataType
            animation_scene = simple.GetAnimationScene()
            animation_scene.UpdateAnimationUsingDataTimeSteps()
            time_keeper = animation_scene.TimeKeeper
            time_values = list(time_keeper.TimestepValues)
            engine.initialize(self.server, rv, time_values, self.state.timeDependence, time_keeper)
            self.state.time_value = round(time_values[0], 6)
            self.state.times = len(time_values) - 1
            self.state.fields = rv.fields
            self.state.trame__title = "Hottap"
            self.state.flag2D = rv.flag2D
            self.ctrl.view_update()
            self._renderView.ResetCamera(False)
            config_camZoom = 100 / 8  # 100/8
            cam = simple.GetActiveCamera()
            cam.Dolly(config_camZoom)

def create_engine(server=None):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    return Engine(server)

