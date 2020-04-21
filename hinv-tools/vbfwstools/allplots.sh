#!/bin/bash 


python plotTFExperimental.py "MTR_" Zmumu Zee ZMUMU ZEE "Z#rightarrow #mu#mu / Z#rightarrow ee" 0 3  TF_MTR_double_lepton "41.5 fb^{-1} / 59.8 fb^{-1} (13 TeV, 2017/2018)" "MTR"
python plotTFExperimental.py "MTR_" Wmunu Wenu WMUNU WENU "W#rightarrow #mu#nu / W#rightarrow e#nu" 0 3  TF_MTR_single_lepton "41.5 fb^{-1} / 59.8 fb^{-1} (13 TeV, 2017/2018)" "MTR"

python plotTFExperimental.py "VTR_" Zmumu Zee ZMUMU ZEE "Z#rightarrow #mu#mu / Z#rightarrow ee" 0 5  TF_VTR_double_lepton "41.5 fb^{-1} / 59.8 fb^{-1} (13 TeV, 2017/2018)" "VTR"
python plotTFExperimental.py "VTR_" Wmunu Wenu WMUNU WENU "W#rightarrow #mu#nu / W#rightarrow e#nu" 0 5  TF_VTR_single_lepton "41.5 fb^{-1} / 59.8 fb^{-1} (13 TeV, 2017/2018)" "VTR"

python plotTFTheories.py "MTR_2017_" mumu munu MUMU MUNU "Z#rightarrow #mu#mu / W#rightarrow #mu#nu" 0 0.2  TF_MTR_2017_muons "41.5 fb^{-1} (13 TeV, 2017)" "MTR"
python plotTFTheories.py "MTR_2017_" ee enu EE ENU       "Z#rightarrow ee / W#rightarrow e#nu" 0 0.3  TF_MTR_2017_electrons   "41.5 fb^{-1} (13 TeV, 2017)" "MTR"

python plotTFTheories.py "MTR_2018_" mumu munu MUMU MUNU "Z#rightarrow #mu#mu / W#rightarrow #mu#nu" 0 0.3  TF_MTR_2018_muons "59.8 fb^{-1} (13 TeV, 2018)" "MTR"
python plotTFTheories.py "MTR_2018_" ee enu EE ENU       "Z#rightarrow ee / W#rightarrow e#nu" 0 0.3  TF_MTR_2018_electrons   "59.8 fb^{-1} (13 TeV, 2018)" "MTR"

python plotTFTheories.py "VTR_2017_" mumu munu MUMU MUNU "Z#rightarrow #mu#mu / W#rightarrow #mu#nu" 0 0.4  TF_VTR_2017_muons "41.5 fb^{-1} (13 TeV, 2017)" "VTR"
python plotTFTheories.py "VTR_2017_" ee enu EE ENU       "Z#rightarrow ee / W#rightarrow e#nu" 0 0.4  TF_VTR_2017_electrons   "41.5 fb^{-1} (13 TeV, 2017)" "VTR"

python plotTFTheories.py "VTR_2018_" mumu munu MUMU MUNU "Z#rightarrow #mu#mu / W#rightarrow #mu#nu" 0 0.4  TF_VTR_2018_muons "59.8 fb^{-1} (13 TeV, 2018)" "VTR"
python plotTFTheories.py "VTR_2018_" ee enu EE ENU       "Z#rightarrow ee / W#rightarrow e#nu" 0 0.8  TF_VTR_2018_electrons   "59.8 fb^{-1} (13 TeV, 2018)" "VTR"

