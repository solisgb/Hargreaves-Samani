# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:26:19 2019

@author: solis

calcula la etp por el método de Hargreaves-Samani
"""


class ETP():

    FILE_RO = 'Ro_mm_12m.txt'
    # tipo de base de datos
    DBTYPES = ('postgres',)


    def __init__(self, dbname: str='bda', dbtype: str='postgres',
                 latitud: str='N'):
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
        if latitud not in ('N', 'S'):
            raise ValueError('La latitud debe ser N o S')
        self.latitud = latitud


    def hs(self, select: str, dir_out, file_out='ET_Hargreaves-Samani.txt'):
        """
        calculo de la ET por el metodo de Hargreaves
        """
        from datetime import date
        from math import fmod
        from time import time
        from ado import Connection

        start_time=time()

        con=Connection(self.db)

        latitudes_Allen, ro_d15=HS.ro_d15_mm_read()

        latitudes_Allen=np.array(latitudes_Allen, np.float32)
        ro_d15=np.array(ro_d15, np.float32)

#        ndx=np.searchsorted(latitudes_Allen, estaciones.latitudes)

        for i, (cod1, latitud1, ns1) in enumerate(zip(estaciones.cods, estaciones.latitudes, estaciones.NS)):
            j=i+1
            if fmod(i, 5)==0.0:
                flag_show=1

            select1=db.select1_get(cod1)
            fechas_ts=con.fetchall(select1, cacheSize=10000)
            fechas=[date(item[0].year, item[0].month, item[0].day) for item in fechas_ts]
            tmedias=np.array([(item[1]+item[2])/2. for item in fechas_ts])
            tmedias=tmedias*10.

            ro=[]
            month_prev=fechas[0].month
            k=0
            for fecha1 in fechas:
                if fecha1.month==month_prev:
                    k+=1
                else:
                    #calcular
                    pass



            for fecha1, tmedias1 in zip(fechas, tmedias):
                if ns1=='N':
                    z=np.interp(latitud1, latitudes_Allen, ro_d15[:, fecha1.month-1])
                else:
                    z=np.interp(latitud1, latitudes_Allen, ro_d15[:, fecha1.month+11])
                ro.append(z)

                    #np.interp(2.5, xp, fp)


            if flag_show==1:
                ellapsed_min, min_to_end=time_2_end_get(start_time, n, j)
                print('Ellapsed min {0:0.1f}, {1:0.1f} min to end'.format(ellapsed_min, min_to_end))
                flag_show=0

