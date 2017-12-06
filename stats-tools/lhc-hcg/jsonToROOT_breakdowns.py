import json
import ROOT as r
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

import sys,os
name = sys.argv[1]
import parameters

def strtoverb(stri):
	return stri.replace("_"," ")
	#return "'\'verb{%s}"%stri

with open(name+".json") as data_file:
	data = json.load(data_file)

def makeBarChart(MODEL,entry,params):
	histT = r.TH1F("newbar",";;",len(params),0,len(params))  
	histE = r.TH1F("newbarE",";;",len(params),0,len(params))  
	histS = r.TH1F("newbarS",";;",len(params),0,len(params))  
	histSth = r.TH1F("newbarSth",";;",len(params),0,len(params))  
	histBth = r.TH1F("newbarBth",";;",len(params),0,len(params))  
	histT.SetBarWidth(0.1)	
	histE.SetBarWidth(0.1)	
	histS.SetBarWidth(0.1)	
	histSth.SetBarWidth(0.1)	
	histBth.SetBarWidth(0.1)	
	histT.SetBarOffset(0.)	
	histE.SetBarOffset(0.1)	
	histS.SetBarOffset(0.2)	
	histSth.SetBarOffset(0.3)	
	histBth.SetBarOffset(0.4)
	histT.SetTitle("%s"%MODEL)
	histT.GetYaxis().SetTitle("Symmetric uncertainty")
	histT.GetYaxis().SetTitleOffset(1.5)
	histT.GetYaxis().SetTitleSize(0.03)
	for i,p in enumerate(params):
		 histT.GetXaxis().SetBinLabel(i+1,p)
		 histT.SetBinContent(i+1,0.5*(abs(entry[p]["ErrorHi"])+abs(entry[p]["ErrorLo"])))
		 histE.SetBinContent(i+1,0.5*(abs(entry[p]["ExpHi"])+abs(entry[p]["ExpLo"])))
		 histS.SetBinContent(i+1,0.5*(abs(entry[p]["StatHi"])+abs(entry[p]["StatLo"])))
		 histSth.SetBinContent(i+1,0.5*(abs(entry[p]["SigThHi"])+abs(entry[p]["SigThLo"])))
		 histBth.SetBinContent(i+1,0.5*(abs(entry[p]["BkgThHi"])+abs(entry[p]["BkgThLo"])))

	histT.SetLineColor(1)	
	histE.SetLineColor(1)	
	histS.SetLineColor(1)	
	histBth.SetLineColor(1)	
	histSth.SetLineColor(1)
	
	histT.SetFillColor(r.kCyan+1)	
	histE.SetFillColor(r.kRed+1)	
	histS.SetFillColor(r.kBlue-4)	
	histBth.SetFillColor(r.kGreen+3)	
	histSth.SetFillColor(r.kOrange+1)	
	
	leg=r.TLegend(0.6,0.7,0.89,0.89)
	leg.SetFillColor(0)
	leg.SetTextFont(42)
	leg.AddEntry(histT,"Total","F")
	leg.AddEntry(histE,"Expt","F")
	leg.AddEntry(histS,"Stat","F")
	leg.AddEntry(histSth,"Sig Th","F")
	leg.AddEntry(histBth,"Bkg Th","F")

	canv = r.TCanvas("c","c",300,360)
	histT.Draw("barL")
	histE.Draw("barsameL")
	histS.Draw("barsameL")
	histSth.Draw("barsameL")
	histBth.Draw("barsameL")
	leg.Draw()
	#canv.SetLogy()
	canv.SaveAs("%s_%s.pdf"%(name,MODEL))

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

