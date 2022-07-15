import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def initialize(server, rv, default_resolution):
    state, ctrl = server.state, server.controller

    @state.change("resolution")
    def update_cone(resolution=default_resolution, **kwargs):
        rv.cone_source.SetResolution(resolution)
        ctrl.view_update()

    @ctrl.set("update_reset_resolution")
    def update_reset_resolution():
        state.resolution = default_resolution
