#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

# TODO 可定制的figsize 2017-5-18 achieved on 2017-5-18
# TODO 添加可调整plt参数的控件(标签，背景颜色，标签旋转)
# x_ticks rotation achieved on 2017-5-18

version = "0.2.0"
x = {"kind": "Select", "argname": "x", "options": {"options": [], "description": " X: "}}
a = {"kind": "Select", "argname": "a", "options": {"options": [], "description": " a: "}}
y = {"kind": "Select", "argname": "y", "options": {"options": [], "description": " Y: "}}
hue = {"kind": "Select", "argname": "hue", "options": {"options": [], "description": " Hue: "}}
col = {"kind": "Select", "argname": "col", "options": {"options": [], "description": " Col: "}}
row = {"kind": "Select", "argname": "row", "options": {"options": [], "description": " Row: "}}
legend = {"kind": "Checkbox", "argname": "legend", "options": {"description": "legend: ", "value": True}}
robust = {"kind": "Checkbox", "argname": "robust", "options": {"description": "robust: ", "value": False}}
sharex = {"kind": "Checkbox", "argname": "sharex", "options": {"description": "sharey: ", "value": True}}
sharey = {"kind": "Checkbox", "argname": "sharey", "options": {"description": "sharey: ", "value": True}}
orient = {"kind": "Select", "argname": "orient",
          "options": {"options": [("", None), ("vertical", "v"), ("horizontal", "h")], "description": "orient: "}}

# markers 可能为list，暂时不处理
# markers = {"kind": "Select", "argname": "markers", "options": {"option":["D","o"],"description": "markers"}}
# linestyle = {"kind": "Select", "argname": "markers", "options": {"option":[],"description": "markers"}}
palette = {"kind": "Select", "argname": "palette",
           "options": {"options": [
               ("default", None), ("Set1", "Set1"), ("Set2", "Set2"), ("Set3", "Set3"), ("muted", "muted"),
               ('Blues_d', 'Blues_d'), ("Blues", "Blues"), ("BuGn_r", "BuGn_r"), ("GnBu_d", "GnBu_d"),
               ("RdBu", "RdBu"), ("Paired", "Paired")
           ],
               "description": "palette: "
           }}

dist_hist = {"kind": "Checkbox", "argname": "hist", "options": {"description": "hist: ", "value": True}}
dist_kde = {"kind": "Checkbox", "argname": "kde", "options": {"description": "kde: ", "value": True}}
dist_rug = {"kind": "Checkbox", "argname": "rug", "options": {"description": "rug: ", "value": False}}

lm_scatter = {"kind": "Checkbox", "argname": "scatter", "options": {"description": "scatter: ", "value": True}}
lm_fit_reg = {"kind": "Checkbox", "argname": "fit_reg", "options": {"description": "fit_reg: ", "value": True}}
logistic = {"kind": "Checkbox", "argname": "logistic", "options": {"description": "logistic: ", "value": False}}
lowess = {"kind": "Checkbox", "argname": "lowess", "options": {"description": "lowess: ", "value": True}}
x_bins = {"kind": "Select", "argname": "x_bin",
          "options": {"description": "x_bins", "options": [("default", None), (3, 3), (5, 5), (8, 8), (12, 12)]}}

violin_split = {"kind": "Checkbox", "argname": "split", "options": {"value": False, "description": "split: "}}
violin_scale = {"kind": "Select", "argname": "scale",
                "options": {"options": [("", None), ("area", "area"), ("count", "count"), ("width", "width")],
                            "description": "scale: ", "value": "count"}}
violin_inner = {"kind": "Select", "argname": "inner",
                "options": {"options": [("", None), ("box", "box"), ("quartile", "quartile"), ("point", "point"),
                                        ("stick", "stick")],
                            "description": "inner: ", "value": "box"}}

jitter = {"kind": "FloatSlider", "argname": "jitter",
          "options": {"min": 0, "max": 0.2, "step": 0.01, "description": "jitter: "}}

#
dodge = {"kind": "Checkbox", "argname": "dodge", "options": {"value": False, "description": "dodge: "}}
join = {"kind": "Checkbox", "argname": "join", "options": {"value": True, "description": "join: "}}

# heatmap
annot = {"kind": "Checkbox", "argname": "annot", "options": {"value": True, "description": "annot: "}}
fmt = {"kind": "Select", "argname": "fmt",
       "options": {"options": ["d", "0.1f", "0.2f", "0.3f", "0.4f", "0.2g"], "value": "0.2g",
                   "description": "format"}}