latex_out = open("latex_%s.tex"%name,"w")
latex_out.write("\\documentclass{article} \n")
latex_out.write("\\begin{document} \n")

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
		  if data[MODEL][p]["ValidOtherLimitHi"]: 
			print "Including some negative scans"
			ext = " -g 5 "
        if not allParamsOk: 
		print "Missing parameters (skipping) !!! -- ", missingpars
		continue
	
        if not data[MODEL][params[0]].has_key("StatHi"): continue 
        if not data[MODEL][params[0]].has_key("ExpHi"): continue 
	# Make a nice table of things 
	latex_out.write("\\begin{table}[htbp]\n")
	latex_out.write("\\begin{center}\n")
	latex_out.write("\\caption{%s}\n"%strtoverb(MODEL))
	latex_out.write("\\begin{tabular}{|l|c|cccc|}\n")
	latex_out.write("\\hline\n")
	latex_out.write("Parameter & Value & Exp syst & Bkg Th syst & Sig Th syst & Stat \\\ \n \\hline \n& & & & & \\\ \n")
	for p in params: 
		latex_out.write("%s & $%.2f ^{+%.2f}_{%.2f}$ & $^{+%.2f}_{%.2f}$ & $^{+%.2f}_{%.2f}$ & $^{+%.2f}_{%.2f}$ & $^{+%.2f}_{%.2f}$ \\\ \n  & & & & & \\\ \n "%(\
		 strtoverb(p) \
		 ,data[MODEL][p]["Val"] \
		, data[MODEL][p]["ErrorHi"]\
		, data[MODEL][p]["ErrorLo"]\
		, data[MODEL][p]["ExpHi"]\
		, data[MODEL][p]["ExpLo"]\
		, data[MODEL][p]["BkgThHi"]\
		, data[MODEL][p]["BkgThLo"]\
		, data[MODEL][p]["SigThHi"]\
		, data[MODEL][p]["SigThLo"]\
		, data[MODEL][p]["StatHi"]\
		, data[MODEL][p]["StatLo"]\
		))

	latex_out.write("\\hline\n")
        latex_out.write("\\end{tabular} \n")
        latex_out.write("\\end{center} \n")
        latex_out.write("\\end{table} \n")

        makeBarChart(MODEL,data[MODEL],params)

	output.write("\npython makeRooFile.py %s %s_%s "%(ext,name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorHi"],abs(data[MODEL][p]["ErrorHi"])))
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorLo"],abs(data[MODEL][p]["ErrorLo"])))
		if len(ext):
	    	 if data[MODEL][p].has_key("ValidOtherLimitHi") and abs(data[MODEL][p]["OtherLimitLo"]) < 900:
			output.write(" %d,%g "%(0,(data[MODEL][p]["OtherLimitLo"])))  # Negative ranges 
			output.write(" %d,%g "%(0,(data[MODEL][p]["OtherLimitHi"])))  
	    	 else: 
			output.write(" %d,%g "%(1,-999))  # Negative ranges 
			output.write(" %d,%g "%(1,-999))  
	
	output.write("\npython makeRooFile.py %s sig2_%s_%s "%(ext,name,MODEL)) 	# 2 sigma
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorHi"],abs(data[MODEL][p]["2sig_ErrorHi"])))
		output.write(" %d,%g "%(not data[MODEL][p]["ValidErrorLo"],abs(data[MODEL][p]["2sig_ErrorLo"])))
		
		if len(ext):
	    	 if data[MODEL][p].has_key("ValidOtherLimitHi") and abs(data[MODEL][p]["2sig_OtherLimitLo"]) < 900  :
			output.write(" %d,%g "%(0,(data[MODEL][p]["2sig_OtherLimitLo"])))  # Negative ranges 
			output.write(" %d,%g "%(0,(data[MODEL][p]["2sig_OtherLimitHi"])))  
	    	 else: 
			output.write(" %d,%g "%(1,-999))  # Negative ranges 
			output.write(" %d,%g "%(1,-999))  


        if not data[MODEL][params[0]].has_key("StatHi"): continue 
        if not data[MODEL][params[0]].has_key("ExpHi"): continue 
	output.write("\npython makeRooFile.py stat_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" 0,%g "%abs(data[MODEL][p]["StatHi"]))
		output.write(" 0,%g "%abs(data[MODEL][p]["StatLo"]))

	output.write("\npython makeRooFile.py thsig_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" 0,%g "%abs(data[MODEL][p]["SigThHi"]))
		output.write(" 0,%g "%abs(data[MODEL][p]["SigThLo"]))
	output.write("\npython makeRooFile.py thbkg_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" 0,%g "%abs(data[MODEL][p]["BkgThHi"]))
		output.write(" 0,%g "%abs(data[MODEL][p]["BkgThLo"]))
	output.write("\npython makeRooFile.py exp_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		output.write(" 0,%g "%abs(data[MODEL][p]["ExpHi"]))
		output.write(" 0,%g "%abs(data[MODEL][p]["ExpLo"]))

	output.write("\npython makeRooFile.py sys_%s_%s "%(name,MODEL))
	for p in params: 
		output.write(" 0,%g "%data[MODEL][p]["Val"])
		eU = (abs(data[MODEL][p]["ErrorHi"])**2) - (abs(data[MODEL][p]["StatHi"])**2) 
		eD = (abs(data[MODEL][p]["ErrorLo"])**2) - (abs(data[MODEL][p]["StatLo"])**2) 
		eU=eU**0.5
		eD=eD**0.5
		output.write(" 0,%g "%eU)
		output.write(" 0,%g "%eD)

print "Created - ", output.name
os.system('chmod +x %s'%output.name)
latex_out.write("\\end{document} \n")
