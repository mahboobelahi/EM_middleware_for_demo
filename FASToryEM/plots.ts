
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { AppService } from '@app/core';
import { EventMqttService } from '@app/core/mqtt.service';
import { AlertService } from '@app/core/alert.service';
import { ErrorService } from '@app/core/error.service';
import { TranslateService } from '@ngx-translate/core';
import { Logger, LogLevel, I18nService } from '@app/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, filter, tap } from 'rxjs/operators';




		//JS-INIT-9DD4E7




		//JS-INIT-943281




		//JS-INIT-6C8F09

//JS-IMPORT-MARKER

const log = new Logger('App');

@Component({
  selector: 'app-PAGE_5D3581',
  templateUrl: './PAGE_5D3581.component.html',
  styleUrls: ['./PAGE_5D3581.component.scss']
})
export class PAGE_5D3581Component implements OnInit {
  

	//JS-ATTR-9DD4E7
		multi_9DD4E7: any[];
		view_9DD4E7: any[] = [window.innerWidth - 44 , window.innerHeight * 0.3];
		showXAxis_9DD4E7 = true;
		showYAxis_9DD4E7 = true;
		gradient_9DD4E7 = false;
		showLegend_9DD4E7 = false;
		showXAxisLabel_9DD4E7 = true;
		xAxisLabel_9DD4E7 = 'Time (s)';
		showYAxisLabel_9DD4E7 = true;
		yAxisLabel_9DD4E7 = 'Power (W)';
		colorScheme_9DD4E7 = {
			"domain": ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
		};
		source_9DD4E7 = "http://localhost/z_studio/sample_data/line-chart.json";
		autoScale_9DD4E7 = true; 
	//JS-ATTR-END-9DD4E7

	

	//JS-ATTR-943281
		multi_943281: any[];
		view_943281: any[] = [window.innerWidth - 44 , window.innerHeight * 0.3];
		showXAxis_943281 = true;
		showYAxis_943281 = true;
		gradient_943281 = false;
		showLegend_943281 = false;
		showXAxisLabel_943281 = true;
		xAxisLabel_943281 = 'Time (s)';
		showYAxisLabel_943281 = true;
		yAxisLabel_943281 = 'RmsVoltage (V)';
		colorScheme_943281 = {
			"domain": ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
		};
		source_943281 = "http://localhost/z_studio/sample_data/line-chart.json";
		autoScale_943281 = true; 
	//JS-ATTR-END-943281

	

	//JS-ATTR-6C8F09
		multi_6C8F09: any[];
		view_6C8F09: any[] = [window.innerWidth - 44 , window.innerHeight * 0.3];
		showXAxis_6C8F09 = true;
		showYAxis_6C8F09 = true;
		gradient_6C8F09 = false;
		showLegend_6C8F09 = false;
		showXAxisLabel_6C8F09 = true;
		xAxisLabel_6C8F09 = 'Time (s)';
		showYAxisLabel_6C8F09 = true;
		yAxisLabel_6C8F09 = 'Rms Current (A)';
		colorScheme_6C8F09 = {
			"domain": ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
		};
		source_6C8F09 = "http://localhost/z_studio/sample_data/line-chart.json";
		autoScale_6C8F09 = true; 
	//JS-ATTR-END-6C8F09

	//JS-ATTR-B29ED0
		single_B29ED0: any[];
		view_B29ED0: any[] = [window.innerWidth - 44 , window.innerHeight * 0.3];
		showXAxis_B29ED0 = true;
		showYAxis_B29ED0 = true;
		gradient_B29ED0 = false;
		showLegend_B29ED0 = false;
		showXAxisLabel_B29ED0 = true;
		xAxisLabel_B29ED0 = 'Country';
		showYAxisLabel_B29ED0 = true;
		yAxisLabel_B29ED0 = 'Population';
		colorScheme_B29ED0 = {
			"domain": ['#A10A28','#5AA454' , '#C7B42C', '#AAAAAA']
		};
		direction_B29ED0 = "vertical";
		source_B29ED0 = "http://localhost/z_studio/sample_data/bar-chart.json" 
	//JS-ATTR-END-B29ED0

