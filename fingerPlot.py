#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cufflinks as cf
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd

# TODO category 变量类型问题，，，解决方案一，转str类型

# class FingerPlot(object):
#     def __init__(self, offline=True, theme='ggplot'):
#         cf.set_config_file(offline=offline, world_readable=True, theme=theme)
#         pass


def _first():
    # _type_check(frame)
    pass


def _type_check(frame):
    # 检查传入类型
    pass


def _cat_to_str():
    # 未知原因，需要把Category类型数据转为str类型
    pass


def line(frame, x=None, y=None, fill=False, **kwargs):
    # 折线图
    """
    不指定x,y时，以索引为x轴，分别以其他列为y轴绘图
    只指定x时，以x为x轴，分别以其他列为y轴绘图
    只指定y时，以索引为x轴，以y列为y轴绘图

    """

    _first()
    return frame.iplot(x=x, y=y, fill=fill, **kwargs)


def scatter(frame, x=None, y=None, mode='markers', size=5, **kwargs):
    # 散点图
    """
    和line参数相近
    Parameter:
    ---------
    size:float, default 5.0
        the size of dot

    """
    return frame.iplot(kind='scatter', mode=mode, x=x, y=y, size=size, **kwargs)


def bubble(frame, x=None, y=None, size=None, text=None, **kwargs):
    # 气泡图
    """
    Parameter:
    ----------
    frame: dataFrame
    x: x axis
    y: y axis
    size: columns that the bubble size
    text: columns that the bubble description
    """
    return frame.iplot(kind='bubble', x=x, y=y, size=size, text=text, **kwargs)


def bar(frame, barmode='stack', boxpoints="outliers", **kwargs):
    # 柱形图

    return frame.iplot(kind='bar', barmode=barmode, boxpoints=boxpoints, **kwargs)


def barh(frame, barmode='stack', boxpoints="outliers", **kwargs):
    # 水平柱形图
    return frame.iplot(kind='barh', barmode=barmode, boxpoints=boxpoints, **kwargs)


def histogram(frame, barmode='stack', bins=None, histnorm=None, histfunc=None, **kwargs):
    # 频率图
    """
    barmode (overlay | group | stack)
    bins (int)
    histnorm ('' | 'percent' | 'probability' | 'density' | 'probability density')
    histfunc ('count' | 'sum' | 'avg' | 'min' | 'max')
    """
    _first()

    return frame.iplot(kind='histogram', barmode=barmode, bins=bins, histnorm=histnorm, histfunc=histfunc, **kwargs)


def scatter3d(frame, x=None, y=None, z=None, mode='markers', size=12, **kwargs):

    return frame.iplot(kind='scatter3d', x=x, y=y, z=z, mode=mode, size=size, **kwargs)


def box(frame, boxpoints="outliers", **kwargs):
    _first()
    return frame.iplot(kind='box', boxpoints=boxpoints, **kwargs)


def area(frame, fill=True, **kwargs):
    return frame.iplot(kind='area', fill=fill, **kwargs)


def pie(frame, x, **kwargs):
    # 扇形图
    frame = pd.DataFrame(frame[x].value_counts(),columns=[x]).reset_index()
    frame['index'] = frame['index'].astype('str')
    return frame.iplot(kind='pie', labels='index', values=x)


# 矩阵图
def scatter_matrix(frame, **kwargs):
    frame.scatter_matrix()
    pass


def heatmap(frame, **kwargs):
    """

    :param frame: pandas.DataFrame
    :param kwargs: other parameter
    :return: plot
    """

    return frame.corr().iplot(kind='heatmap', **kwargs)


def plot(frame):
    pass


def countplot(frame, x, hue=None, barmode="group", **kwargs):
    _first()
    if hue is None:
        data = frame[x].value_counts()
    else:
        data = pd.crosstab(frame[x], frame[hue])

    return data.iplot(kind='bar', barmode=barmode)


def lmplot(frame, x=None, y=None, hue=None, mode="markers", **kwargs):
    if hue is None:
        return scatter(frame, x=x, y=y, **kwargs)
    else:
        data = []
        for cat in pd.unique(frame[hue]):
            t = frame[frame[hue] == cat]
            data.append(go.Scatter(
                x=t[x],
                y=t[y],
                name=cat,
                mode=mode
            ))
        #             可能会在之后实现可针对不同分类的不同颜色，不同标记的方法.
        return frame.iplot(data=data, **kwargs)


def boxplot(frame, y=None, hue=None, boxpoints="outliers", **kwargs):
    # TODO 提供水平方向和垂直方向选择
    if hue is None:
        return box(frame=frame[[y]], boxpoints=boxpoints)
    else:
        data = []
        for cat in pd.unique(frame[hue]):
            t = frame[frame[hue] == cat]
            data.append(go.Box(
                y=t[y],
                name=cat,
                boxpoints=boxpoints
            ))

        return frame.iplot(data=data, **kwargs)


def jointplot(frame, x, y, color='Earth', ncontours=20,
              hist_color=(0, 0, 0.5), point_color=(0, 0, 0.5),
              point_size=2, title='2D Density Plot', height=600, width=600, **kwargs):

    fig = ff.create_2d_density(
        x=frame[x],
        y=frame[y],
        colorscale=color,
        ncontours=ncontours,
        hist_color=hist_color,
        point_color=point_color,
        point_size=point_size,
        title=title,
        height=height,
        width=width,
    )
    return frame.iplot(data=fig['data'], layout=fig['layout'], **kwargs)

# 参数    ： 参数名称        参数类型   参数说明
# 公用参数： colorscale        str                             cf.colors.get_scales().keys()
# 公用参数： title             str        Chart Title
# 公用参数： xTitle            str         X Axis Title
# 公用参数： yTitle            string      Y Axis Title
# 公用参数： zTitle            string      Z Axis Title
# 公用参数： theme             string      Layout Theme        cufflinks.getThemes()
# 公用参数： subplots          bool        separate subplots
# 公用参数： shape             tuple       shape of subplots
# 公用参数： shared_xaxes      bool        share_x
# 公用参数： shared_yaxes      bool        share_y
# 公用参数： subplot_titles    bool        子表标题
# 公用参数： legend=False      bool        是否显示图例
