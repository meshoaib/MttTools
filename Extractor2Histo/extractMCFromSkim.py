#!/usr/bin/env python

from __future__ import division
import os, subprocess, tempfile, datetime

d = datetime.datetime.now().strftime("%d%b%y")

files = [
        # Background
        ["MC_TT_powheg_histos_nominal.root", "skims/%s/MC_TT_powheg_skims_nominal.root"],

        ["MC_T_tW-channel_histos_nominal.root", "skims/%s/MC_T_tW-channel_skims_nominal.root"],
        ["MC_T_s-channel_histos_nominal.root", "skims/%s/MC_T_s-channel_skims_nominal.root"],
        ["MC_T_t-channel_histos_nominal.root", "skims/%s/MC_T_t-channel_skims_nominal.root"],

        ["MC_Tbar_tW-channel_histos_nominal.root", "skims/%s/MC_Tbar_tW-channel_skims_nominal.root"],
        ["MC_Tbar_s-channel_histos_nominal.root", "skims/%s/MC_Tbar_s-channel_skims_nominal.root"],
        ["MC_Tbar_t-channel_histos_nominal.root", "skims/%s/MC_Tbar_t-channel_skims_nominal.root"],

        ["MC_DY1JetsToLL_M-50_histos_nominal.root", "skims/%s/MC_DY1JetsToLL_M-50_skims_nominal.root"],
        ["MC_DY2JetsToLL_M-50_histos_nominal.root", "skims/%s/MC_DY2JetsToLL_M-50_skims_nominal.root"],
        ["MC_DY3JetsToLL_M-50_histos_nominal.root", "skims/%s/MC_DY3JetsToLL_M-50_skims_nominal.root"],
        ["MC_DY4JetsToLL_M-50_histos_nominal.root", "skims/%s/MC_DY4JetsToLL_M-50_skims_nominal.root"],

        ["MC_W1JetsToLNu_histos_nominal.root", "skims/%s/MC_W1JetsToLNu_skims_nominal.root"],
        ["MC_W2JetsToLNu_histos_nominal.root", "skims/%s/MC_W2JetsToLNu_skims_nominal.root"],
        ["MC_W3JetsToLNu_histos_nominal.root", "skims/%s/MC_W3JetsToLNu_skims_nominal.root"],
        ["MC_W4JetsToLNu_histos_nominal.root", "skims/%s/MC_W4JetsToLNu_skims_nominal.root"],

        # QCD
        ["MC_QCD_pt15to30_bEnriched_MuEnrichedPt14_histos_nominal.root", "skims/semimu/MC_QCD_pt15to30_bEnriched_MuEnrichedPt14_skims_nominal.root"],
        ["MC_QCD_pt30to50_bEnriched_MuEnrichedPt14_histos_nominal.root", "skims/semimu/MC_QCD_pt30to50_bEnriched_MuEnrichedPt14_skims_nominal.root"],
        ["MC_QCD_pt50to150_bEnriched_MuEnrichedPt14_histos_nominal.root", "skims/semimu/MC_QCD_pt50to150_bEnriched_MuEnrichedPt14_skims_nominal.root"],
        ["MC_QCD_pt150_bEnriched_MuEnrichedPt14_histos_nominal.root", "skims/semimu/MC_QCD_pt150_bEnriched_MuEnrichedPt14_skims_nominal.root"],

        ["MC_QCD_Pt_20_30_EMEnriched_histos_nominal.root", "skims/semie/MC_QCD_Pt_20_30_EMEnriched_skims_nominal.root"],
        ["MC_QCD_Pt_30_80_EMEnriched_histos_nominal.root", "skims/semie/MC_QCD_Pt_30_80_EMEnriched_skims_nominal.root"],
        ["MC_QCD_Pt_80_170_EMEnriched_histos_nominal.root", "skims/semie/MC_QCD_Pt_80_170_EMEnriched_skims_nominal.root"],
        ["MC_QCD_Pt_170_250_EMEnriched_histos_nominal.root", "skims/semie/MC_QCD_Pt_170_250_EMEnriched_skims_nominal.root"],
        ["MC_QCD_Pt_250_350_EMEnriched_histos_nominal.root", "skims/semie/MC_QCD_Pt_250_350_EMEnriched_skims_nominal.root"],
        ["MC_QCD_Pt_350_EMEnriched_histos_nominal.root", "skims/semie/MC_QCD_Pt_350_EMEnriched_skims_nominal.root"],

        ["MC_QCD_Pt_30_80_BCtoE_histos_nominal.root", "skims/semie/MC_QCD_Pt_30_80_BCtoE_skims_nominal.root"],
        ["MC_QCD_Pt_80_170_BCtoE_histos_nominal.root", "skims/semie/MC_QCD_Pt_80_170_BCtoE_skims_nominal.root"],
        ["MC_QCD_Pt_170_250_BCtoE_histos_nominal.root", "skims/semie/MC_QCD_Pt_170_250_BCtoE_skims_nominal.root"],
        ["MC_QCD_Pt_250_350_BCtoE_histos_nominal.root", "skims/semie/MC_QCD_Pt_250_350_BCtoE_skims_nominal.root"],
        ["MC_QCD_Pt_350_BCtoE_histos_nominal.root", "skims/semie/MC_QCD_Pt_350_BCtoE_skims_nominal.root"],

        # Background + Signal
        ["Signal_S0_S_i_M400_cpl1_scalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M400_cpl1_scalar_skims_nominal.root"],
        ["Signal_S0_S_i_M500_cpl1_scalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M500_cpl1_scalar_skims_nominal.root"],
        ["Signal_S0_S_i_M600_cpl1_scalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M600_cpl1_scalar_skims_nominal.root"],
        ["Signal_S0_S_i_M700_cpl1_scalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M700_cpl1_scalar_skims_nominal.root"],
        ["Signal_S0_S_i_M800_cpl1_scalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M800_cpl1_scalar_skims_nominal.root"],

        ["Signal_S0_S_i_M400_cpl1_pseudoscalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M400_cpl1_pseudoscalar_skims_nominal.root"],
        ["Signal_S0_S_i_M500_cpl1_pseudoscalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M500_cpl1_pseudoscalar_skims_nominal.root"],
        ["Signal_S0_S_i_M600_cpl1_pseudoscalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M600_cpl1_pseudoscalar_skims_nominal.root"],
        ["Signal_S0_S_i_M700_cpl1_pseudoscalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M700_cpl1_pseudoscalar_skims_nominal.root"],
        ["Signal_S0_S_i_M800_cpl1_pseudoscalar_histos_nominal.root", "skims/%s/Signal_S0_S_i_M800_cpl1_pseudoscalar_skims_nominal.root"],

        ["Signal_ZPrimeToTTJets_M500GeV_W5GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M500GeV_W5GeV_merged_skims_nominal.root"],
	["Signal_ZPrimeToTTJets_M750GeV_W7p5GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M750GeV_W7p5GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M1000GeV_W10GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M1000GeV_W10GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M1250GeV_W12p5GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M1250GeV_W12p5GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M1500GeV_W15GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M1500GeV_W15GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M2000GeV_W20GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M2000GeV_W20GeV_merged_skims_nominal.root"],
	
	["Signal_ZPrimeToTTJets_M500GeV_W50GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M500GeV_W50GeV_merged_skims_nominal.root"],
	["Signal_ZPrimeToTTJets_M750GeV_W75GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M750GeV_W75GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M1000GeV_W100GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M1000GeV_W100GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M1250GeV_W125GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M1250GeV_W125GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M1500GeV_W150GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M1500GeV_W150GeV_merged_skims_nominal.root"],
        ["Signal_ZPrimeToTTJets_M2000GeV_W200GeV_histos_nominal.root", "skims/%s/Signal_ZPrimeToTTJets_M2000GeV_W200GeV_merged_skims_nominal.root"],
        ]