	//JS-ATTR-MARKER

  constructor(public router: Router, public appService: AppService, public mqttService: EventMqttService, public translate: TranslateService, 
    private http: HttpClient, public errorService: ErrorService, public changeDetector: ChangeDetectorRef, public alertService: AlertService) {}

  ngOnInit() {
    

		//JS-INIT-9DD4E7
				this.init_linechart_9DD4E7();
		//JS-INIT-END-9DD4E7

		

		//JS-INIT-943281
				this.init_linechart_943281();
		//JS-INIT-END-943281

		

		//JS-INIT-6C8F09
				this.init_linechart_6C8F09();
		//JS-INIT-END-6C8F09

		//JS-INIT-B29ED0
				this.init_barchart_B29ED0();
		//JS-INIT-END-B29ED0

	//JS-INIT-MARKER
  }

  

	//JS-FNKT-9DD4E7
		onSelect_linechart_9DD4E7(event: any) {
			console.log(event);
		}

		init_linechart_9DD4E7() {
			let list1 = new Array();
			let list2 = new Array();
			let list3 = new Array();
			let count = 0; 
            let env = this;
            setTimeout(() => { 
                env.mqttService.msgBusMessagesSubscription.subscribe((messages: any) => {

                    //console.log("messages", messages) 

                    if(messages.length == 0) {
                        env.multi_9DD4E7 =  [
                            {"name": "Germany", "series": [
                                {"name": "2010", "value": 7555000},
                                {"name": "2011","value": 8940000}
                            ]},
                            {"name": "USA", "series": [
                                {"name": "2010","value": 7870000},
                                {"name": "2011", "value": 8270000}
                            ]},
                            {"name": "France", "series": [
                                {"name": "2010","value": 5000002},
                                {"name": "2011","value": 5800000}
                            ]}
                        ];
                    } else { 
                        
                        let jsonObj = JSON.parse(messages[messages.length-1].message)
                        let datapoint = {};
   
                        if (jsonObj.data.c8y_PowerMeasurement != undefined) {
                            datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
                            datapoint["name"] = count++;
                            list1.push(datapoint);
                        }
                        this.multi_9DD4E7 = [
                            {"name": "FASTory", "series": list1}
                        ];
                               
                        env.changeDetector.detectChanges(); 
                    }
                     
                }); 
            },750); 
			
            // Changed 
            /*this.message_9DD4E7$.subscribe((val: any) => {
				let jsonObj = JSON.parse(val.payload)
				let datapoint = {};
				if (jsonObj.data.c8y_PowerMeasurement != undefined) {
					datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
					datapoint["name"] = count++;
					list1.push(datapoint);
				}
				this.multi_9DD4E7 = [
					{"name": "device1", "series": list1}
				];
			});*/
            
			// use the commented code block to plot all the 
			/*
            datapoint["name"] = count++;
            if (jsonObj.data.c8y_PowerMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
                
                list1.push(datapoint);
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            } else if (jsonObj.data.c8y_VoltageMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_VoltageMeasurement.voltage.value;
                
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list1.length-1].value)}); 
                list2.push(datapoint); 
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            } else if (jsonObj.data.c8y_CurrentMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_CurrentMeasurement.current.value;
                
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list1.length-1].value)}); 
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push(datapoint);
            } else {
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list2.length-1].value)});
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            }
            
            console.log("this.multi_9DD4E7", list1,list2,list3)
            
            this.multi_9DD4E7 = [
                {"name": "device1", "series": list1},
                {"name": "device2", "series": list2},
                {"name": "device3", "series": list3}
            ];*/
		}
	//JS-FNKT-END-9DD4E7

	

	//JS-FNKT-943281
		onSelect_linechart_943281(event: any) {
			console.log(event);
		}

