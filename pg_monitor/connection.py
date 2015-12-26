#!/usr/bin/python 

import time
import sql
import math


def getConnections( param=None ) :
        item_name = 'POSTGRES_CONNECTIONS'
        status = []
        perfdata = '-'
        output = ''
        if param != None :
                query = "SELECT \
                              datname \
                         FROM \
                              pg_database \
                         WHERE datistemplate is FALSE"

                dbs = sql.getSQLResult ( {'host': param['host'] , 'port' : param['port'], 'dbname': 'postgres', 'user' : param['user'] ,'password' : param['password'] } ,query )
		for db in dbs :
			query = "select version()"
			begin = time.time()
			row = sql.getSQLResult ( {'host': param['host'] , 'port' : param['port'], 'dbname': db[0], 'user' : param['user'] ,'password' : param['password'] } ,query )
			duration = int ( math.ceil ( ( time.time() - begin ) * 1000 ) )
			if row != None :
				status.append(0)
			else :
				status.append(2)

                        if perfdata == '-' :
                                perfdata = db[0] + '=' + str( duration )
                                output =  '{0:s} connection test took {1:s} ms'.format(db[0],str(duration) )
                        elif perfdata != '-'  :
                                perfdata = perfdata + '|' + db[0] + '=' + str ( duration )
                                output =  output + '; {0:s} connection test took {1:s} ms'.format(db[0],str(duration) )


                status.sort( reverse=True )
                return str(status[0]) + ' ' + item_name + ' ' + str(perfdata) + ' ' + output
        else :
                return 2 + ' ' + 'POSTGRES_CONNECTIONS' + ' ' + '-' + 'Invalid parameters passed to check'
## testing the function 
if __name__ == '__main__' :
        print ( getConnections( {'host' : 'localhost', 'port' : '5432' ,'user' : 'postgres' , 'password' : '' } )  )
