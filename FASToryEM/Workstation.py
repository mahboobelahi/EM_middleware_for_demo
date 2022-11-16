from datetime import datetime
import numpy as np
from sqlalchemy import exc
import threading, requests, json, time,socket
from pprint import pprint as P
from flask import Flask, redirect, render_template, request, jsonify, url_for,flash,send_from_directory
from FASToryEM import configurations as CONFIG
from FASToryEM.dbModels import EnergyMeasurements, WorkstationInfo,MeasurementsForDemo
from FASToryEM import UtilityFunctions as helper
# orchestrator connector object
#EnergyMeasurements.query.filter_by(ActiveZones='1001').update(dict(LoadCombination=9))
from FASToryEM import db
from flask_sqlalchemy import SQLAlchemy





# workstation class

class Workstation:
    def __init__(self, ID, wLocIP, make ,type, wLocPort,numFast,num):
        # token
        self.token = ''
        self.access_token_time = 0
        self.expire_time = 0
        self.headers = {}
        # workstation attributes
        self.count = 0
        self.stop_recording = 0
        self.LoadCombination = 0
        self.activeZones = ''
        self.classLabel = 2
        self.BeltTension = 0
        self.make = make
        self.type = type
        self.name = f'FASTory_Energy_Monitoring_E10_Module_WrkStation_{ID}'
        self.ID = ID
        self.source_ID = 0
        self.external_ID = f'{ID}4EM'
        self.url_self = f'http://{wLocIP}:{wLocPort}' #use when working in FASTory network
        #self.url_self = f'http://{self.get_local_ip()}:{wLocPort}'#130.230.190.118
        self.port = wLocPort
        self.EM = True
        # workstaion servies
        self.measurement_ADD = f'{self.url_self}/measurements'
        self.EM_service_url = f'http://192.168.{ID}.4/rest/services/send_all_REST'
        self.CNV_start_stop_url = f'http://192.168.{ID}.2/rest/services/'
        # for reat-time grphs
        self.powerlist = []
        self.power = 0
        self.voltage = 0
        self.current = 0
        # checking for Z4 and installed EM modules
        if self.ID in CONFIG.hav_no_EM:
            self.EM = False
        if ID == 1 or ID == 7:
            self.hasZone4 = False
        else:
            self.hasZone4 = True
        self.num = num #request timeout
        self.numFast = numFast
        self.stop_simulation = False
        
    # *****************************************
    #  WorkstationClass mutators and DB section
    # *****************************************

    def callWhenDBdestroyed(self):
        # inserting info to db
        # one time call, only uncomment when db destroyed otherwise
        # do the update
        info = WorkstationInfo(
            WorkCellName=self.name,
            WorkCellID=self.ID,
            RobotMake = self.make,
            RobotType = self.type,
            DAQ_ExternalID=self.external_ID,
            DAQ_SourceID=self.source_ID,
            HasZone4=self.hasZone4,
            HasEM_Module=self.EM,
            WorkCellIP=self.url_self,
            EM_service_url=self.EM_service_url,
            CNV_service_url=self.CNV_start_stop_url
        )
        db.session.add(info)
        db.session.commit()

    def updateIP(self):
        WrkIP = WorkstationInfo.query.get(self.ID)
        WrkIP.WorkCellIP = self.url_self
        # WrkIP=WorkstationInfo.query.filter(WorkstationInfo.WorkCellID==self.ID)
        # WrkIP.update({WorkstationInfo.WorkCellIP:self.url_self})
        db.session.commit()

    # accessors and setters

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def get_ID(self):
        return self.ID
    
    def get_external_ID(self):
        return self.external_ID
    
    def get_headers(self):
        return self.headers
    
    def get_stop_simulation(self):
        return self.stop_simulation

    def WkSINFO(self):
        P(self.__dict__)

    def has_EM(self):
        return self.EM

    def set_has_EM(self, flage):
        self.EM = flage

    def set_source_ID(self, srID):
        self.source_ID = srID

    def set_count(self, num=0):
        self.count = num

    def count_inc(self):
        self.count = self.count + 1
        return self.count

    def stop_recording_inc(self):
        self.stop_recording = self.stop_recording + 1

    def set_stop_recording(self, num=0):
        self.stop_recording = num

    def set_stop_simulations(self,flag):
        self.stop_simulation =flag

    def updatePR_parameters(self, L, AZ):
        self.load = L
        self.activeZones = AZ

    def updateClassLabel(self, CL,BT,lc):
        self.classLabel = CL
        self.BeltTension = BT
        self.LoadCombination = lc

    def update_PVC(self, p, v, c):
        self.power = p
        self.voltage = v
        self.current = c
        print(self.power)

    # *********************************************
    # Workstation Methods
    # *********************************************
    # auto start/stop energy-measurement service

    def invoke_EM_service(self, cmd='stop'):
        if self.EM == False:
            print("Has no EM module.")
            return
        body = {
            "cmd": cmd,
            "send_measurement_ADDR": self.measurement_ADD,
            "ReceiverADDR": 'http://192.168.100.100:2000/noware'  # f'{self.url_self}/noware'
        }
        try:
            r = requests.post(url=self.EM_service_url, json=body)
            return f"Status Code: {r.status_code}, Reason: {r.reason}"
        except requests.exceptions.RequestException as err:
            print("[X-W] OOps: Something Else", err)
            return err
    # related to DAQ
    # events/alarms/deviceControl etc

    def handleAlarms(self):
        pass

    def sendEvent(self, type, text):
        pass

    def deviceControl(self):
        pass

    # registration to ZDMP-DAQ component
    def register_device(self):
        # need to set some guard condition to avoid re-registration of device
        # each device registared against a unique external ID
        try:
            req = requests.get(
                url=f'{CONFIG.ADMIN_URL}/deviceInfo?externalId={self.external_ID}',
                headers=self.headers)
            if req.status_code == 200:
                self.set_source_ID(req.json().get('id'))
                print('[X-W-RD] Device already Registered. Device details are:\n')
                # pprint(req.json())
            else:
                print('[X-W-RD] Registering the device')
                req_R = requests.post(
                    url=f'{CONFIG.ADMIN_URL}/registerDevice?externalId={self.external_ID}&name={self.name}&type=c8y_Serial',
                    headers=self.headers)
                print(f'Http Status Code: {req_R.status_code}')
                # setting souece ID of device
                self.set_source_ID(req_R.json().get('id'))
                print('[X-W-RD] Device Registered Successfully.\n')
                # pprint(req_R.json())
        except requests.exceptions.RequestException as err:
            print("[X-W-RD] OOps: Something Else", err)

    # register data source to ASYNC-DAQ service
    def sub_or_Unsubscribe_DataSource(self, subs=False):

        payload = {"externalId": self.external_ID, "topicType": 'multi'}
        try:
            if subs:
                req = requests.delete(f'{CONFIG.ASYNCH_URL}/unsubscribe',
                                   params=payload, headers=self.headers)
                #self.sendEvent('DAQ-ASYNC', 'Data source have unsubscribed to previous subscriptions.....')
                print(f'[X-W-SUD] Unsubscribing to Data Source: {self.external_ID}....{req.status_code}')
                req = requests.post(f'{CONFIG.ASYNCH_URL}/subscribe',
                                   params=payload, headers=self.headers)
                if req.status_code == 200:
                    #self.sendEvent('DAQ-ASYNC', 'Data source have subscribed to ASYNC data access...')
                    P(req.json())
                    print(f'[X-W-SUD] Subscription Status: {req.status_code} {req.reason}')
                elif req.status_code in [500,401,400,409,408]:
                    print(f'[X-W-SUD] Status from Error block: {req.status_code} {req.reason}')
                    P(req.json())
                    time.sleep(1)
                    req = requests.post(f'{CONFIG.ASYNCH_URL}/subscribe',
                                       params=payload, headers=self.headers)
                    if req.status_code == 200:
                        #self.sendEvent('DAQ-ASYNC', 'Data source have subscribed to ASYNC data access...')
                        print(f'[X-W-SUD] Subscription Status: {req.status_code} {req.reason}')

                else:

                    print(f'[X-W-SUD] Subscription Status: {req.status_code} {req.reason}')
            else:
                req = requests.delete(f'{CONFIG.ASYNCH_URL}/unsubscribe',
                                   params=payload, headers=self.headers)

                if req.status_code == 200:
                    print(f'[X-W-SUD] Unsubscribe Status: {req.status_code} {req.reason}')
                else:
                    print(f'[X-W-SUD] Unsubscribe Status: {req.status_code} {req.reason}')

        except requests.exceptions.RequestException as err:
            print("[X-W-SUD] OOps: Something Else", err)

    # checks for active zones on conveyor of a particular workstation

    def get_ZoneStatus(self):
        try:
            load = 0
            ActiveZone = ''
            for i in [1, 2, 3, 5]:
                req = requests.post(
                    f'http://192.168.{self.ID}.2/rest/services/Z{i}', json={"destUrl": ""})
                if req.json().get('PalletID') == '-1':
                    ActiveZone = ActiveZone + '0'
                else:
                    ActiveZone = ActiveZone + '1'
                    load = load + 1
            return (load, int(ActiveZone[::-1],base=2), ActiveZone[::-1])
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('[X] Decoding JSON has failed')


    def info(self):
        """
        This method gives information of object on which it is called
        :return: object information dictionary
        """
        return self.__dict__

    def get_access_token(self):
        try:
            ACCESS_URL = "https://keycloak-zdmp.platform.zdmp.eu/auth/realms/testcompany/protocol/openid-connect/token"
            headers = {'accept': "application/json", 'content-type': "application/x-www-form-urlencoded"}
            payload = "grant_type=password&client_id=ZDMP_API_MGMT_CLIENT&username=zdmp_api_mgmt_test_user&password=ZDMP2020!"
            response = requests.post(ACCESS_URL, data=payload, headers=headers)
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                self.access_token_time = int(time.time())
                self.expire_time = response.json().get('expires_in')
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print(f'[X-W-Tk] ({response.status_code})')
                self.sendEvent('Token', 'Accessing Token......')
            else:
                print(f"[X-W-Tk] {response.status_code}")
        except requests.exceptions.RequestException as err:
            self.sendEvent('Token', 'Not Accessed......')
            print("[X-W-Tk] OOps: Something Else", err)

    def simulate_measurements(self):      
            counter =0
            while True:
                if self.get_stop_simulation() == True:
                    print("[X-W-SM] in simulate_measurements-while")
                    break
                # PR values must be added
                records = MeasurementsForDemo.query.filter_by(WorkCellID=self.ID).all()
                for measurement in records:
                    counter =counter+1
                    if self.get_stop_simulation() == True:
                        print("[X-W-SM] in simulate_measurements-FOR ")
                        break
                    if int(time.time() - self.access_token_time) >= (self.expire_time - 50):
                        print(f'[X-W-SM] Accessing New Token.......')
                        self.get_access_token()
                    try:
                        # for real-time HighCharts
                        self.update_PVC(measurement.Power, measurement.RmsVoltage, measurement.RmsCurrent)
                        # sending measurements to ZDMP-DAQ
                        #for AI-ART
                        Power,Voltage,Current,az,lc= measurement.getRequiredData
                        features = np.round(np.array(np.append(CONFIG.Power_scaler.transform([[Power]]),
                                                            CONFIG.Load_scaler.transform([[lc]])),
                                                    ndmin=2), 4)
                        print(f'[X] {features},{measurement.Power}, {lc}')
                        payload = {"externalId": self.external_ID,
                                "fragment": f'belt-tension-class-pred'
                                }
                        # sending measurements to ZDMP-DAQ
                        req_V = requests.post(
                            url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=CurrentMeasurement&value={Current}&unit=A',
                            headers=self.headers)
                        req_A = requests.post(
                            url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=VoltageMeasurement&value={Voltage}&unit=V',
                            headers=self.headers)
                        req_P = requests.post(
                            url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=PowerMeasurement&value={Power}&unit=W',
                            headers=self.headers)
                        self.stop_recording_inc()
                        req_pred = requests.post(url=f'{CONFIG.SYNCH_URL}/sendCustomMeasurement',
                                                params=payload, headers=self.headers,
                                                json={"powerConsumption": round(features[0][0], 3),
                                                    "load": round(features[0][1], 3)})
                        self.update_PVC(measurement.Power, measurement.RmsVoltage, measurement.RmsCurrent)
                        if counter ==4:
                            req_pred = requests.post(url=f'{CONFIG.SYNCH_URL}/sendCustomMeasurement',
                                            params=payload, headers=self.headers,
                                            json={"powerConsumption": 0.015,
                                                "load":0.01})
                            counter =0
                        # time.sleep(.1)
                        print( f'[X-RqS] ({req_A.status_code}, {req_V.status_code}, {req_P.status_code}, {req_pred.status_code}, {counter})')
                        print(f'[X-Var] Record from DB({self.ID})....{Power}W-{self.stop_recording}-{az},{lc},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    except exc.SQLAlchemyError as err:
                        print("[X-W] OOps: Something Else", err)
                    except requests.exceptions.RequestException as err:
                        print("[X-W-SM] OOps: Something Else", err)
                self.set_stop_simulations(True) ##fix this line
                time.sleep(1)
                self.set_stop_simulations(False)
            print("[X-W-SM] Return from FUNC") 

  
    # *******************************************
    #   Flask Application
    # *******************************************

    def runApp(self):
        """
        Set the flask application
        :return:none
        """
        # ,
        app = Flask(__name__)  # template_folder='./workstations'
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{CONFIG.DB_USER}:{CONFIG.DB_PASSWORD}@{CONFIG.DB_SERVER}/{CONFIG.DB_NAME}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)

        # Flask application routes
        @app.route('/class', methods=['POST'])
        def labelUpdate():
            
            self.updateClassLabel(request.json.get("cl"),request.json.get("BT"),request.json.get("lc"))
            
            print(self.classLabel,self.BeltTension,self.LoadCombination)
            
            return "OK:"

        @app.route('/', methods=['GET','POST'])
        def home():
            if request.method == 'GET':
                context = {"ID": self.ID, "url": self.url_self}
                return render_template(f'workstations/Workstation.html', title=f'Wrk{self.ID}',
                brandUrl=f'http://{helper.get_local_ip()}:2000/',
                content=context)
            else:
                self.set_stop_recording()
                self.set_count()
                print(f'{self.stop_recording}')
                return "OK"

        @app.route('/info')  # ,methods=['GET']
        def info():
            info=WorkstationInfo.query.get(self.ID)
            return render_template(f'workstations/info.html',
                                   title='Information',
                                   info=WorkstationInfo.query.get(self.ID),
                                   brandUrl=f'http://{helper.get_local_ip()}:2000/')

        ###########Measurements for PR##########
