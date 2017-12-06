import json
import sys,os
name = sys.argv[1]
import parameters
with open(name+".json") as data_file:
	data = json.load(data_file)


# add mu to a1_5D 


if "A1_5P" in data.keys() :
 data["A1_5P"]["mu"] = data["A1_mu"]["mu"]
 data["A1_4P"]["mu"] = data["A1_mu"]["mu"]

if "K2" in data.keys(): 
 data["K2_BSM0"]=data["K2"].copy()
 data["K2_BSM0"]["BRinv"] = data["K2_BSM"]["BRinv"].copy()
 for k in data["K2_BSM0"]['BRinv'].keys(): 
  data["K2_BSM0"]['BRinv'][k]=0.

output = open("conversion_%s.sh"%name,"w")
output.write("#!/bin/bash\n")


for MODEL in data.keys():
	if MODEL not in parameters.parameter_order: continue 
        print MODEL, "--->"
	params = parameters.parameter_order[MODEL]
	ext = ""
	#for p in params : 
	#	if p in ["lambda_tg","lambda_WZ"]: ext = " -g 5 "
	allParamsOk = True
	missingpars = []
	for p in params:
		if not data[MODEL].has_key(p):
		  missingpars.append(p)
		  allParamsOk=False
		if data[MODEL][p].has_key("ValidOtherLimitHi"): 
		  if data[MODEL][p]["ValidOtherLimitHi"] or data[MODEL][p]["2sig_ValidOtherLimitHi"]: 
			print "Including some negative scans"
			ext = " -g 5 "
        if not allParamsOk: 
		print "Missing parameters (skipping) !!! -- ", missingpars
		continue
	
	output.write("\npython makeRooFile.py %s %s_%s "%(ext,name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorHi"],abs(data[MODEL][p]["ErrorHi"])))
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorLo"],abs(data[MODEL][p]["ErrorLo"])))
		if len(ext):
	    	 if data[MODEL][p].has_key("ValidOtherLimitHi"):
		     if  (data[MODEL][p]["ValidOtherLimitHi"]) and abs(data[MODEL][p]["OtherLimitLo"]) < 900   :
			output.write(" %d,%g "%(0,(data[MODEL][p]["OtherLimitLo"])))  # Negative ranges 
			output.write(" %d,%g "%(0,(data[MODEL][p]["OtherLimitHi"])))  
		     else :
			output.write(" %d,%g "%(1,-999))  # Negative ranges 
			output.write(" %d,%g "%(1,-999))  
	    	 else: 
			output.write(" %d,%g "%(1,-999))  # Negative ranges 
			output.write(" %d,%g "%(1,-999))  

	output.write("\npython makeRooFile.py %s sig2_%s_%s "%(ext,name,MODEL)) 	# 2 sigma
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorHi"],abs(data[MODEL][p]["2sig_ErrorHi"])))
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorLo"],abs(data[MODEL][p]["2sig_ErrorLo"])))
		
		if len(ext):
	    	 if data[MODEL][p].has_key("2sig_ValidOtherLimitHi") :
		     if  (data[MODEL][p]["2sig_ValidOtherLimitHi"]) and abs(data[MODEL][p]["2sig_OtherLimitLo"]) < 900   :
			output.write(" %d,%g "%(0,(data[MODEL][p]["2sig_OtherLimitLo"])))  # Negative ranges 
			output.write(" %d,%g "%(0,(data[MODEL][p]["2sig_OtherLimitHi"]))) 
		     else:  
			output.write(" %d,%g "%(1,-999))  # Negative ranges 
			output.write(" %d,%g "%(1,-999))  
	    	 else: 
			output.write(" %d,%g "%(1,-999))  # Negative ranges 
			output.write(" %d,%g "%(1,-999))  


        if not data[MODEL][params[0]].has_key("Stat"): continue 
	output.write("\npython makeRooFile.py stat_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" 0,%g "%abs(data[MODEL][p]["Stat"]["ErrorHi"]))
		output.write(" 0,%g "%abs(data[MODEL][p]["Stat"]["ErrorLo"]))

	output.write("\npython makeRooFile.py sys_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		eU = (abs(data[MODEL][p]["ErrorHi"])**2) - (abs(data[MODEL][p]["Stat"]["ErrorHi"])**2) 
		eD = (abs(data[MODEL][p]["ErrorLo"])**2) - (abs(data[MODEL][p]["Stat"]["ErrorLo"])**2) 
		eU=eU**0.5
		eD=eD**0.5
		output.write(" 0,%g "%eU)
		output.write(" 0,%g "%eD)

print "Created - ", output.name
os.system('chmod +x %s'%output.name)