linewidths = {"kind": "IntSlider", "argname": "linewidths",
              "options": {"min": 0, "max": 10, "description": "linewidths: "}}

color = {"kind": "ColorPicker", "argname": "color", "options": {"description": "color: ", "value": "#4c72b0"}}

ci = {"kind": "IntSlider", "argname": "ci",
      "options": {"min": 0, "max": 100, "value": 95, "description": "ci: "}}

figure = {
    "kind": "HBox",
    "children": [
        {"kind": "IntSlider", "argname": "figsize_x", "options": {
            "min": 4, "max": 16, "value": 8, "description": "figsize_X: "}},
        {"kind": "IntSlider", "argname": "figsize_y", "options": {
            "min": 4, "max": 12, "value": 6, "description": "figsize_Y: "}},
        {"kind": "IntSlider", "argname": "x_ticks_rotation", "options": {
            "min": -90, "max": 90, "step": 15, "value": 0, "description": "X_ticks_rotation: "}},
    ]
}


# TODO 确认copy deepcopy的区别


def node(kind, argname, desc, **kwargs):
    return {"kind": kind, "argname": argname, "options": dict({"description": desc}, **kwargs)}


sns_config = {
    "jointplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x,
                    y,
                    # copy.deepcopy(palette),
                    {"kind": "Select", "argname": "kind",
                     "options": {"options": ["scatter", "reg", "resid", "kde", "hex"], "description": " kind :"}}
                ],
            }, figure
        ],
        "titles": [(0, "parameter"), (1, "figure")]
    },
    "pairplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    hue,
                    palette,
                    {"kind": "Select", "argname": "kind",
                     "options": {"options": ["scatter", "reg"], "description": " kind :"}}
                ]}
        ],
        "titles": [(0, "parameter")]
    },
    "distplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    a,
                    dist_hist,
                    dist_kde,
                    dist_rug
                ]
            }, figure
        ],
        "titles": [(0, "parameter"), (1, "figure")]
    },
    "kdeplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    {"kind": "Select", "argname": "data", "options": {"options": [], "description": " X :"}},
                    {"kind": "Select", "argname": "data2", "options": {"options": [], "description": " Y :"}},
                ]
            }, {
                "kind": "HBox",
                "children": [
                    {"kind": "Checkbox", "argname": "shade", "options": {"value": False, "description": "shade :"}},
                    {"kind": "Select", "argname": "kernel",
                     "options": {"options": ["gau", "cos", "biw", "epa", "tri", "triw"], "description": "kernel : "}},
                    color
                ]
            }, figure

        ],
        "titles": [(0, "columns"), (1, "parameter"), (2, "figure")]
    },
    "rugplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    copy.deepcopy(a),
                    {"kind": "FloatSlider", "argname": "height",
                     "options": {"min": 0.05, "max": 1.0, "step": 0.05, "value": 0.05, "description": "height : "}}
                ]
            }, figure
        ],
        "titles": [(0, "parameter"), (1, "figure")]
    },

    "lmplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    copy.deepcopy(x),
                    copy.deepcopy(y),
                    copy.deepcopy(hue),
                    copy.deepcopy(col),
                    copy.deepcopy(row),
                ]},
            {
                "kind": "HBox",
                "children": [
                    copy.deepcopy(palette),
                    copy.deepcopy(lm_scatter),
                    copy.deepcopy(lm_fit_reg),
                    copy.deepcopy(ci),
                    copy.deepcopy(robust)
                ]
            }
        ],
        "titles": [(0, "columns"), (1, "parameter")]
    },
    "regplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    copy.deepcopy(x),
                    copy.deepcopy(y),
                    copy.deepcopy(ci),
                    copy.deepcopy(color)
                ]
            }, {
                "kind": "HBox",
                "children": [
                    copy.deepcopy(lm_scatter),
                    copy.deepcopy(lm_fit_reg),
                    copy.deepcopy(logistic),
                    copy.deepcopy(robust)
                ]
            }
        ],
        "titles": [(0, "columns"), (1, "parameter")]
    },

    "factorplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue, col, row
                ]
            }, {
                "kind": "HBox",
                "children": [
                    ci,
                    {"kind": "Select", "argname": "kind",
                     "options": {"options": ["point", "bar", "count", "box", "violin", "strip"],
                                 "description": "kind: "}},
                    orient, sharex, sharey
                ]
            }
        ],
        "titles": [(0, "data"), (1, "parameter")]
    },
    "boxplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    orient, color, palette
                ]
            }, figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },
    "violinplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue, violin_split
                ]
            }, {
                "kind": "HBox",
                "children": [
                    violin_scale, violin_inner, orient, color, palette
                ]
            }, figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },
    "stripplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    # color
                    jitter, palette, violin_split
                ]
            }, figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },
    "swarmplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    # color
                    palette, violin_split
                ]
            }, figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },
    "pointplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    # color
                    dodge, join, color, palette, ci
                ]
            }, figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },
    "barplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    # color
                    color, palette, ci
                ]
            }, figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },
    "countplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    # color
                    color, palette
                ]
            },
            figure
        ],
        "titles": [(0, "data"), (1, "parameter"), (2, "figure")]
    },

    "heatmap": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    annot, fmt, linewidths
                ]
            }, figure
        ],
        "titles": [(0, "parameter"), (1, "figure")]
    },
}

