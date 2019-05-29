import ROOT

r = ROOT.TRandom3();

fi = ROOT.TFile.Open("output_average_sums.root")
fout = ROOT.TFile("output_profiles.root","RECREATE")

gr_AVE = ROOT.TGraph()
gr_all_AVE = ROOT.TGraph2D()

gr_AVE1 = ROOT.TGraphErrors()
gr_AVE2 = ROOT.TGraph()
gr_AVE3 = ROOT.TGraph()

keys = fi.GetListOfKeys()
pt = 0;
allpts = 0 
fout.cd()
for key in keys :
  h = key.ReadObj()
  esp = h.GetName()
  if "ieta" not in esp: continue 
  if "XET" in esp: continue
  if "YET" in esp: continue

  sign = 1
  if "neg" in esp: sign = -1
  ieta = sign*int(esp[esp.rfind("_")+1:])
  
  for i in range(0,100): 
    aveE = (h.ProjectionY("%f"%r.Uniform(0,1),i,i)).GetMean()
    gr_all_AVE.SetPoint(allpts,ieta,i,aveE)

    allpts+=1
  
  sumE = (h.ProjectionY("%f"%r.Uniform(0,1),0,99)).GetMean() 
  gr_AVE.SetPoint(pt,ieta,sumE)

  sumE1 = (h.ProjectionY("%f"%r.Uniform(0,1),0,11)).GetMean() 
  sumE2 = (h.ProjectionY("%f"%r.Uniform(0,1),11,21)).GetMean() 
  sumE3 = (h.ProjectionY("%f"%r.Uniform(0,1),21,32)).GetMean() 

  gr_AVE1.SetPoint(pt,ieta,sumE1)
  gr_AVE2.SetPoint(pt,ieta,sumE2)
  gr_AVE3.SetPoint(pt,ieta,sumE3)

  pt+=1
  
  CNV = ROOT.TCanvas("c","c",660,600)
  CNV.SetName(h.GetName()+"_canv")
  CNV.SetRightMargin(0.18)
  h.Draw("colz")
  h.GetXaxis().SetTitle("NTT |ieta|<=15")
  h.GetYaxis().SetTitle("ET - Region (rank)")
  h.GetYaxis().SetTitleOffset(1.2)
  prof = h.ProfileX()
  prof.SetLineColor(2); 
  prof.SetMarkerColor(2);
  prof.SetLineWidth(3);

  prof.Draw("same")
  CNV.Write()
  ROOT.gStyle.SetOptStat(0)
  CNV.SetLogz()
  CNV.SaveAs("PROFILES/%s.pdf"%(CNV.GetName()))


for pt in range(gr_all_AVE.GetN()):
  x = gr_all_AVE.GetX()[pt]
  y = gr_all_AVE.GetY()[pt]
  z = gr_all_AVE.GetZ()[pt]

  #print "ieta, NTT, <E>", x,y,z

gr_all_AVE.SetName("LUT"); gr_all_AVE.Write()
gr_AVE.SetName("aveE_vs_iEta"); gr_AVE.Write()
gr_AVE1.SetName("aveE_vs_iEta_1"); gr_AVE1.Write()
gr_AVE2.SetName("aveE_vs_iEta_2"); gr_AVE2.Write()
gr_AVE3.SetName("aveE_vs_iEta_3"); gr_AVE3.Write()


