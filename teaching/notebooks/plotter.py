from bqplot import pyplot
import ipywidgets

def plot(x,y,axis=[None, None, None, None], **kwargs):
    pyplot.figure()
    x_sc = pyplot.LinearScale(min=axis[0] or min(x),max= axis[1] or max(x))
    y_sc = pyplot.LinearScale(min=axis[2] or min(y),max=axis[3] or max(y))
    ax_x = pyplot.Axis(label='x', scale=x_sc, grid_lines='solid')
    ax_y = pyplot.Axis(label='u', scale=y_sc, orientation='vertical', side='left', grid_lines='solid')
    lines = pyplot.Lines(x=x, y=y, scales = {'x': x_sc, 'y': y_sc})
    plt = pyplot.Figure(layout=ipywidgets.Layout(width='auto'),
                        marks=[lines], axes=[ax_x,ax_y],
                        **kwargs)

    return plt


def video_block(f, slider_def=ipywidgets.IntSlider(value=0, min=0, max=1, step=1),
                video_def={'value':0, 'min':0, 'max':1, 'step':1}):
    """ Drive a function from a video control, with slider.

    slider_def should be an acceptable input to ipywidets.interactive.
    video_def is passed as keyword arguments to the ipywidgets.Play control.""" 

    var_name = f.__code__.co_varnames[0]
    tmp = {var_name:slider_def}
    w = ipywidgets.interactive(f, **tmp);
    slider = w.children[0]
    output = w.children[-1]

    play = ipywidgets.Play(**video_def)
    ipywidgets.jslink((play, 'value'), (slider, 'value'))

    box_layout = ipywidgets.Layout(display='flex',
                                   flex_flow='row',
                                   align_items='stretch',
                                   width='100%')

    return ipywidgets.Box([play, slider], layout=box_layout), output
    
