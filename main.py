# -*- coding: utf-8 -*-
"""
Created on 06/09/2019

@author: Luis Solís

driver módulo ETP
Antes de ejecutar la app asegúrate de que rellenas correctamente los valores
    de los parámetros que controlan la ejecución en el módulo
    etp_param
Al finalizar la ejecución el programa crea el fichero app.log con las
    incidencias de la ejecución
"""
import littleLogging as logging

if __name__ == "__main__":

    try:
        from time import time
        import traceback
        from etp import ETP
        import etp_param as par

        startTime = time()

        h = ETP(par.dbtype, par.db)

        h.hs(par.select1, par.select2, par.dir_out, par.xygraph)

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
