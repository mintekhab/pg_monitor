#!/usr/bin/python

import math
import re

def getTimeFactor ( check_val ) :
        factor = 0
        val = ''
        unit = ''
        if check_val.lower().endswith('min')  or  check_val.lower().endswith('mins')  :
                factor = 1
                val = check_val.lower().replace('min','').replace('s','').replace(' ','')
                unit = 'min'
        elif check_val.lower().endswith('hr')  or check_val.lower().endswith('hrs')   :
                factor = 60
                val = check_val.lower().replace('hr','').replace('s','').replace(' ','')
                unit = 'hr'
        elif check_val.lower().endswith('day')  or check_val.lower().endswith('days')  :
                factor = 24*60
                val = check_val.lower().replace('day','').replace('s','').replace(' ','')
                unit = 'day'
        elif check_val.lower().endswith('wk') or check_val.lower().endswith('wks')  :
                factor = 60 * 24 * 7
                val = check_val.lower().replace('wk','').replace('s','').replace(' ','')
                unit = 'wk'
        elif check_val.lower().endswith('yr')  or check_val.lower().endswith('yrs') :
                factor = 60 * 24 * 7 * 52
                val = check_val.lower().replace('yr','').replace('s','').replace(' ','')
                unit = 'yr'

	if str(val).isdigit() :
        	return [val , factor, unit]
	else :
		return None


def getSizeFactor ( check_val ) :
        factor = 0
        val = ''
        unit = ''
        if check_val.lower().endswith('k') :
                factor = 1024
                val = check_val.lower().replace('k','')
                unit = 'KB'
        elif check_val.lower().endswith('m') :
                factor = 1024 * 1024
                val = check_val.lower().replace('m','')
                unit = 'MB'
        elif check_val.lower().endswith('g')  :
                factor = 1024 * 1024 * 1024
                val = check_val.lower().replace('g','')
                unit = 'GB'
        elif check_val.lower().endswith('t') :
                factor = 1024 * 1024 * 1024 * 1024
                val = check_val.lower().replace('t','')
                unit = 'TB'
        elif check_val.lower().endswith('p')  :
                factor = 1024 * 1024 * 1024 * 1024 * 1024
                val = check_val.lower().replace('p','')
                unit = 'PB'

	if str(val).isdigit() :
                return [val , factor, unit]
        else :
                return None


def getNumberPercentLimits( limit, total ) :
        if limit != None :
                pLimit = limit.split('or')
                nperc = 0
                wperc = 0
                for ele in pLimit :
                        if ele.find('%') == -1 :
				nperc = int ( ele.replace(' ','')   )
                        elif ele.find('%') != -1 :
                                wperc =  math.ceil( ( float ( ele.replace('%','').replace(' ','') ) / 100 ) * total )
                return int (max( nperc, wperc ))



def checkDigit (check_val) :
        retval = re.findall(r'\d.+\d+',check_val)
        return False not in  [True for element in retval if element.isdigit()]

	

def getNumberPercentMix (warning=None, critical=None, defaultWarn=None, defaultCritical=None ) :
        retval = {}
        warn = warning   if warning != None else defaultWarn
        crit = critical  if critical != None else defaultCritical
        retval.update ({'warning' : warn})
        retval.update ({'critical' : crit})

        if checkDigit(warn.split('or'))  or  checkDigit(crit.split('or'))  : 
                return retval
        else :
                return None


def warningAndOrCriticalProvided (warning,critical) :
        # as an heuristic 
        # warning = 0.8 * critical
        if warning == None and critical != None :
                critical = getSizeFactor ( critical )
                if critical == None :
                        return None
                return {'warning' : None , 'critical' : str(critical[0]) + critical[2][0] }
        elif warning != None and critical == None :
                warning = getSizeFactor ( warning )
                if warning == None :
                        return None
                return {'warning' : str(warning[0]) + warning[2][0] ,  'critical' : None }
	elif warning != None and critical != None :
		critical = getSizeFactor ( critical )
		warning = getSizeFactor ( warning )
		if warning == None or critical == None :
			return None
		return {'warning' : str(warning[0]) + warning[2][0] ,  'critical' : str( critical[0] ) + critical[2][0] }
        else :
                return None



def getTimeDefaults (warning, critical , defaultWarning, defaultCritical) :
                warn = warning if warning != None else defaultWarning
                crit = critical if critical != None else defaultCritical
                warn = getTimeFactor( warn )
                crit = getTimeFactor( crit )
                retval = {}
                if warn != None and crit != None :
			# check for the larger of the 2
                        retval.update( {'warning' : str(warn[0]) + str(warn[2]) }  )
                        retval.update( {'critical' : str(crit[0]) + str(crit[2]) }  )
                        return retval
                else :
                        return None

