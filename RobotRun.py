import subprocess
import argparse
from getpass import getpass
import multiprocessing
import os
import ConfigParser

#this feature will only run when if there are failures during first time of execution of ALL tests in parallel
def rerunFunction(processNum,curWorkDir):
    outputFilePath='output.xml';
    rerunFilePath='rerun.xml';
    print 'Failures in batch causing rerun of failed scripts second time'

    reruncommand='pabot --nostatusrc --rerunfailed' + ' ' + outputFilePath + ' --output' + ' ' + rerunFilePath + ' ' + \
                 '--variable RALLY_TEST_ENV:' + args.ENV + \
                 ' --variable ON_DEMAND:' + args.SAUCE + \
                 ' --variable PROCESSES:' + args.PROCESSES + \
                 ' --variable RALLY_SUPER_USERNAME:' + authUsername + \
                 ' --variable RALLY_SUPER_PASSWORD:' + authPassword + \
                 ' --loglevel ' + args.LOGLEVEL + \
                 ' ./'
    print 'merging and creating final output.xml'

    mergecommand='rebot --nostatusrc --output output.xml --merge output.xml rerun.xml'

    p8 = subprocess.Popen(reruncommand,shell=True)
    p8.wait()
    p9 = subprocess.Popen(mergecommand,shell=True)
    p9.wait()
    print 'function completed'

def _getValueFromConfigOtherwiseUseDefault(configParser, environmentArgument, configKeyName, defaultValue):
    if configParser.has_option(environmentArgument.upper(), configKeyName):
        value = configParser.get(environmentArgument.upper(), configKeyName)
    else:
        print "No value defined for '%s' in section '%s' of the config file.  " \
              "Using default value instead." % (configKeyName, environmentArgument.upper())
        value = defaultValue

    return value

def _setUsername(usernameArgument, configParser, environmentArgument, configKeyName, defaultValue):
    if (not usernameArgument):
        usernameValue = _getValueFromConfigOtherwiseUseDefault(configParser, environmentArgument, configKeyName,
                                                              defaultValue)
    else:
        usernameValue = usernameArgument
    return usernameValue

def _setPassword(passwordArgument, configParser, environmentArgument, configKeyName, defaultValue):
    if (passwordArgument != None and passwordArgument.upper() == "PROMPTME"):
        # Prompt for a password which will not be easily visible
        passwordValue = getpass('Password: ')
    elif (not passwordArgument):
        passwordValue = _getValueFromConfigOtherwiseUseDefault(configParser, environmentArgument, configKeyName,
                                                              defaultValue)
    else:
        passwordValue = passwordArgument
    return passwordValue


numCPUs = str(multiprocessing.cpu_count())

defaultUserName = 'rallyhealth'
defaultPassword = 'rallyw1ns!'
setIncludedTags = ''
configFileAuthUsernameName = "authUsername"
configFileAuthPasswordName = "authPassword"

parser = argparse.ArgumentParser(description='Take values for running automation')

parser.add_argument('-e', '--ENV', nargs='?', type=str.upper, help='Any valid environment [Default: LOCAL]', default='LOCAL', metavar='')
parser.add_argument('-r', '--RUN', nargs='+', help='Space separated tags to run (ALL to run all batches in parallel) [Default: DEV]', default=['DEV'], metavar='')
parser.add_argument('-s', '--SAUCE', nargs='?', type=str.upper, choices=['TRUE','FALSE'], help='TRUE, FALSE [Default: FALSE]' , default='FALSE', metavar='')
parser.add_argument('-u', '--USERNAME', nargs='?', help='Replace with your username if desired.', metavar='')
parser.add_argument('-p', '--PASSWORD', nargs='?', help='Replace with your password if desired.', metavar='')
parser.add_argument('-n', '--PROCESSES', nargs='?', help='Number of processes to run with [Default: ' + str(numCPUs) + ']', default=numCPUs, metavar='')
parser.add_argument('-l', '--LOGLEVEL', nargs='?', help='Log level to run with [Default: ERROR]', default='ERROR', metavar='')

args = parser.parse_args()

configFilename = 'system.cfg'
config = ConfigParser.ConfigParser()
config.read([configFilename])

if config.read([configFilename]) == []:
    print ("ERROR - could not find the configuration file %s.  \n"
           "This is the file where all the rally test environments are defined.  Check to see the .cfg file exists in the right path" % configFilename)
    raise IOError('Config file %s was not found' % configFilename)

authPassword = _setPassword(args.PASSWORD, config, args.ENV, configFileAuthPasswordName, defaultPassword)
authUsername = _setUsername(args.USERNAME, config, args.ENV, configFileAuthUsernameName, defaultUserName)

setVariableArgs = ' --processes ' + str(args.PROCESSES) + \
                  ' --variable ENVIRONMENT:' + args.ENV + \
                  ' --variable ON_DEMAND:' + args.SAUCE + \
                  ' --variable RALLY_AUTH_USERNAME:' + authUsername + \
                  ' --variable RALLY_AUTH_PASSWORD:' + authPassword + \
                  ' --loglevel ' + args.LOGLEVEL

if (len(args.RUN) > 0):
    currentDir= os.getcwd()
    dir = os.path.dirname(__file__)

    setIncludedTags = '--include ' + ' --include '.join(args.RUN)
    p1 = subprocess.Popen('pabot ' + setVariableArgs + ' ' + setIncludedTags + ' ./', shell=True)
    p1.wait()

#Find out if any of the tags that should be rerun are in the rerun_tags list and then call the rerunFunction
rerun_tags=['ALL', 'SMOKE']

if any(args.RUN[0].upper() in s for s in rerun_tags):
      print(args.RUN[0].upper())
      rerunFunction(p1,currentDir)
else:
    print("No tags to be rerun")


print("done")