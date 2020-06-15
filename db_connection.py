# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 17:48:42 2019

@author: solis
"""


def con_get(dbtype: str, dbpath: str):
    """
    conexión a una base de datos
    """
    if dbtype == 'ms_access':
        con = ms_access_conn_get(dbpath)
        return con
    elif dbtype == 'sqlite':
        con = sqlite_conn_get(dbpath)
        return con
    elif dbtype == 'postgres':
        con = postgres_conn_get(dbpath)
        return con
    else:
        raise ValueError(f'El tipo de db {dbtype} no está implementado')


def postgres_conn_get(section: str):
    """
    devuelve la conexión a una db postgres
        los parámetros de la conexiona los obtiene del fichero FILE_INI
        que tiene tantas secciones como bases de datos; cada sección tiene
        los parámetros: host, database, user, password
    """
    import psycopg2
    from configparser import ConfigParser
    FILE_INI = 'pgdb.ini'
    parser = ConfigParser()
    parser.read(FILE_INI)
    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise ValueError(f'No se encuentra section {section} en' +\
                         f' {FILE_INI}')
    return psycopg2.connect(**db_params)


def ms_access_conn_get(dbpath: str):
    """
    devuelve la conexión a una db ms access
    """
    import pyodbc
    con_str = r'DRIVER={Microsoft Access Driver ' +\
    '(*.mdb, *.accdb)}; ' + f'DBQ={dbpath};'
    return pyodbc.connect(con_str)


def sqlite_conn_get(dbpath: str):
    """
    devuelve la conexión a una db ms access
    """
    import sqlite3
    return sqlite3.connect(dbpath)