agg_config = {
    "groupby": {
        "kind": "Tab",
        "children": [
            {
                "kind": "zzz"
            }, {
                "kind": "zzz"
            }, {
                "kind": "func"
            }
        ],
        "titles": [(0, "select"), (1, "by"), (2, 'func')]
    },
    "pivot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "sss"
            }, {
                "kind": "sss"
            }, {
                "kind": "HBox",
                "children": [
                    node("Select", "values", "value: "),
                    node("Select", "aggfunc", "aggfunc: ")
                ]
            }
        ],
        "titles": [(0, "index"), (1, "columns"), (2, "parameter")]
    }

}

chart_config = {
    "chart": {
        "kind": "Tab",
        "children": [
            {"kind": "Checkbox", "argname": "use_temp", "options": {"value": True, "description": "Use agg data: "}},
            {
                "kind": "sss"
            }, {
                "kind": "HBox",
                "children": [
                    {"kind": "Select", "argname": "index", "options": {"options": [], "description": "Index: "}},
                    {"kind": "Select", "argname": "kind", "options": {
                        "options": [('line', 'line'), ('bar', 'bar'), ('barh', 'barh'), ('pie', 'pie')],
                        "description": "Kind: "
                    }},
                    {"kind": "Select", "argname": "chart_type", "options": {
                        "options": [('default', 'default'), ('stock', 'stock')],
                        "description": "chart_type: "
                    }},
                    {"kind": "Checkbox", "argname": "polar", "options": {"value": False, "description": "polar: "}},
                    {"kind": "Checkbox", "argname": "legend", "options": {"value": True, "description": "legend: "}},
                    {"kind": "Select", "argname": "theme", "options": {"options": ["default"], "disabled": True,
                                                                       "description": "Theme: "}}
                ]
            }, {
                "kind": "HBox",
                "children": [
                    {"kind": "IntSlider", "argname": "figsizex",
                     "options": {"min": 400, "max": 1200, "value": 975, "description": "X Size: "}},
                    {"kind": "IntSlider", "argname": "figsizey",
                     "options": {"min": 200, "max": 600, "value": 400, "description": "Y Size: "}}
                ]
            }, {
                "kind": "Text", "argname": "title",
                "options": {"placeholder": "chart title", "value": "My Chart", "description": "Title"}
            }
        ],
        "titles": [(0, "Data"), (1, "Columns"), (2, "Parameter"), (3, "Figure"), (4, "Title")]
    }
}

