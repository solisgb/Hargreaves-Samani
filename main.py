# -*- coding: utf-8 -*-
"""
Created on 06/09/2019

@author: Luis Solís

driver módulo interpol
Antes de ejecutar la app asegúrate de que rellenas correctamente los valores
    de los parámetros que controlan la ejecución en el módulo
    interpolation_param
Al finalizar la ejecución el programa crea el fichero app.log con las
    incidencias de la ejecución
"""


if __name__ == "__main__":

    try:
        from time import time
        import traceback
        from interpol import Interpolate
        import interpolation_param as par
        import littleLogging as logging

        startTime = time()

        i = Interpolate(par.dbtype, par.db, par.select,
                 par.day1, par.month1, par.year1,
                 par.day2, par.month2, par.year2,
                 par.time_step, par.no_value, par.float_format,
                 par.variable_short_name, par.ylabel)

        i.idw_serie_temporal(par.pathin, par.fpoints, par.skip_lines,
                             par.pathout,
                             par.kidw, par.poweridw, par.epsidw,
                             par.xygraph)

        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')

    except ValueError:
        msg = traceback.format_exc()
        logging.append(f'ValueError exception\n{msg}')
    except ImportError:
        msg = traceback.format_exc()
        print (f'ImportError exception\n{msg}')
    except Exception:
        msg = traceback.format_exc()
        logging.append(f'Exception\n{msg}')
    finally:
        logging.dump()
        print('se ha creado el fichero app.log')
