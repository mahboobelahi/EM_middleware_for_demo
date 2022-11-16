#related to middleware app only
import joblib
#DB#####
DB_USER="FASToryPowerConsumption"
DB_PASSWORD = "FASToryPR2021!"
DB_SERVER = "localhost"
DB_NAME = "PowerConsumption"
#globals for application
appLocIP = '0.0.0.0'#'192.168.100.100'
appLocPort = 2000#change it back to 2000
WorkStations = [1,2,3,4,5,6,7,8,9,10,11,12] #FASTory Line's workcells
wrkCellLocIP = '192.168.100.100'
wrkCellLocPort = 2000
hav_no_EM = [1,7,8] #  workcells that have no/out of order EM modules
energy_meters=[2,3,4,5,6,9,10,11,12]
FILE_NAME = 'testData.csv'#forWorksation10_PR.csv#testData_349.csv'#'s_Measurements10.csv'
make = ["Yaskawa","Sony","Kuka","ABB","Omron-Adept","Sony","N/A","Omron-Adept","Sony","Sony","Sony","Sony"]
type = ["Dual-Arm","SCARA","6-axis","6-axis","6-axis","SCARA","N/A","SCARA-eCobra","SCARA","SCARA","SCARA","SCARA"]
# loading MinMaxScaler Objects
Load_scaler = joblib.load('pallet-scaler.save')#loadScalerjb.save pallet-scaler.save
Power_scaler = joblib.load('Power-scaler.save')#powerScalerjb.save Power-scaler.save
num_Fast=60
num=60
#DAQ URLs
ADMIN_URL = f'http://apigw-zdmp.platform.zdmp.eu/gateway/data-acquisition-admin-service/v0'#f'http://192.168.100.100:30025'
ASYNCH_URL = f'http://apigw-zdmp.platform.zdmp.eu/gateway/data-acquisition-asynch-service/v0' #f'http://192.168.100.100:30026'
SYNCH_URL =  f'http://apigw-zdmp.platform.zdmp.eu/gateway/data-acquisition-synch-service/v0' #f'http://192.168.100.100:30027'
TOPIC_TYPE= 'multi'
#JWT token
ACCESS_URL = "https://keycloak-zdmp.platform.zdmp.eu/auth/realms/testcompany/protocol/openid-connect/token"
headers = {'accept': "application/json", 'content-type': "application/x-www-form-urlencoded"}
payload = "grant_type=password&client_id=ZDMP_API_MGMT_CLIENT&username=zdmp_api_mgmt_test_user&password=ZDMP2020!"
 
##############################MQTT-Settings###########################################
BASE_TOPIC ='TAU/FASTory/cmd'
Conn_ALIVE = 5#60
NAME = 'FAST-LAB'
MQTT_CLIENT_ID = 'FASToryEMOrchestrator'
zMSG_PORT_VPN = 30204
zMSG_TLS_PORT = 8883#30206
zMQTT_BROKER_URL_VPN = '192.168.100.100'
zMQTT_BROKER_URL = 'msgbus-zdmp.platform.zdmp.eu'  # public ZDMP messageBus
#MQTT_BROKER_PORT = zMSG_PORT  # default port for non-tls connection
MQTT_USERNAME = 'tau'  # set the username here if you need authentication for the broker
MQTT_PASSWORD = 'ZDMP-tau2020!' # set the password here if the broker demands authentication
MQTT_KEEPALIVE = Conn_ALIVE  # set the time interval for sending a ping to the broker to 5 seconds
MQTT_TLS_ENABLED_VPN = False
MQTT_TLS_ENABLED = True  # set TLS to disabled for testing purposes
MQTT_TLS_CERTFILE = './files/ca_certificate.pem' 
MQTT_REFRESH_TIME = 1.0  # refresh time in seconds

# ZDMP-Cumulocity IoT tenant credentials
#No more required in updated version of DAQ 
# domain = "https://zdmp-da.eu-latest.cumulocity.com"
# TenantID = "t59849255/mahboob.elahi@tuni.fi"
# passward = "mahboobelahi93"