		init_linechart_943281() {
			let list1 = new Array();
			let list2 = new Array();
			let list3 = new Array();
			let count = 0; 
            let env = this;
            setTimeout(() => { 
                env.mqttService.msgBusMessagesSubscription.subscribe((messages: any) => {

                    //console.log("messages", messages) 

                    if(messages.length == 0) {
                        env.multi_943281 =  [
                            {"name": "Germany", "series": [
                                {"name": "2010", "value": 7555000},
                                {"name": "2011","value": 8940000}
                            ]},
                            {"name": "USA", "series": [
                                {"name": "2010","value": 7870000},
                                {"name": "2011", "value": 8270000}
                            ]},
                            {"name": "France", "series": [
                                {"name": "2010","value": 5000002},
                                {"name": "2011","value": 5800000}
                            ]}
                        ];
                    } else { 
                        
                        let jsonObj = JSON.parse(messages[messages.length-1].message)
                        let datapoint = {};
   
                        if (jsonObj.data.c8y_VoltageMeasurement != undefined) {
                            datapoint["value"] = jsonObj.data.c8y_VoltageMeasurement.voltage.value;
                            datapoint["name"] = count++;
                            list1.push(datapoint);
                        }
                        this.multi_943281 = [
                            {"name": "device1", "series": list1}
                        ];
                               
                        env.changeDetector.detectChanges(); 
                    }
                     
                }); 
            },750); 
			
            // Changed 
            /*this.message_943281$.subscribe((val: any) => {
				let jsonObj = JSON.parse(val.payload)
				let datapoint = {};
				if (jsonObj.data.c8y_PowerMeasurement != undefined) {
					datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
					datapoint["name"] = count++;
					list1.push(datapoint);
				}
				this.multi_943281 = [
					{"name": "device1", "series": list1}
				];
			});*/
            
			// use the commented code block to plot all the 
			/*
            datapoint["name"] = count++;
            if (jsonObj.data.c8y_PowerMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
                
                list1.push(datapoint);
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            } else if (jsonObj.data.c8y_VoltageMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_VoltageMeasurement.voltage.value;
                
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list1.length-1].value)}); 
                list2.push(datapoint); 
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            } else if (jsonObj.data.c8y_CurrentMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_CurrentMeasurement.current.value;
                
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list1.length-1].value)}); 
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push(datapoint);
            } else {
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list2.length-1].value)});
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            }
            
            console.log("this.multi_943281", list1,list2,list3)
            
            this.multi_943281 = [
                {"name": "device1", "series": list1},
                {"name": "device2", "series": list2},
                {"name": "device3", "series": list3}
            ];*/
		}
	//JS-FNKT-END-943281

	

	//JS-FNKT-6C8F09
		onSelect_linechart_6C8F09(event: any) {
			console.log(event);
		}