plotly_default = {
    "z": {
        "kind": "Select",
        "argname": "z",
        "options": {
            "options": [],
            "description": "Z: "
        }
    },
    "text": {
        "kind": "Select",
        "argname": "text",
        "options": {
            "options": [],
            "description": "text: "
        }
    },
    "size": {
        "kind": "IntSlider",
        "argname": "size",
        "options": {
            "min": 5,
            "max": 20,
            "value": 5,
            "description": "dot size: "
        }
    },
    "bubble_col": {
        "kind": "Select",
        "argname": "col",
        "options": {
            "options": [],
            "description": "bubble_col: "
        }
    },
    "mode": {
        "kind": "Select",
        "argname": "mode",
        "options": {
            "options": [],
            "description": "mode"
        }
    },
    "barmode": {
        "kind": "Select",
        "argname": "barmode",
        "options": {
            "options": ["stack", "group", "overlay"],
            "description": "barmode: "
        }
    },
    "boxpoints": {
        "kind": "Select",
        "argname": "boxpoints",
        "options": {
            "options": ["","outliers", "all", "suspectedoutliers", "False"],
            "value": "outliers",
            "description": "boxpoints"
        }
    },
    "bins": {
        "kind": "IntSlider",
        "argname": "bins",
        "options": {
            "min": 0,
            "max": 100,
            "value": 0,
            "description": "bins: "
        }
    },

    "fill": {
        "kind": "Checkbox",
        "argname": "fill",
        "options": {
            "value": False,
            "description": "fill: "
        }
    },

    "subplots": {
        "kind": "Checkbox",
        "argname": "subplots",
        "options": {
            "value": False,
            "description": "subplots: "
        }
    },
    "sub_row": {
        "kind": "IntSlider",
        "argname": "sub_row",
        "options": {
            "min": 1,
            "max": 6,
            "value": 3,
            "description": "sub_row: "
        }
    },
    "sub_col": {
        "kind": "IntSlider",
        "argname": "sub_col",
        "options": {
            "min": 1,
            "max": 6,
            "value": 2,
            "description": "sub_col: "
        }
    },
    "sub_title": {
        "kind": "Checkbox",
        "argname": "subplot_titles",
        "options": {
            "value": True,
            "description": "sub_titles: "
        }
    },
    "share_x": {
        "kind": "Checkbox",
        "argname": "shared_xaxes",
        "options": {
            "value": False,
            "description": "share_x: "
        }
    },
    "share_y": {
        "kind": "Checkbox",
        "argname": "shared_yaxes",
        "options": {
            "value": False,
            "description": "share_y: "
        }
    },

    "theme": {
        "kind": "Select",
        "argname": "theme",
        "options": {
            "options": [],
            "description": "Theme: "
        }
    },
    "title": {
        "kind": "Text",
        "argname": "title",
        "options": {
            "placeholder": "Chart Title",
            "description": "Chart Title: "
        }
    },
    "colorscale": {
        "kind": "Select",
        "argname": "colorscale",
        "options": {
            "options": [],
            "description": "colorscale: "
        }
    },
    "legend": {
        "kind": "Checkbox",
        "argname": "legend",
        "options": {
            "value": True,
            "description": "Legend: "
        }
    },

    "_msg": {
        "kind": "Label",
        "argname": "_msg",
        "options": {
            "value": "Please don't use the function on big datasets,maybe the return value isn`t you expected, "
                     "In my opinion,The method should only be used for aggregated data . "
                     "I will be implement some function for aggregated data in the future."}}
}

subplots = {
    "kind": "HBox",
    "children": [
        plotly_default.get("subplots"),
        plotly_default.get("sub_row"),
        plotly_default.get("sub_col"),
        plotly_default.get("sub_title"),
        plotly_default.get("share_x"),
        plotly_default.get("share_y"),
    ]
}
plot_chart = {
    "kind": "HBox",
    "children": [
        plotly_default.get("title"),
        plotly_default.get("colorscale"),
        plotly_default.get("legend"),
        plotly_default.get("theme"),
    ]
}

ix_filter = {
    "kind": "HBox",
    "children": [
        {
            "kind": "Label",
            "argname": "_msg",
            "options": {
                "value": "ix: "
            }
        }, {
            "kind": "Text",
            "argname": "_ix_index",
            "options": {
                "placeholder": "1:50:2 or a:f:2 "
            }
        }, {
            "kind": "Text",
            "argname": "_ix_col",
            "options": {
                "placeholder": "1:5:2 or A:C or A,B,C"
            }
        }
    ]
}

PLOTLY_SCALES = {'Greys': ['rgb(0,0,0)', 'rgb(255,255,255)'],
                 'YlGnBu': ['rgb(8,29,88)', 'rgb(255,255,217)'],
                 'Greens': ['rgb(0,68,27)', 'rgb(247,252,245)'],
                 'YlOrRd': ['rgb(128,0,38)', 'rgb(255,255,204)'],
                 'Bluered': ['rgb(0,0,255)', 'rgb(255,0,0)'],
                 'RdBu': ['rgb(5,10,172)', 'rgb(178,10,28)'],
                 'Reds': ['rgb(220,220,220)', 'rgb(178,10,28)'],
                 'Blues': ['rgb(5,10,172)', 'rgb(220,220,220)'],
                 'Picnic': ['rgb(0,0,255)', 'rgb(255,0,0)'],
                 'Rainbow': ['rgb(150,0,90)', 'rgb(255,0,0)'],
                 'Portland': ['rgb(12,51,131)', 'rgb(217,30,30)'],
                 'Jet': ['rgb(0,0,131)', 'rgb(128,0,0)'],
                 'Hot': ['rgb(0,0,0)', 'rgb(255,255,255)'],
                 'Blackbody': ['rgb(0,0,0)', 'rgb(160,200,255)'],
                 'Earth': ['rgb(0,0,130)', 'rgb(255,255,255)'],
                 'Electric': ['rgb(0,0,0)', 'rgb(255,250,220)'],
                 'Viridis': ['rgb(68,1,84)', 'rgb(253,231,37)']}

