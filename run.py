import threading,time,csv

from flask import send_file
from FASToryEM import app
from FASToryEM import UtilityFunctions as helper
from FASToryEM import configurations as CONFIG
#from FASToryEM.msgBus import MqqtClient
from FASToryEM.dbModels import EnergyMeasurements, WorkstationInfo,MeasurementsForDemo



if __name__ == '__main__':
    # query = MeasurementsForDemo.query.all()
    # fileName='forDemo.csv'
    # helper.SQL_queryToCsv(fileName,query)
    # mqtt = MqqtClient(CONFIG.NAME,CONFIG.MQTT_CLIENT_ID)
    # mqtt.connect()
    
    helper.createModels()    
    # Workstation Objects
    start_workstations=threading.Thread(target=helper.Workstations)
    start_workstations.daemon=True
    start_workstations.start()
    helper.createModels()
    #time.sleep(5)
    #helper.get_local_ip()
    app.run(host='0.0.0.0', port=CONFIG.appLocPort)#,use_reloader=False,debug=True helper.get_local_ip()
#'192.168.100.100' helper.get_local_ip()


