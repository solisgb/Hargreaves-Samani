# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl


def xy_ts_plot_1g(title: str, x: list, y: list, ylabel: str, dst: str):
    """
    Dibuja una figura con 1 gráfico (axis) xy
    args
    title: título de la figura
    tsu: lista de objetos Time_series para el gráfico superior
    x: lista de objetos date
    y: lista de valores interpolados float
    dst: nombre fichero destino (debe incluir la extensión png)
    """
    # parámetros específicos
    mpl.rc('font', size=8)
    mpl.rc('axes', labelsize=8, titlesize= 10, grid=True)
    mpl.rc('axes.spines', right=False, top=False)
    mpl.rc('xtick', direction='out', top=False)
    mpl.rc('ytick', direction='out', right=False)
    mpl.rc('lines', linewidth=0.8, linestyle='-', marker='.', markersize=4)
    mpl.rc('legend', fontsize=8, framealpha=0.5, loc='best')

    fig, ax = plt.subplots()

    plt.suptitle(title)
    ax.set_ylabel(ylabel)

    fig.autofmt_xdate()

    ax.plot(x, y)

    fig.savefig(dst)
    plt.close('all')
    plt.rcdefaults()