# EM measurements from FASTory received here and stored to DB
        @app.route('/PR-measurements', methods=['GET', 'POST'])
        def measurements4PR():
         
            # if int(time.time() - self.access_token_time) >= (self.expire_time - 50):
            #     print(f'[X-W-sm] Accessing New Token.......')
            #     self.get_access_token()
            
            if request.method == 'GET':
            
                page = request.args.get('page',1,type=int)
                measurements = EnergyMeasurements.query.filter_by(WorkCellID=self.ID).order_by(
                    EnergyMeasurements.id.desc()).paginate(per_page=20, page=page )#[:500]
                if measurements:
                    return render_template(f'workstations/PR_measurements.html',
                                        title='History',
                                        contxt={"measurements":measurements,
                                                        "id":self.ID,
                                                        "hasEM":self.EM})
                else:
                    return render_template(f'workstations/PR_measurements.html',
                                        title='History',
                                        contxt={"measurements":measurements,
                                                        "id":self.ID,
                                                        "hasEM":self.EM})
            else:
                if self.EM:

                    # Averaging the power
                    #print(f'-----{request.json.get("active_power_c")}')
                    #if self.stop_recording <= 10000000:
                        l,lc,az = self.get_ZoneStatus()
                        data_in = request.json
                        motorPower = data_in.get("active_power_c")#motorPower = round(sum(self.powerlist) / len(self.powerlist), 3)
                        nominalPower = round((motorPower / 1000) * 100, 3)
                        #pred = helper.predict(nP,nL)
                        measurements = EnergyMeasurements( 
                            WorkCellID=self.ID,
                            RmsVoltage=data_in.get("rms_voltage_c"),
                            RmsCurrent=data_in.get("rms_current_c"),
                            Power=motorPower,
                            Nominal_Power=nominalPower,
                            ActiveZones=az,
                            LoadCombination = lc,#self.LoadCombination,
                            Load=l,
                            BeltTension = self.BeltTension,
                            TrueClass = self.classLabel,
                            # NormalizedPower = nP,
                            # NormalizedLoad = nL,
                            #PredictedClass = self.classLabel,#pred,
                            Fkey=data_in.get("CellID"),
                            line_Frequency = data_in.get("line_frequency")
                            
                            )
                        
                        # db.session.add(measurements)
                        # db.session.commit()
                        print(f'[X] {motorPower}W ,{self.stop_recording}, {az}, {l}, {lc}')
                        
                        self.stop_recording_inc()
                        # for real-time plot ---->  power,voltage,current
                        #self.update_PVC(motorPower, data_in.get("rms_voltage_c"), data_in.get("rms_current_c"))
                        return jsonify({"results": data_in.get("active_power_c")})
                self.stop_recording_inc()
                print(f'[X] {self.stop_recording}, {request.json.get("active_power_c")}W, {self.get_ZoneStatus()}')
                
                return 'NOT-OK'
        ########################################
        # EM measurements from FASTory received here and stored to DB
        @app.route('/measurements', methods=['GET', 'POST'])
        def insert_measurements2Db():
            
            #print(f'[X-W-sm] ({self.access_token_time}, {self.expire_time}, {int(time.time() - self.access_token_time)})')
            
            if int(time.time() - self.access_token_time) >= (self.expire_time - 50):
                print(f'[X-W-sm] Accessing New Token.......')
                self.get_access_token()
            
            if request.method == 'GET':
            
                page = request.args.get('page',1,type=int)
                measurements = MeasurementsForDemo.query.filter_by(WorkCellID=self.ID).order_by(
                    MeasurementsForDemo.id.desc()).paginate(per_page=20, page=page )#[:500]
                if measurements:
                    return render_template(f'workstations/measurements.html',
                                        title='History',
                                        contxt={"measurements":measurements,
                                                        "id":self.ID,
                                                        "hasEM":self.EM})
                else:
                    return render_template(f'workstations/measurements.html',
                                        title='History',
                                        contxt={"measurements":measurements,
                                                        "id":self.ID,
                                                        "hasEM":self.EM})
            else:
                if self.EM:
                    self.count_inc()
                    # Averaging the power
                    if self.stop_recording <= 100 :#<= 10 >=0
                        l,lc,az = self.get_ZoneStatus()
                        data_in = request.json
                        try:    
                            motorPower = data_in.get("active_power_c")#round(sum(self.powerlist) / len(self.powerlist), 3)
                            nominalPower = round((motorPower / 1000) * 100, 3)
                            # for real-time plot ---->  power,voltage,current
                            self.update_PVC(motorPower, data_in.get("rms_voltage_c"), data_in.get("rms_current_c"))
                            measurements = MeasurementsForDemo( #EnergyMeasurements MeasurementsForDemo
                                WorkCellID=self.ID,
                                RmsVoltage=data_in.get("rms_voltage_c"),
                                RmsCurrent=data_in.get("rms_current_c"),
                                Power=motorPower,
                                Nominal_Power=nominalPower,
                                ActiveZones=az,
                                Load=l,
                                Fkey=data_in.get("CellID"),
                                line_Frequency = data_in.get("line_frequency")
                                #info=data_in.get("CellID")
                                )

                            # db.session.add(measurements)
                            # db.session.commit()
                            #for AI-ART
                            features = np.round(np.array(np.append(CONFIG.Power_scaler.transform([[motorPower]]),
                                                                CONFIG.Load_scaler.transform([[lc]])),
                                                        ndmin=2), 4)
                            print(f'[X] {features},{motorPower}, {lc}')
                            payload = {"externalId": self.external_ID,
                                    "fragment": f'belt-tension-class-pred'
                                    }
                         # sending measurements to ZDMP-DAQ
                            req_V = requests.post(
                                url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=CurrentMeasurement&value={data_in.get("rms_current_c")}&unit=A',
                                headers=self.headers)
                            req_A = requests.post(
                                url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=VoltageMeasurement&value={data_in.get("rms_voltage_c")}&unit=V',
                                headers=self.headers)
                            req_P = requests.post(
                                url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=PowerMeasurement&value={motorPower}&unit=W',
                                headers=self.headers)
                            self.stop_recording_inc()
                            req_pred = requests.post(url=f'{CONFIG.SYNCH_URL}/sendCustomMeasurement',
                                                    params=payload, headers=self.headers,
                                                    json={"powerConsumption": round(features[0][0], 3),
                                                        "load": round(features[0][1], 3)})

                            print( f'[X-RqS] ({req_A.status_code}, {req_V.status_code}, {req_P.status_code}, {req_pred.status_code})')
                            print(f'[X-Var] Record added to DB({self.ID})....{motorPower}W-{self.stop_recording}-{az}-{l},{lc}')
                            return jsonify(res= 200)
                        except exc.SQLAlchemyError as err:
                                print("[X-W] OOps: Something Else", err)
                        except requests.exceptions.RequestException as err:
                            print("[X] OOps: Something Else", err)
                    else:
                        print(f'[X] Reset Counter {request.json.get("active_power_c")}')
                        time.sleep(0.1)
                        return jsonify(res= 200)
            return jsonify(res= 200)

        # for historic Data
        @app.route('/history', methods=['GET'])
        def historicPlot():
            records = MeasurementsForDemo.query.filter_by(WorkCellID=self.ID).all()
            #BT_record=EnergyMeasurements.query.filter_by(WorkCellID=self.ID).count()
            power_values= []
            #label = []
            voltage_values = []
            current_values = []
            #BT_Class = [x.PredictedClass for x in BT_record]
            BT_Class= [ EnergyMeasurements.query.filter_by(PredictedClass=1).count(),
                        EnergyMeasurements.query.filter_by(PredictedClass=2).count(),
                        EnergyMeasurements.query.filter_by(PredictedClass=3).count()]
            print(BT_Class)            
            for measurement in records:
                power_values.append(measurement.Power)
                voltage_values.append(measurement.RmsVoltage)
                current_values.append(measurement.RmsCurrent)
            label=[x for x in range(1,MeasurementsForDemo.query.filter_by(WorkCellID=self.ID).count())]
            print(BT_Class,power_values,voltage_values)
            return render_template(f'workstations/historicData.html',
                                    power = json.dumps(power_values),
                                    voltage = json.dumps(voltage_values),
                                    current = json.dumps(current_values),
                                    BTClass = json.dumps([60,283,157]),
                                    #BTClass = json.dumps(BT_Class),
                                    id=self.ID,
                                    brandUrl=f'http://{helper.get_local_ip()}:2000/',
                                    label = json.dumps(label))
        
        # for jQuery
        @app.route('/measurements/history', methods=['GET'])
        def history():
            from time import time
            x = int(time()) * 1000
            return jsonify([x, self.power])  # jsonify({"results":self.data})

        @app.route('/meaurements/real-time', methods=['GET'])
        def realTimePlot():
            from time import time
            return render_template(f'workstations/live_data.html', title='RT-Plot',
            brandUrl=f'http://{helper.get_local_ip()}:2000/',ID=self.ID)

        @app.route('/services', methods=['GET'])
        def services():
            return render_template(f'workstations/services.html')

        @app.route('/fastory_services', methods=['GET'])
        def fastory_services():
            return render_template(f'workstations/cnv_services.html', Z4=self.hasZone4)

        @app.route('/s1000_services', methods=['GET'])
        def s1000_services():
            print(f'[X-W-sS] {self.has_EM()}')
            return render_template(f'workstations/s1000_services.html', EM=self.has_EM())

        @app.route('/cnv_cmd', methods=['POST'])
        def cnv_cmd():
            # i do not want to change S1000 code
            cmd = request.form["cnv"]  # CNV section
            cnv = request.form["cmd"]  # comand
            if cnv == 'start':
                payload = {"cmd": cmd, "ReceiverADDR": self.url_self}
                try:
                    res = requests.post(f'{self.CNV_start_stop_url}StartUnCondition', json=payload, timeout= self.numFast)
                    res.raise_for_status()
                    flash(f'Status Code: {res.status_code}, Reason: {res.reason}')
                    return redirect(url_for('services'))
                    #jsonify({"payload": payload, "Status Code": r.status_code, "Reason": r.reason})
                except requests.exceptions.RequestException as err:
                    flash(f'Status: Unsuccessfull, Reason: {err}')
                    
                    print("[X-W-cC] OOps: Something Else", err)
                    return redirect(url_for('services'))
                #return jsonify({"payload": payload, "Message": "Not Connected to Line"}, {"Response": None})
            else:
                payload = {"cmd": cmd, "ReceiverADDR": self.url_self}
                try:
                    res = requests.post(f'{self.CNV_start_stop_url}StopUnCondition', json=payload,timeout=self.numFast)
                    res.raise_for_status()
                    flash(f'Status Code: {res.status_code}, Reason: {res.reason}')
                    return redirect(url_for('services'))
                    # jsonify(payload, {"Status Code": r.status_code, "Reason": r.reason})
                except requests.exceptions.RequestException as err:
                    print("[X-W-cC] OOps: Something Else", err)
                    flash(f'Status: Unsuccessfull, Reason: {err}')
                    return redirect(url_for('services'))
                #return jsonify({"payload": payload, "Message": "Not Connected to Line"}, {"Response": None})

        @app.route('/E10_services', methods=['POST'])
        def E10_services():
            cmd = request.form["cmd"]
            
            if cmd == 'start':
                # return jsonify({"cmd":cmd},{"Message": "Not Connected to Line" },{"Status-Code":403})
                res = self.invoke_EM_service(cmd)
                flash(str(res))
                return redirect(url_for('services'))#res
            else:
                res = self.invoke_EM_service()
                flash(str(res))
                return redirect(url_for('services'))# res

        @app.route('/api/energyService', methods =['POST'])
        def api_energyService():
            print(f'[X] Query Params converted to Dict--{request.args.to_dict()}')
            #instruction =request.args.to_dict().get("cmd")
            self.invoke_EM_service(cmd=request.args.to_dict().get("cmd"))
            return "ok"
###############################################
        
        @app.route('/api/simulation', methods=['POST'])
        def simulation():
            if request.method == 'POST':
              if request.args.to_dict().get("cmd") == "start":
                self.set_stop_simulations(False)
                time.sleep(0.5)
                send_loop_thread = threading.Thread(target=self.simulate_measurements)
                send_loop_thread.daemon = True
                send_loop_thread.start() 
              else:
                  self.set_stop_simulations(True)
            return "OK"
        
    
        app.run(host='0.0.0.0', port=self.port)#0.0.0.0 192.168.100.100
