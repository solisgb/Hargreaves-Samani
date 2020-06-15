# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 17:53:24 2019

@author: solis

Parámetros de un módulo de cálculo de la ETP

Antes de ejecutar el programa lee atentamente los parámetros que intervienen
"""

"""=====================PARÁMETROS GENERALES===============================
dbtype: msaccess, sqlite, puede ser ms_access, sqlite o postgres
db: base de datos con los datos a interpolar
select1: select estaciones donde se va a calcular la ET con latitud
select2: select de datos de tmax y tmin para calcular la ET
dir_out: directorio donde se graban los resultados
xygraph: se graban ficheros xy True/False
"""
dbtype = 'postgres'
db = r'bda'
select1 = \
"""
select e.c_clima , max(st_y(st_transform(e.geom, 4326))) latitud
from met.cl_est_climat e
	left join met.cl_temper_diaria t using (c_clima)
where t.fh_medida >= '1985-01-01' and t.fh_medida < '2015-01-01'
group by e.c_clima
having count(*) > 7300
order by e.c_clima;"""
select2 = \
"""
select t.fh_medida , t.tmax , t.tmin , (t.tmax + t.tmin)*0.5::float tavg
from met.cl_temper_diaria t
where t.c_clima=%s and
    t.fh_medida >= '1985-01-01' and t.fh_medida < '2015-01-01'
order by t.fh_medida;
"""
dir_out = r'C:\Users\solis\Documents\work\tmp'
xygraph: bool = True