		init_linechart_6C8F09() {
			let list1 = new Array();
			let list2 = new Array();
			let list3 = new Array();
			let count = 0; 
            let env = this;
            setTimeout(() => { 
                env.mqttService.msgBusMessagesSubscription.subscribe((messages: any) => {

                    //console.log("messages", messages) 

                    if(messages.length == 0) {
                        env.multi_6C8F09 =  [
                            {"name": "Germany", "series": [
                                {"name": "2010", "value": 7555000},
                                {"name": "2011","value": 8940000}
                            ]},
                            {"name": "USA", "series": [
                                {"name": "2010","value": 7870000},
                                {"name": "2011", "value": 8270000}
                            ]},
                            {"name": "France", "series": [
                                {"name": "2010","value": 5000002},
                                {"name": "2011","value": 5800000}
                            ]}
                        ];
                    } else { 
                        
                        let jsonObj = JSON.parse(messages[messages.length-1].message)
                        let datapoint = {};
   
                        if (jsonObj.data.c8y_CurrentMeasurement != undefined) {
                            datapoint["value"] = jsonObj.data.c8y_CurrentMeasurement.current.value;
                            datapoint["name"] = count++;
                            list1.push(datapoint);
                        }
                        this.multi_6C8F09 = [
                            {"name": "FASTory", "series": list1}
                        ];
                               
                        env.changeDetector.detectChanges(); 
                    }
                     
                }); 
            },750); 
			
            // Changed 
            /*this.message_6C8F09$.subscribe((val: any) => {
				let jsonObj = JSON.parse(val.payload)
				let datapoint = {};
				if (jsonObj.data.c8y_PowerMeasurement != undefined) {
					datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
					datapoint["name"] = count++;
					list1.push(datapoint);
				}
				this.multi_6C8F09 = [
					{"name": "device1", "series": list1}
				];
			});*/
            
			// use the commented code block to plot all the 
			/*
            datapoint["name"] = count++;
            if (jsonObj.data.c8y_PowerMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_PowerMeasurement.power.value;
                
                list1.push(datapoint);
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            } else if (jsonObj.data.c8y_VoltageMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_VoltageMeasurement.voltage.value;
                
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list1.length-1].value)}); 
                list2.push(datapoint); 
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            } else if (jsonObj.data.c8y_CurrentMeasurement != undefined) {
                datapoint["value"] = jsonObj.data.c8y_CurrentMeasurement.current.value;
                
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list1.length-1].value)}); 
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push(datapoint);
            } else {
                list1.push({"name": count, "value": (list1.length == 0 ? 0 : list1[list2.length-1].value)});
                list2.push({"name": count, "value": (list2.length == 0 ? 0 : list2[list2.length-1].value)});
                list3.push({"name": count, "value": (list3.length == 0 ? 0 : list3[list3.length-1].value)});
            }
            
            console.log("this.multi_6C8F09", list1,list2,list3)
            
            this.multi_6C8F09 = [
                {"name": "device1", "series": list1},
                {"name": "device2", "series": list2},
                {"name": "device3", "series": list3}
            ];*/
		}
	//JS-FNKT-END-6C8F09

	//JS-FNKT-B29ED0
		onSelect_barchart_B29ED0(event: any) {
			console.log(event);
		}
		
		init_barchart_B29ED0() {
			if(this.direction_B29ED0 === "horizontal") {
				var tmp = this.xAxisLabel_B29ED0;
				this.xAxisLabel_B29ED0 = this.yAxisLabel_B29ED0;
				this.yAxisLabel_B29ED0 = tmp; 
			}
            let list1 = [
                            {"name": "Class1",	"value": 0 },
                            { "name": "Class2", "value": 0 },
                            {"name": "Class3", "value": 0 }
                        ] ;
			let count1 = 0
            let count2 = 0
            let count3 = 0; 
            let env = this;

            setTimeout(() => { 
                    env.mqttService.msgBusMessagesSubscription.subscribe((messages: any) => {
    
                        //console.log("messages", messages) 
    
                        if(messages.length == 0) {
                            //this.single_B29ED0 = list1;
                            env.single_B29ED0 = [
                                {"name": "Germany",	"value": 8940000 },
                                { "name": "USA", "value": 5000000 },
                                {"name": "France", "value": 7200000 }
                            ];
                        } else {
                            let jsonObj = JSON.parse(JSON.parse(messages[messages.length-1].message))
       
                            if (jsonObj.BT_Class == 1) {
                                list1[0].value =count1++;
                                //list1[0].name = "Class1";
                                console.log("Class1>>>>",list1[0]);
                            }
                            if (jsonObj.BT_Class == 2) {
                                list1[1].value =count2++;
                                //list1[1].name = "Class2";
                                console.log("Class2>>>>",list1[1]);
                            }
                            if (jsonObj.BT_Class == 3) {
                                list1[2].value =count3++;
                                //list1[2].name = "Class3";
                                console.log("Class3>>>>",list1[2]);
                            }
                            console.log(list1);
                            
                            //env.changeDetector.detectChanges();
                            this.single_B29ED0 = [
                                list1[0],list1[1],list1[2]
                            ];
                        }
                         
                    }); 
                },750);
				
		}
	//JS-FNKT-END-B29ED0

	//JS-FNKT-MARKER
}
