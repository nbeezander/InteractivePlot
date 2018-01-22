#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# create by zander on 2017-5-14
# create the class named tomato on 2017-5-19


import re
import copy
# import numpy as np
# import pandas as pd
import seaborn as sns
import ipywidgets as wgt
import matplotlib.pyplot as plt
from IPython.display import display
from pandas.core.frame import DataFrame
# from .noname import Fun
from IPython.display import clear_output
# from pandas_highcharts.display import display_charts
from config import sns_config, agg_config, chart_config, set_args_options, set_config, plotly_config
import fingerPlot as fip

# TODO 类命名 备选：peach，包命名 备选：
# TODO 多列选择方法 2017-5-21


class Fun(object):

    def __init__(self,func,tree,clear=True,**kwargs):
        # Type check
        self.func = func
        self.clear=clear
        self.tree = tree
        self.kw = kwargs
        self.kv = {}
        if not tree:
            # 初始化tree
            pass

        self.__submit = wgt.Button(
            description='Submit',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Submit',
            icon='check'
        )

        self.__submit.on_click(self.__callback)

        display(self.__submit)
        self.__box = self.create_tree(self.tree)
        display(self.__box)

    def close(self):
        self.__submit.close()
        self.__box.close()

    def __getitem__(self, item):
        return self.kv[item]

    def __setitem__(self, key, value):
        self.kv[key] = value

    def __callback(self,*args):
        kwargs = self.kw
        for k in self.kv:
            kwargs[k] = self[k].value
        # print kwargs
        if self.clear:
            clear_output(wait=True)
        self.func(**kwargs)

    def create_tree(self,node):
        if 'children' in node:
            box = getattr(wgt, node['kind'])(children=[self.create_tree(c) for c in node['children']])
            if 'titles' in node:
                for title in node['titles']:
                    box.set_title(*title)
            return box
        else:
            self[node['argname']] = getattr(wgt, node['kind'])(**node['options'])
            return self[node['argname']]

    def create_widgets(self):

        pass


class Peach(object):
    """finger Plot

    just create and use

    Parameters
    ----------
    frame : DataFrame of pandas
    feature : array-like,default None
            he columns of frame will be use,if None use all columns
    clear : bool,default True
        whether clear the Plot when draw a new Plot
    """

    def __init__(self, frame, feature=None, clear=True):
        self.version = "0.2.0"
        if not type(frame) == DataFrame:
            raise TypeError("pandas.DataFrame is the only support type by this version:%s" % self.version)

        self.clear = clear
        self.feature = [("", None)]
        if feature is not None:
            self.feature += [(f, f) for f in feature]
        else:
            self.feature += [(f, f) for f in frame.columns]

        self.frame = frame

        layout = wgt.Layout(width='20%')
        self.options = {
            "x": {"options": self.feature, "layout": layout},
            "a": {"options": self.feature, "layout": layout},
            "data": {"options": self.feature, "layout": layout},
            "data2": {"options": self.feature, "layout": layout},
            "y": {"options": self.feature, "layout": layout},
            "hue": {"options": self.feature, "layout": layout},
            "col": {"options": self.feature, "layout": layout},
            "row": {"options": self.feature, "layout": layout},
            "robust": {"layout": layout},
            "palette": {"layout": layout},
            "kind": {"layout": layout},
            "scatter": {"layout": layout},
            "ci": {"layout": layout},
            "fit_reg": {"layout": layout},
            "color": {"layout": layout},
            "orient": {"layout": layout}
        }

        self.__plot_select = wgt.Select(
            options=[("----", 0), ('jointplot', 'jointplot'), ('pairplot', 'pairplot'),
                     ('distplot', 'distplot'), ('kdeplot', 'kdeplot'), ('rugplot', 'rugplot'),
                     ('----', 0), ('lmplot', 'lmplot'), ('regplot', 'regplot'),
                     ('----', 0), ('factorplot', 'factorplot'), ('boxplot', 'boxplot'), ('violinplot', 'violinplot'),
                     ('stripplot', 'stripplot'), ('swarmplot', 'swarmplot'), ('pointplot', 'pointplot'),
                     ('barplot', 'barplot'),
                     ('countplot', 'countplot'),
                     ('----', 0), ('heatmap', 'heatmap')
                     ],
            description="Select plot type"
        )

        self.__plot_select.observe(self.__callback, names='value')
        self.__box = None
        display(self.__plot_select)

    def __callback(self, node):
        if self.__box:
            self.__box.close()
        if node['new']:
            wc = copy.deepcopy(sns_config[node['new']])
            wc = set_args_options(wc, self.options)
            # 如果放在这里，那么每次切换都需要设置一次

            method = node['new']
            if method == 'kdeplot':
                fun = kdeplot
                self.__box = Fun(self._fun_wrap, wc, frame=self.frame, fun=fun, clear=self.clear)
            else:
                if method == 'distplot':
                    fun = distplot
                elif method == 'rugplot':
                    fun = rugplot
                elif method == "heatmap":
                    fun = heatplot
                else:
                    fun = getattr(sns, node['new'])
                self.__box = Fun(self._fun_wrap, wc, data=self.frame, fun=fun, clear=self.clear)

    @staticmethod
    def _fun_wrap(fun, figsize_x=None, figsize_y=None, x_ticks_rotation=0, **kwargs):
        # TODO 如果不清除旧图的话，那么就有必要区别这些图，考虑添加opt_title字段，使用display_html添加一个标题栏 2017-5-18
        if figsize_x and figsize_y:
            plt.subplots(figsize=(figsize_x, figsize_y))
        fig = fun(**kwargs)
        #         fig.axis(ymin=0,ymax=8000)
        if x_ticks_rotation:
            plt.xticks(rotation=x_ticks_rotation)