def launch(input, output, btag):
    args = ["./extractorToHisto", "-i", input, "-o", output, "--mc", "--skim", "--b-tag", str(btag)]
    if "semie" in input:
        args.append("--semie")
    elif "semimu" in input:
        args.append("--semimu")

    return " ".join(args)

tmpfile = tempfile.NamedTemporaryFile(dir = '/scratch/', delete = False)

# Build output tree structure
for btag in [1, 2]:
    for type in ["semie", "semimu"]:
        path = "plots/%s/%d-btag/%s" % (d, btag, type)
        try:
            os.makedirs(path)
        except:
            pass

print("Extracting datasets...")

for file in files:
    for btag in [1, 2]:
    #for btag in [2]:
        #for type in ["semie", "semimu"]:
        for type in ["semie", "semimu"]:
            if not "%" in file[1] and not type in file[1]:
                continue
            path = "plots/%s/%d-btag/%s" % (d, btag, type)
            if not "%" in file[1]:
                tmpfile.write(launch(file[1], "%s/%s" % (path, file[0]), btag) + "\n");
            else:
                tmpfile.write(launch(file[1] % type, "%s/%s" % (path, file[0]), btag) + "\n");

tmpfile.flush()

print tmpfile.name
args = ["parallel", "-u", "-a", tmpfile.name, "-j", "4"] 
subprocess.call(args)
