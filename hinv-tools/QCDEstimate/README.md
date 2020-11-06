# QCD Fits 

The code is all inside `mkQCD.py` - this code takes histograms (provided by S. Webb) and produces workspaces containing the method B) QCD estimate. 
It also runs a "closure" check in the A/B regions where the JetHT data is used (lower MET). This closure is not great just yet but will be worked 
on in the future. 

To get the codes, run

`bash <(curl -s https://raw.githubusercontent.com/nucleosynthesis/work-tools/master/hinv-tools/QCDEstimate/sparse-checkout-VBFQCD-ssh.sh)`

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
  * `out_VTR_2017.root_qcdDD_closure_ratio.pdf` - just ignore, not sure why I bothered to include that one (it might be better to make a dedicated study of it)
  * `out_MTR_2017.root_qcdDD_fitTransferForShapeSys.pdf` - A fit (pol1) to the normalised shape of data in region B / data in region A vs mjj. Used to determine shape uncertainties for the QCD template. 
  * `out_MTR_2017.root_mjj_CR.pdf` - The data and non-qcd backgrounds plot in the QCD control region. 
  
When everything looks ok with the fits/plots etc, **you must add the option** `--mkworkspace`, which will finally produce the workspace (inside a file called `out_VTR_2017.root_qcdDD.root`), for combine. You **must make sure** that you are using the same version of CMSSW as combine otherwise the workspace in the end won't work - see here for the reccomended versions : http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#setting-up-the-environment-and-installation 

Note that all of the above plots will also be included in the root file with the workspace inside a folder called `Plots`. 


Note the naming convention is to just use the input file name with extensions, hopefully it is self explanatory 

# JetHT correlation study 

Also included in the QCD estimate is alternative up/down shapes based on possible correlations between mjj and delta phi. To check this, you can also run the script `data_mc_AB_transfer.py` to make plots from the JetHT data and MC QCD simulation from the A and B regions which shows B/A vs mjj. To run, use something like 

`
python data_mc_AB_transfer.py out_MTR_2017.root --ymin -0.2 --ymax 1 --label "MTR 2017"
`

for example in the MTR 2017 category. Change the options for other categories of course.
