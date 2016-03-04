#!/usr/bin/python 

# list of valid actions 
# backends 
#connections
# wals
# autovacuum
# vacuum
# autoanalyze 
# analyze 
# tale_bloat 
# index_bloat 
# table_size
# index_size 
# database_size 
# nonblocking
# blocking
# checkpoints 
# duplicate_indexes
# replica_lag

import factors as fac


def getDefaults (check , warning , critical ) :
	if check == 'backends' : 
		# only whole digits and percentages allowed, an or separator is also allowed 
		return fac.getNumberPercentMix (warning, critical, '80%', '90%' )
	elif check == 'connections' :
                return {'warning':'dummy', 'critical' :'dummy'}
	else :
		if warning != None or critical != None :
			warn = None 
			crit = None 

                        if warning != None :
                        	crit = critical if critical != None else warning
                        elif critical != None :
                        	warn = warning if warning != None else critical

			if check == 'wals' :
				# -- warning and/or critical must be supplied
				if str(warn).isdigit() and str(crit).isdigit() :
					return {'warning' : warn , 'critical' : crit}
				else :
					return None  
			elif check == 'autovacuum' or check == 'vacuum' or check == 'autoanalyze' or check == 'analyze':
				# -- warning = 1 month
				return fac.getTimeDefaults (warning, critical , '1month', '')
			elif check == 'table_bloat' or check == 'index_bloat' :
				#  Warning and/or Critical must be provided
				return fac.warningAndOrCriticalProvided (warning,critical,0.8)
			elif check == 'table_size' or check == 'index_size' or check == 'database_size' :
				# warning and/or critical value must be supplied
				return fac.warningAndOrCriticalProvided (warning,critical,0.5) 
			elif check == 'nonblocking' or check == 'blocking' :
				# --warning = 2min
				# critical = 3min
				return fac.getTimeDefaults (warning, critical , '1min', '2mins', 0.8) 
			elif check == 'checkpoints' :
				# warning and/or critical value must be supplied
				return None
			elif check == 'replica_lag' :
				# -- warning = 5 wal files
				# -- critical = 10 wal files 
				return fac.getNumberPercentMix (warning, critical, '5', '10' ) 
		else :
			return None 
