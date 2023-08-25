import logging
from paraview import simple
import paraview as pv

from trame.app import asynchronous
import asyncio

from PIL import Image
import io

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class mesh_Representations:
    Points = 0
    Wireframe = 1
    Surface = 2 
    SurfaceWithEdges = 3 
    
class background_Colors:  
    AliceBlue = 0
    White = 1
    LightSlateGray = 2
    LemonChiffon = 3
    CornflowerBlue = 4
 
class colormap_Representations:  
    Jet = 0
    hsv = 1
    Blue_to_Red_Rainbow = 2
    Greyscale = 3
    Cool_to_Warm = 4
 
def initialize(server, rv, time_values, timeDependence, time_keeper):
    state, ctrl = server.state, server.controller
    representation = rv.representation
    renderView = rv.view
    state.change("active_array")
    state.change("active_component")
    
    
    # Color Map Callbacks
    @state.change("contour_color_preset")
    def update_contour_color_preset(contour_color_preset, **kwargs):
        use_preset(contour_color_preset)
        ctrl.view_update_image()

    @state.change("viewMode")
    def update_view(viewMode, **kwargs):
        ctrl.view_update_image()
        if viewMode == "local":
            ctrl.view_update_geometry()
    # if timeDependence == "Transient": 
    @state.change("time")
    def update_time(time,  **kwargs):
        if len(time_values) == 0:
            return

        if time >= len(time_values):
            time = 0
            state.time = time
        time_value = time_values[time]
        time_keeper.Time =  time_value
        state.time_value = round(time_value, 6)
        # update_view(viewMode)
        ctrl.view_update_image()

    @state.change("GoToStart")
    @asynchronous.task
    async def skip_to_start(**kwargs): 
        with state:
            if state.time > 0:
                state.time = 0 
            #
            update_time(state.time)
 
    @state.change("components")
    def update_components(components,**kwargs):
        state.components = components#fields[fieldValue]['components']

    @state.change("active_component")
    def update_component_color(active_component, active_array,fields, components, viewMode="remote", **kwargs):
        if len(components) == 0:
            return
        skip_to_start()  
        componentsArray = components[active_component] 
        fieldArray      = fields[active_array]
        fieldName       = fieldArray.get("text")
        componentName   = componentsArray.get("text")
        simple.ColorBy(representation, (fieldArray.get("location"), fieldName, componentName), True) 
        representation.RescaleTransferFunctionToDataRange(True) 
        representation.SetScalarBarVisibility(renderView, False)
        nProxies = pv.servermanager.ProxyManager().GetNumberOfProxies('lookup_tables')
        for i in range(nProxies):
            proxyName = pv.servermanager.ProxyManager().GetProxyName('lookup_tables', i)
            pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).ApplyPreset('Jet', True)
            temperatureLUTColorBar = simple.GetScalarBar(pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName),renderView)  
            temperatureLUTColorBar.Title = fieldName                                   #TODO add unit to part of the input file 
            temperatureLUTColorBar.ComponentTitle =componentName 
            _min, _max = componentsArray.get("range")  
            pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).RescaleTransferFunction(_min, _max)
            # # get color legend/bar for temperatureLUT in view renderView1
            pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).UseAboveRangeColor = 1
            pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).AboveRangeColor = [0.7725490196078432, 0.7725490196078432, 0.7725490196078432]
        simple.UpdateScalarBars(view=renderView)
        update_view(viewMode)
 
    @state.change("active_array")
    def update_color_by(active_array, fields, viewMode="remote", **kwargs):
        if len(fields) == 0:
            return 
        array = fields[active_array] 
        fieldComponents= array.get("components") 
        update_components(fieldComponents)
        active_component = 0  
        update_component_color(active_component, active_array,fields, fieldComponents,viewMode)
        update_view(viewMode)

    update_color_by(0, rv.fields, "remote") 
    ctrl.view_update_image()


    @state.change("GoToPrevious")
    @asynchronous.task
    async def skip_previous(**kwargs): 
        with state:
            if state.time > 0:
                state.time -= 1 
            #
            update_time(state.time)

    @state.change("play")
    @asynchronous.task
    async def update_play(**kwargs):
        while state.play:
            with state:
                state.time += 1
                update_time(state.time)

            await asyncio.sleep(0.01)

    @state.change("GoToNext")
    @asynchronous.task
    async def skip_next(**kwargs):
        # while state.play:
        with state:
            if state.time < len(time_values)-1:
                state.time += 1
            else:
                state.time = len(time_values)-1
            update_time(state.time)

    @state.change("skipToEnd")
    @asynchronous.task
    async def skip_to_end(**kwargs):
        # while state.play:
        with state:
            if state.time < len(time_values)-1:
                state.time = len(time_values)-1
            update_time(state.time)



    @state.change("viewMode")
    def update_view(viewMode, **kwargs):
        ctrl.view_update_image()
        if viewMode == "local":
            ctrl.view_update_geometry()
    @state.change("mesh_representation")
    def update_mesh_representation(mesh_representation, **kwargs):
        update_representation( representation, mesh_representation) 
        ctrl.view_update_image()

    @ctrl.trigger("download_screenshot")
    def download_screenshot():
        simple.SaveScreenshot('/deploy/ScreenCapture.png', renderView)
        im = Image.open('/deploy/ScreenCapture.png')
        buf = io.BytesIO()
        im.save(buf,format='PNG')
        return server.protocol.addAttachment(memoryview(buf.getvalue()))
     
    @state.change("background_color")
    def update_background_color(background_color, **kwargs):
        update_backgroundcolor( renderView, background_color) 
        ctrl.view_update_image()
        
    # background color Callbacks
    def update_backgroundcolor(renderView, mode): 
        if mode == background_Colors.CornflowerBlue:
            renderView.Background = [0.392156863,0.584313725,0.929411765]
        elif mode == background_Colors.White:
            renderView.Background = [1.0, 1.0, 1.0]
        elif mode == background_Colors.LightSlateGray:
            renderView.Background = [0.466666667,0.533333333,0.6]
        elif mode == background_Colors.LemonChiffon:
            renderView.Background = [1.0,0.980392157,0.803921569]
        elif mode == background_Colors.AliceBlue: 
            renderView.Background = [0.60784313725, 0.63529411764, 0.784313725]

    # Representation Callbacks
    def update_representation(representation, mode): 
        if mode == mesh_Representations.Points:
            representation.SetRepresentationType('Points')
        elif mode == mesh_Representations.Wireframe:
            representation.SetRepresentationType('Wireframe')
        elif mode == mesh_Representations.Surface:
            representation.SetRepresentationType('Surface')
        elif mode == mesh_Representations.SurfaceWithEdges:
            representation.SetRepresentationType('Surface With Edges')


    def use_preset(preset):
        
        nProxies = pv.servermanager.ProxyManager().GetNumberOfProxies('lookup_tables')
        for i in range(nProxies):
            proxyName = pv.servermanager.ProxyManager().GetProxyName('lookup_tables', i)
            
            if preset == colormap_Representations.Jet:
                pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).ApplyPreset('Jet', True)
            elif preset == colormap_Representations.hsv:
                pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).ApplyPreset('hsv', True)
            elif preset == colormap_Representations.Blue_to_Red_Rainbow:
                pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).ApplyPreset('Blue to Red Rainbow', True)
            elif preset == colormap_Representations.Greyscale:
                pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).ApplyPreset('Grayscale', True)
            elif preset == colormap_Representations.Cool_to_Warm:
                pv.servermanager.ProxyManager().GetProxy('lookup_tables', proxyName).ApplyPreset('Cool to Warm', True)
       
  
