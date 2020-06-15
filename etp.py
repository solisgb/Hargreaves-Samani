# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:26:19 2019

@author: solis

ET by Hargreaves-Samani method
If you don't have numba installed comment lines
    from numba import jit
    _hargreaves_samani_01
and uncomment line
    _hargreaves_samani
"""
from numba import jit
import numpy as np


class ETP():

    DBTYPES = ('postgres',)


    def __init__(self, dbtype: str='postgres', dbname: str='bda'):
        """
        dbtype: un valor de DBTYPES
        dbnama: nombre de la base de datos
            su dbtype postgres dbname es el nombre de la sección del fichero
            pgdb.ini con los datos de la conexión, por ejemplo
            [bda]
            host=localhost
            database=bda
            user=postgres
            password=mypw
        latitud: N (norte) o S (sur)
        """
        if dbtype not in self.DBTYPES:
            dbtypes = ','.join(self.DBTYPES)
            raise ValueError(f'dbtype debe ser un valor en {dbtypes}')
        self.dbtype = dbtype
        self.dbname = dbname


    def hs(self, select1: str, select2: str, dir_out: str, xygraph : bool):
        """
        calculo de la ET por el metodo de Hargreaves
        """
        from os.path import join
        import sqlite3
        from db_connection import con_get
        from graphs import xy_ts_plot_1g

        select_r0 = 'select r0 from r0 where lat = ? order by "month"'

        con = con_get(self.dbtype, self.dbname)
        cur = con.cursor()

        con3 = sqlite3.connect('r0.db')
        cur3 = con3.cursor()

        cur.execute(select1)
        stations = [row for row in cur.fetchall()]

        for station in stations:
            print(station[0])
            if station[1] > 70:
                station[1] = 70
            elif station[1] < -70:
                station[1] = - 70
            ilat = int(round(station[1], 0))
            cur3.execute(select_r0, (ilat,))
            r0s = [row[0] for row in cur3.fetchall()]
            if not r0s:
                raise ValueError(f'{station[0]}: no r0 at {ilat}º')
            cur.execute(select2, (station[0],))
            ts = np.array([row for row in cur.fetchall()])
            tmax = ts[:, 1] / 10.
            tmin = ts[:, 2] / 10.
            tavg = ts[:, 3] / 10.
            im = np.array([row[0].month-1 for row in ts], np.int32)
#            self._hargreaves_samani(r0s, im, tmax, tmin, tavg,
#                                    np.empty(len(im), np.float32))

            etp = np.empty(len(im), np.float32)
            _hargreaves_samani_01(np.array(r0s, np.float32),
                                  im,
                                  tmax.astype(np.float32),
                                  tmin.astype(np.float32),
                                  tavg.astype(np.float32),
                                  etp
                                  )
            self._write(station[0],
                       [row[0].strftime('%Y-%m-%d') for row in ts],
                       etp,
                       dir_out)

            if xygraph:
                title = f'{station[0]}'
                x = [row[0] for row in ts]
                ylabel = 'etp (mm)'
                dst = join(dir_out, f'{station[0]}.png')
                xy_ts_plot_1g(title, x, etp, ylabel, dst)

        con3.close()
        con.close()
        self._h_metadata(select1, select2, dir_out, xygraph, stations)


    def _write(self, station, sdate, etp, dir_out: str):
        from os.path import join
        dst = join(dir_out, f'{station}.hs')
        with open(dst, 'w') as f:
            f.write('"fecha","etp"\n')
            for i in range(len(sdate)):
                f.write(f'{sdate[i]},{etp[i]:0.1f}\n')


    @staticmethod
    def _hargreaves_samani(r0, im, tmax, tmin, tavg, etp):
        """
        calculo d ela etp por el metodo de hargreaves-samani
        r0: radiación extraterrestre mm
        im: mes de la observación -1
        tmax, tmin, tavg: tamperatura máxima, míima y media en grados C
        etp: etp calculad aen mm
        """
        for i in range(len(im)):
            etp[i] = 0.0023 * (tavg[i] + 17.78) + r0[im[i]] \
                * (tmax[i] - tmin[i])**0.5


    def _h_metadata(self, select1: str, select2: str, dir_out: str,
                    xygraph : bool, stations: list):
        """
        Graba el fichero de metadatos
        args igual que hs
        """
        from os.path import join
        dst = join(dir_out, 'hs_metadata.txt')
        with open(dst, 'w') as f:
            f.write(f'hargreaves-samani\n')
            f.write(f'db type: {self.dbtype}\n')
            f.write(f'db name: {self.dbname}\n')
            f.write(f'select stations: {select1}\n')
            f.write(f'select data: {select2}\n')
            f.write(f'Write xy: {xygraph}\n')
            f.write(f'stations,lat (epsg 4326)\n')
            for row in stations:
                f.write(f'{row[0]},{row[1]:0.1f}\n')


@jit(nopython=True)
def _hargreaves_samani_01(r0, im, tmax, tmin, tavg, etp):
    """
    calculo d ela etp por el metodo de hargreaves-samani
    r0: radiación extraterrestre mm
    im: mes de la observación -1
    tmax, tmin, tavg: tamperatura máxima, míima y media en grados C
    etp: etp calculad aen mm
    """
    for i in range(len(im)):
        etp[i] = 0.0023 * (tavg[i] + 17.78) + r0[im[i]] \
            * (tmax[i] - tmin[i])**0.5