# class Cluster(object):
#     def __init__(self, frame, feature=None, clear=True):
#         self.version = "0.02"
#         self.clear = clear
#         self.feature = [("", None)]
#         if feature is not None:
#             self.feature += [(f, f) for f in feature]
#         else:
#             self.feature += [(f, f) for f in frame.columns]
#
#         self.frame = frame
#
#         self.last_data = None
#
#         self.__fun_select = wgt.Select(
#             options=[('', None), ('groupby', 'groupby'), ('pivot', 'pivot')],
#             description="Select func : "
#         )
#         self.__config = copy.deepcopy(agg_config)
#         self.__config['groupby']['children'][0] = set_config(self.feature, prefix="x_", row_wrap=8)
#         self.__config['groupby']['children'][1] = set_config(self.feature, prefix="y_", row_wrap=8)
#         groupfun = [(0, 0), ('mean', 'mean'), ('count', 'count'), ('min', 'min'), ('max', 'max'), ('sum', 'sum')]
#         self.__config['groupby']['children'][2] = set_config(groupfun, prefix="f_")
#
#         self.option = {
#             "index": {"options": self.feature}
#         }
#         self.__chart_config = copy.deepcopy(chart_config)
#         self.__chart_config['chart']['children'][1] = set_config(self.feature, prefix="x_", row_wrap=8)
#         # print self.__config['groupby']
#
#         self.__fun_select.observe(self.__callback, names='value')
#         self.__box = None
#
#         self.__chart_box = wgt.Checkbox(
#             value=True,
#             description="Use agg data: "
#         )
#
#         display(self.__fun_select)
#
#     def __callback(self, node):
#         if self.__box:
#             self.__box.close()
#         opt = node['new']
#         if opt == 'groupby':
#             self.__box = Fun(self.__group, self.__config[opt], data=self.frame)
#         elif opt == 'pivot':
#             pass
#
#     def __group(self, data, **kwargs):
#         kw = {}
#         for k in kwargs:
#             if kwargs[k]:
#                 pre = k[:1]
#                 name = k[2:]
#                 if pre in kw:
#                     kw[pre].append(name)
#                 else:
#                     kw[pre] = [name]
#         for f in kw['y']:
#             if f not in kw['x']:
#                 kw['x'].append(f)
#         if len(kw['f']) == 1:
#             self.last_data = getattr(data[kw['x']].groupby(kw['y']), kw['f'][0])()
#         else:
#             self.last_data = getattr(data[kw['x']].groupby(kw['y']), 'agg')(kw['f'])
#         display(self.last_data)
#
#     def __pivot(self, data, **kwargs):
#
#         pass
#
#     def __use_data_callback(self):
#         pass
#
#     def chart(self):
#         # print self.__chart_config['chart']
#         wc = set_args_options(self.__chart_config['chart'], self.option)
#
#         Fun(self.__draw_chart, wc)
#
#     def __draw_chart(self, **kwargs):
#
#         if kwargs['use_temp']:
#             df = self.last_data if self.last_data is not None else self.frame
#         else:
#             col = []
#             for k in kwargs:
#                 if k.startswith("x_"):
#                     if kwargs[k]:
#                         col.append(k[2:])
#
#             if kwargs['index']:
#                 if kwargs['index'] not in col:
#                     col.append(kwargs['index'])
#                 df = self.frame[col].set_index(kwargs['index'])
#             else:
#                 df = self.frame[col]
#         kw = {
#             "kind": kwargs['kind'],
#             "chart_type": kwargs['chart_type'],
#             "polar": kwargs['polar'],
#             "legend": kwargs['legend'],
#             "figsize": (kwargs['figsizex'], kwargs['figsizey']),
#             "title": kwargs['title']
#         }
#
#         display_charts(df=df, **kw)


