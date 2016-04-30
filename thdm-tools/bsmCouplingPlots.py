import array 
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)
# very fine-grained colour palettee
def set_palette(ncontours=999):
    style=1
    if (style==1):
     # default palette, looks cool
     stops = [0.00, 0.34, 0.61, 0.84, 1.00]
     red   = [0.00, 0.00, 0.77, 0.85, 0.90]
     green = [0.00, 0.81, 1.00, 0.20, 0.00]
     blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)
    elif (style==3):
     
     red   = [ 0.00, 0.90, 1.00] 
     blue  = [ 1.00, 0.50, 0.00] 
     green = [ 0.00, 0.00, 0.00] 
     stops = [ 0.00, 0.50, 1.00] 
     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)

    elif (style==2):
     # blue palette, looks cool
     stops = [0.00, 0.14, 0.34, 0.61, 0.84, 1.00]
     red   = [0.00, 0.00, 0.00, 0.05, 0.30, 1.00]
     green = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
     blue  = [1.00, 0.80, 0.6, 0.4, 0.2, 0.0]

     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)

    npoints = len(st)
    r.TColor.CreateGradientColorTable(npoints, st, re, gr, bl, ncontours)
    r.gStyle.SetNumberContours(ncontours)

def makeHC(gr,xt,yt,lconst,logy=0):
  cv = r.TCanvas("c","",600,600); cv.SetName(gr.GetName())
  gr.SetMaximum(10)
  h2 = gr.GetHistogram(); h2.SetTitle("")
  h2.GetXaxis().SetTitle(xt)
  h2.GetYaxis().SetTitle(yt)
  h2CL = h2.Clone("sig1")
  h2CL.SetContour(2)
  h2CL.SetContourLevel(1,2.3)
  h2CL.SetLineWidth(3)
  h2CL.SetLineColor(1)
  h2CL2 = h2.Clone("sig2")
  h2CL2.SetContour(2)
  h2CL2.SetContourLevel(1,6.18)
  h2CL2.SetLineWidth(3)
  h2CL2.SetLineColor(1)
  h2CL2.SetLineStyle(2)

  ranges = [[0.,3.], [0.,3.],[-2.5,2.5] ]
  cgraphs = []
  cgraphsDRAW = []
  grIs = []
  for i,lc in enumerate(lconst):
    cc = 0
    grI = r.TGraph()
    lchist = lc.GetHistogram()
    lch = lchist.Clone()
    for x in range(lch.GetNbinsX()): 
     for y in range(lch.GetNbinsY()): 
       if (lch.GetBinContent(x,y) > ranges[i][1] or lch.GetBinContent(x,y) < ranges[i][0]): 
       	XV = (lch.GetXaxis().GetBinCenter(x)) 
	YV = (lch.GetYaxis().GetBinCenter(y))
        #print "outch, out of bounds", lch.GetName(), XV, YV, lch.GetBinContent(x,y)
       	grI.SetPoint(cc,XV,YV) 
	cc+=1
	
	#lch.SetBinContent(x,y,10)

       #else: lch.SetBinContent(x,y,0)
    grI.SetMarkerStyle(21)
    grI.SetMarkerSize(0.8)
    grI.SetMarkerColor(r.kGray)
    #lch.SetContour(2)
    #lch.SetContourLevel(1,1)
    #lch.SetFillColor(r.kGray)
    #lch.SetFillStyle(4001)
    lch.SetMarkerColor(r.kGray)
    lch.SetMarkerSize(1.2)
    cgraphsDRAW.append(lch.Clone())
    cgraphs.append(lchist.Clone())
    grIs.append(grI)
    cv.Update()
   # clists = r.gROOT.GetListOfSpecials().FindObject("contours")
   # for JJ in range(clists.GetSize()): 
   # 	clists.At(JJ).Print()
   # 	cgraphs.append(clists.At(JJ).Clone())
    # order is lVu,kuu,ldu, -1.6,1.6 0.5,1.5 0.5,1.5
 # print cgraphs
 # for cg in cgraphs: 
 #   cg.SetFillColor(r.kGray)
 #   cg.SetFillStyle(3001)
 #   cg.Draw("fsame")
  for JJ,cg in enumerate(cgraphs): 
    ca = r.TCanvas("ca","",600,600)
    cg.GetXaxis().SetTitle(xt)
    cg.GetYaxis().SetTitle(yt)
    cg.SetTitle(cgraphs[JJ].GetName())
    #cg.SetMinimum(ranges[JJ][0])
    cg.SetMinimum(0.5)
    cg.SetMaximum(ranges[JJ][1])
    ca.SetLogy(logy)
    cg.Draw("colz")
    ca.SaveAs("%s.pdf"%cg.GetName())

  cv.cd()
  h2.Draw("colz")
  h2CL.Draw("cont3same9")
  h2CL2.Draw("cont3same9")
  for JJ,cg in enumerate(grIs): cg.Draw("psame") 
  cv.SetLogy(logy)
  cv.RedrawAxis()
  cv.SaveAs("%s.pdf"%cv.GetName())
  return cv

set_palette()

fi = r.TFile.Open("outplots-2hdm-neg-fine-mssm-final-try2.root")
fo = r.TFile("canvases.root","RECREATE")


gr_type1 = fi.Get("type1")
grs = [fi.Get("lVu"),fi.Get("kuu"),fi.Get("ldu")]
canv_type1 = makeHC(gr_type1,"cos(#beta-#alpha)","tan#beta",grs,1)
fo.WriteTObject(canv_type1)

gr_type2 = fi.Get("type2")
grs = [fi.Get("lVu_2"),fi.Get("kuu_2"),fi.Get("ldu_2")]
canv_type2 = makeHC(gr_type2,"cos(#beta-#alpha)","tan#beta",grs,1)
fo.WriteTObject(canv_type2)


gr_mssm = fi.Get("mssm")
grs = [fi.Get("mssm_lVu"),fi.Get("mssm_kuu"),fi.Get("mssm_ldu")]
canv_mssm = makeHC(gr_mssm,"m_{A} (GeV)","tan#beta",grs,1)
fo.WriteTObject(canv_mssm)



gr_cvcf = fi.Get("cvcf")
grs = [fi.Get("cvcf_lVu"),fi.Get("cvcf_kuu")]
canv_cvcf = makeHC(gr_cvcf,"#kappa_{V}","#kappa_{F}",grs)
fo.WriteTObject(canv_cvcf)



fo.Close()
