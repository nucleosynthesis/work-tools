import ROOT 

# open the file 
import sys

fi = ROOT.TFile.Open(sys.argv[1])
region = sys.argv[2]
fit = "fit_b"

hs = fi.Get("shapes_prefit/%s_SR/VBFHtoInv"%region)

histos = {

 "DY"       : "$\cPZ/\gamma^{*}(\ell^{+}\ell^{-})$+\mathrm{jets}"
, "EWKZll"   : "$\cPZ/\gamma^{*}(\ell^{+}\ell^{-})$+\mathrm{jets} (VBF)"
, "EWKW"     : "$\PW(\ell\\nu)+\\textrm{jets}$ (VBF)"
, "WJETS"    : "$\PW(\ell\\nu)+\\textrm{jets}$ (strong)"
, "EWKZNUNU" : "$\cPZ(\\nu\\nu)+\\textrm{jets}$ (VBF)"
, "ZJETS"    : "$\cPZ(\\nu\\nu)+\\textrm{jets}$ (strong)"
, "VV"       : "Diboson"
, "QCD"       : "Multijet"
, "TOP"      : "$\\ttbar$ + single-top"
, "GluGluHtoInv"      : "$\mathrm{gg}\PH(\\rightarrow \mathrm{inv.})$"
, "VBFHtoInv"         : "$\mathrm{qq}\PH(\\rightarrow \mathrm{inv.})$"

}

order = [
"ZJETS"
,"EWKZNUNU"
,"WJETS"
,"EWKW"
,"TOP"
,"VV"
,"DY"
,"QCD"
#,"EWKZll"
,"GluGluHtoInv"
,"VBFHtoInv"
]

bins = ["%d-%d"%(hs.GetBinLowEdge(b),hs.GetBinLowEdge(b+1)) for b in range(1,hs.GetNbinsX())]
header = "Process & "+" & ".join(bins) + " & $\gt$%d  \\\\"%(hs.GetBinLowEdge(hs.GetNbinsX()))

table_lines = []
for proc in order: 
  if proc=="GluGluHtoInv" or proc=="VBFHtoInv": h = fi.Get("shapes_prefit/%s_SR/%s"%(region,proc))
  else: h = fi.Get("shapes_%s/%s_SR/%s"%(fit,region,proc))
  if proc == "DY" : 
    h2 = fi.Get("shapes_%s/%s_SR/EWKZll"%(fit,region)); h.Add(h2)
  bincontents = ""
  for b in range(h.GetNbinsX()):
    bw = h.GetBinWidth(b+1)
    if proc=="GluGluHtoInv" or proc=="VBFHtoInv": bincontents += " & $%.1f$"%(h.GetBinContent(b+1)*bw)
    else : bincontents += " & $%.1f\pm%.1f$"%(h.GetBinContent(b+1)*bw,h.GetBinError(b+1)*bw)
  if proc=="GluGluHtoInv" : table_lines.append("\\hline")
  table_lines.append("%s"%histos[proc]+" "+bincontents+"\\\\")

tabl = "\\begin{tabular}{l|"+"|".join(["c" for b in range(hs.GetNbinsX())])+"}"
data = "Observed & "+" & ".join(["0" for b in range(hs.GetNbinsX())]) + "\\\\"

#print "\\begin{table}"
print tabl
print header
print "\\hline"
print "\\hline"
for tl in table_lines: print tl 
print "\\hline"
print data
print "\\hline"
print "\\end{tabular}"
#print "\\end{table}"

#print "Total background pre-fit = ", (fi.Get("shapes_prefit/MTR_2017_SR/total_background")).Integral("width")