class Plotly(object):
    """
    support
    you can get more parameter with fingerPlot

    Parameter:
    ---------
    frame:
    feature: array-like
    clear: bool,default True
    """

    def __init__(self, frame, feature=None, clear=True):
        self.version = "0.1.0"
        if not type(frame) == DataFrame:
            raise TypeError("pandas.DataFrame is the only support type by this version:%s" % self.version)

        if feature:
            self.feature = [("", None)] + [(f, f) for f in feature]
            pass
        else:
            self.feature = [("", None)] + [(f, f) for f in frame.columns]
        self.frame = frame
        self.clear = clear
        # colorscale = fip.cf.colors.get_scales().keys()
        colorscale = [key for key in fip.cf.colors.get_scales()]
        themes = [("", None)] + [(t, t) for t in fip.cf.getThemes()]
        layout = [wgt.Layout(width='20%'), wgt.Layout(overflow="inherit")]
        self.options = {
            "x": {"options": self.feature, "layout": layout[0]},
            "y": {"options": self.feature, "layout": layout[0]},
            "z": {"options": self.feature, "layout": layout[0]},
            "col": {"options": self.feature, "layout": layout[0]},
            "hue": {"options": self.feature, "layout": layout[0]},
            "text": {"options": self.feature, "layout": layout[0]},
            # "row": {"options": self.feature, "layout": layout},
            "theme": {"options": themes, "layout": layout[0]},
            "colorscale": {"options": [""] + colorscale, "layout": layout[0]},
            "mode": {
                "options": ["lines", "markers", "lines+markers", "lines+text", "markers+text", "lines+markers+text"],
                "value": "markers"
            },
            "msg": {
                "layout": layout[1]
            }
        }

        self.method_select = wgt.Select(
            options=["", "line", "scatter", "scatter3d", "bubble", "bar", "barh", "histogram", "box", "area",
                     "countplot", "lmplot", "boxplot", "jointplot"],
            description="select method: "
        )
        self.method_select.observe(self.__callback, names="value")
        self.__box = None

        display(self.method_select)

    def __callback(self, c):
        if self.__box:
            self.__box.close()

        if c['new']:
            method = c['new']
            wc = plotly_config[method]
            wc = set_args_options(wc, self.options)
            func = getattr(fip, method)
            self.__box = Fun(self._fun_wrap, wc, clear=self.clear, frame=self.frame, fun=func)

    @staticmethod
    def _fun_wrap(fun, frame, _ix_index=None, _ix_col=None, _msg=None, sub_row=None, sub_col=None, **kwargs):
        # ix[:,:]  正则匹配
        shape = (sub_row, sub_col)
        if _ix_col is not None or _ix_col is not None:
            frame = _frame_filter(frame, _ix_index, _ix_col)
        fun(frame, shape=shape, **kwargs)


def _frame_filter(frame, index=None, col=None):
    if index is None and col is None:
        return frame

    ps = re.compile("^\\w*:\\w*(:\\d*)?$")
    psp = re.compile("^(\\w*,)*\\w+$")
    args = [None] * 6
    carr = None
    if index:
        m = ps.match(index)
        if m:
            a = m.group().split(":")
            a = a + [None] if len(a) == 2 else a
            for i in range(len(a)):
                args[i] = str(a[i]) if a[i] else None
    if col:
        if ps.match(col):
            m = ps.match(col)
            a = m.group().split(":")
            a = a + [None] if len(a) == 2 else a
            for i in range(len(a)):
                args[3 + i] = str(a[i]) if a[i] else None
        elif psp.match(col):
            m = psp.match(col)
            a = m.group().split(",")
            carr = a

    for i in range(len(args)):
        if args[i]:
            args[i] = int(args[i]) if str.isdigit(args[i]) else args[i]

    if carr:
        return frame.ix[args[0]:args[1]:args[2], carr]
    else:
        return frame.ix[args[0]:args[1]:args[2], args[3]:args[4]:args[5]]


def distplot(data, a, hist=True, kde=True, rug=False):
    return sns.distplot(data[a], hist=hist, kde=kde, rug=rug)


def kdeplot(data, data2, shade, kernel, color, frame):
    data = frame[data]
    data2 = frame[data2] if data2 else None
    return sns.kdeplot(data=data, data2=data2, shade=shade, kernel=kernel, color=color)


def rugplot(data, a, height):
    return sns.rugplot(a=data[a], height=height)


def heatplot(data, annot=True, linewidths=0, fmt=".2g"):
    return sns.heatmap(data=data.corr(), annot=annot, linewidths=linewidths, fmt=fmt)



