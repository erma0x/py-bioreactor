# Bioreactor 

### Description
IoT and microbiology with Python, RaspberryPi and Arduino for a self-controlled system for the growth of microorganisms.

### Status 
in development

### What is it a bioreactor
A bioreactor refers to any manufactured device or system that supports a biologically active environment. In one case, a bioreactor is a vessel in which a chemical process is carried out which involves organisms or biochemically active substances derived from such organisms. This process can either be aerobic or anaerobic. These bioreactors are commonly cylindrical, ranging in size from litres to cubic metres, and are often made of stainless steel. It may also refer to a device or system designed to grow cells or tissues in the context of cell culture. These devices are being developed for use in tissue engineering or biochemical/bioprocess engineering.

![Alt Text](/docs/img/Bioreactor_process.jpg?raw=True) 

## Supported functions
### Food
	instrumentation: solenoid valves, timers, relays, transistors
	nutrients: CO2, Peptones, sugar, lipids, sterilized water 30min

### OD
	instrumentation: laser, photoresistor
	date: OD value, measurement time, column


### Salinity
	instrumentation: solenoid valves (x2), timer
	date: salinity value, measurement time, column

### pH
	instrumentation: Phaccamentro, transistor
	date: ph value, measurement time, column number

### Temperature
	instruments: heating band, Peltie cell, thermometer
	data: temperature value, measurement time, column number

### Reservoir
	instrumentation: solenoid valve
	date: quantity left, measurement time, column number

### Air
	instrumentation: solenoid valve, peristalsic pump for air
	date: intensity, on / off cycle time
