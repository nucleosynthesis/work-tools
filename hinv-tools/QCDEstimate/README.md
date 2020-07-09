# QCD Fits 

The code is all inside `mkQCD.py` - this code takes histograms (provided by S. Webb) and produces workspaces containing the method B) QCD estimate. 
It also runs a "closure" check in the A/B regions where the JetHT data is used (lower MET). This closure is not great just yet but will be worked 
on in the future. 

# Example for running the VTR 2017 region 

Below is an example for running the script for the VTR 2017 region, which can be adapted for the other regions

`python mkQCD.py out_VTR_2017.root --function 2 --ymin 0.0001 --ymax 1000  --label "VTR 2017" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.5 --max_blind 2 --mjj_min 900`
where `out_VTR_2017.root` is the file produced from S. Webb. 

You can run with `python mkQCD.py -h` for more explanation on what the options are. 

For running in 2018 of course, just change 2017 to 2018. Instead, for running on MTR, I would suggest the following options 

   * ` --sr_cut 0.5`
   * `--label "MTR 2017"` or `--label "MTR 2018"`
   * `--fit_min 0 --fit_max 1 `
   * `--max_blind 1.2` (although we can probably remove that one now)

**NOTE** - For the MTR regions, the current version of the analysis uses the option `--function 1`, but it could be good to check the difference this gives to `--function 2` which I think is better motivated. 

# Outputs 

The code (following the above) will output the following 

  * `out_VTR_2017.root_qcdDD_normfit.pdf` - this shows the fit in the mindphi variable, it also has the uncertainty from the fit shown on the QCD Normalisation
  * `out_VTR_2017.root_qcdDD.pdf` - this has the final QCD estimate along with its uncertainty band plotted - it will also plot the QCD MC and the method A result (from S. Webb's file)
  * `out_VTR_2017.root_qcdDD_fakefit.pdf` - this shows the fit in the mindphi variable for the A+B region (low met), which is for the closure. 
  * `out_VTR_2017.root_qcdDD_closureAB.pdf` - this shows the result of the fit to the AB region, and compares with Data-bkg in the Region B 
  * `out_VTR_2017.root_qcdEstimate_toys.pdf` - You can mostly ignore this one, except that in the top left, you see a Result like `N = XXX(1+YY)^theta` - the number `1+YY` is what should go in the datacard as the uncertainty on the normalisation from the fit
  * `out_VTR_2017.root_qcdDD_closure_ratio.pdf` - just ignore, not sure why I bothered to include that one

When everything looks ok with the fits/plots etc, **you must add the option** `--mkworkspace`, which will finally produce the workspace (inside a file called `out_VTR_2017.root_qcdDD.root`), for combine. You **must make sure** that you are using the same version of CMSSW as combine otherwise the workspace in the end won't work - see here for the reccomended versions : http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#setting-up-the-environment-and-installation 


Note the naming convention is to just use the input file name with extensions, hopefully it is self explanatory 
