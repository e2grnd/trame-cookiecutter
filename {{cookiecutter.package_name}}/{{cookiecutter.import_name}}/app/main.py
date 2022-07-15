from urllib.parse import parse_qs, urlparse

from paraview.web import venv
from trame.app import get_server
import vtkmodules.vtkRenderingOpenGL2  # noqa
from trame.app import get_server
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from . import engine, ui
from .data import download
from .render_view import RenderView


def main():
    server = get_server()
    state, ctrl = server.state, server.controller
    state.update(
        {
            "job_id": None,
        }
    )
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.OffScreenRenderingOn()

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
    renderer.ResetCamera()
    default_resolution = 6

    @ctrl.set("get_href")
    def get_href(href):
        parsed_path = urlparse(href)
        qs = parse_qs(parsed_path.query)
        if "job_id" in qs and qs["job_id"] is not None:
            job_id = qs["job_id"][0]
            state.job_id = job_id

    @state.change("job_id")
    def reload(job_id, **kwargs):
        renderer.RemoveAllViewProps()
        ctrl.view_update()
        ctrl.render()

    @ctrl.set("render")
    def render():
        if state.job_id is not None:
            value = download(state.job_id)
            rv = RenderView(renderer, value[0])
            engine.initialize(server, rv, default_resolution)
            ctrl.view_update()
            ctrl.view_reset_camera()

    ui.initialize(server, renderWindow, default_resolution)
    server.start()


if __name__ == "__main__":
    main()