plotly_config = {
    "line": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y
                ]
            }, {
                "kind": "HBox",
                "children": [
                    plotly_default.get("fill"),
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "scatter": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y
                ]
            }, {
                "kind": "HBox",
                "children": [
                    plotly_default.get("mode"),
                    plotly_default.get("size")
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "bubble": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x, y, plotly_default.get("bubble_col"), plotly_default.get("text")
                ]
            }, {
                "kind": "HBox",
                "children": [
                    {"kind": "Label", "argname": "_msg", "options": {"value": "nothing "}}
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "bar": {
        "kind": "Tab",
        "children": [
            ix_filter,
            {
                "kind": "HBox",
                "children": [
                    plotly_default.get("barmode"),
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "barh": {
        "kind": "Tab",
        "children": [
            ix_filter,
            {
                "kind": "HBox",
                "children": [
                    plotly_default.get("barmode"),
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "histogram": {
        "kind": "Tab",
        "children": [
            ix_filter,
            {
                "kind": "HBox",
                "children": [
                    plotly_default.get("barmode"),
                    plotly_default.get("bins")
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "box": {
        "kind": "Tab",
        "children": [
            ix_filter,
            {
                "kind":"HBox",
                "children": [
                     plotly_default.get("boxpoints")
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },

    "countplot":{
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x,hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    plotly_default.get("barmode")
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "lmplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x,y,hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    plotly_default.get("mode")
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "boxplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    y,hue
                ]
            }, {
                "kind": "HBox",
                "children": [
                    plotly_default.get("boxpoints")
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    },
    "jointplot": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x,y,
                ]
            }, {
                "kind": "HBox",
                "children": [
                    # {"kind": "IntSlider","argname": "height","options":{"min":400,"max":1200,"value":600}},
                    # {"kind": "IntSlider","argname": "width","options":{"min":400,"max":1200,"value":600}},
                    {"kind": "Select", "argname": "color", "options":{
                        "options":[key for key in PLOTLY_SCALES],"value":"Earth","description": "color: "}},
                    {"kind": "Select", "argname": "hist_color", "options":{
                        "options":[key for key in PLOTLY_SCALES],"value":"Earth","description": "hist_color: "}},
                    {"kind": "Select", "argname": "point_color", "options":{
                        "options":[key for key in PLOTLY_SCALES],"value":"Earth","description": "point_color: "}}
                ]
            },
            subplots,
            plot_chart
        ],
        "titles": [(0, "select"), (1, "parameter"), (2, "figure"), (3, "chart")]
    }
}

preprocessing_config = {
    "Imputer": {
        "kind": "Tab",
        "children": [
            {
                "kind": "HBox",
                "children": [
                    {"kind": "Text", "argname": "missing_values", "options": {
                        "placeholder": "the value will use for fill",
                        "description": "missing_values: ",
                        "value": "NaN"
                    }},
                    {"kind": "Select", "argname": "strategy", "options": {
                        "options": ["mean", "median", "most_frequent"],
                        "description": "fill method: "}},
                    {"kind": "Select", "argname": "strategy", "options": {}}
                ]
            }
        ]
    },
    "factorization": {
        "kind": "Tab",
        "titles": [(0, "parameter")],
        "children": [
            {
                "kind": "HBox",
                "children": [
                    x,
                    node("Text", "bins", "bins: ", value="3", placeholder="int or seq split with ,")
                ]
            }
        ]
    }
}


def set_args_options(node, options):
    if 'children' in node:
        for n in node['children']:
            set_args_options(n, options)
    else:
        if node['argname'] in options:
            node['options'] = dict(node['options'], **options[node['argname']])
    return node


def set_config(feature, prefix, row_wrap=10):
    config = {
        "kind": "VBox",
        "children": []
    }
    boxes = []
    for f in feature[1:]:
        boxes.append({
            "kind": "Checkbox",
            "argname": prefix + f[1],
            "options": {"value": False, "description": f[1]}
        })
    i = 0
    while i < len(boxes):
        config['children'].append({
            "kind": "HBox",
            "children": boxes[i:i + row_wrap]
        })
        i += row_wrap
    return config
