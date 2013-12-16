#!/usr/bin/env python

from __future__ import division
import os, subprocess, tempfile, datetime

d = datetime.datetime.now().strftime("%d%b%y")

files = [
        # Background + Signal
        #["Signal_S0_S_i_M500_cpl1_scalar_skims_nominal.root", "lists/MTT_S0_S_i_M500_cpl1_scalar_%s.list"],
        #["Signal_S0_S_i_M700_cpl1_scalar_skims_nominal.root", "lists/MTT_S0_S_i_M700_cpl1_scalar_%s.list"],
        #["Signal_S0_S_i_M500_cpl1_pseudoscalar_skims_nominal.root", "lists/MTT_S0_S_i_M500_cpl1_pseudoscalar_%s.list"],
        #["Signal_S0_S_i_M700_cpl1_pseudoscalar_skims_nominal.root", "lists/MTT_S0_S_i_M700_cpl1_pseudoscalar_%s.list"],

        # Background
        #["MC_TT_powheg_skims_nominal.root", "lists/MTT_TT_powheg_%s.list"],

        #["MC_T_tW-channel_skims_nominal.root", "lists/MTT_T_tW-channel_%s.list"],
        #["MC_T_s-channel_skims_nominal.root", "lists/MTT_T_s-channel_%s.list"],
        #["MC_T_t-channel_skims_nominal.root", "lists/MTT_T_t-channel_%s.list"],

        #["MC_Tbar_tW-channel_skims_nominal.root", "lists/MTT_Tbar_tW-channel_%s.list"],
        #["MC_Tbar_s-channel_skims_nominal.root", "lists/MTT_Tbar_s-channel_%s.list"],
        #["MC_Tbar_t-channel_skims_nominal.root", "lists/MTT_Tbar_t-channel_%s.list"],

        #["MC_DY1JetsToLL_M-50_skims_nominal.root", "lists/MTT_DY1JetsToLL_M-50_%s.list"],
        #["MC_DY2JetsToLL_M-50_skims_nominal.root", "lists/MTT_DY2JetsToLL_M-50_%s.list"],
        #["MC_DY3JetsToLL_M-50_skims_nominal.root", "lists/MTT_DY3JetsToLL_M-50_%s.list"],
        #["MC_DY4JetsToLL_M-50_skims_nominal.root", "lists/MTT_DY4JetsToLL_M-50_%s.list"],

        #["MC_W1JetsToLNu_skims_nominal.root", "lists/MTT_W1JetsToLNu_%s.list"],
        #["MC_W2JetsToLNu_skims_nominal.root", "lists/MTT_W2JetsToLNu_%s.list"],
        #["MC_W3JetsToLNu_skims_nominal.root", "lists/MTT_W3JetsToLNu_%s.list"],
        #["MC_W4JetsToLNu_skims_nominal.root", "lists/MTT_W4JetsToLNu_%s.list"],

        ["MC_QCD_Pt_20_30_EMEnriched_skims_nominal.root", "lists/MTT_QCD_Pt_20_30_EMEnriched_semie.list"],
        ["MC_QCD_Pt_30_80_EMEnriched_skims_nominal.root", "lists/MTT_QCD_Pt_30_80_EMEnriched_semie.list"],
        ["MC_QCD_Pt_80_170_EMEnriched_skims_nominal.root", "lists/MTT_QCD_Pt_80_170_EMEnriched_semie.list"],
        ["MC_QCD_Pt_170_250_EMEnriched_skims_nominal.root", "lists/MTT_QCD_Pt_170_250_EMEnriched_semie.list"],
        ["MC_QCD_Pt_250_350_EMEnriched_skims_nominal.root", "lists/MTT_QCD_Pt_250_350_EMEnriched_semie.list"],
        ["MC_QCD_Pt_350_EMEnriched_skims_nominal.root", "lists/MTT_QCD_Pt_350_EMEnriched_semie.list"],

        ["MC_QCD_pt15to30_bEnriched_MuEnrichedPt14_skims_nominal.root", "lists/MTT_QCD_pt15to30_bEnriched_MuEnrichedPt14_semimu.list"],
        ["MC_QCD_pt30to50_bEnriched_MuEnrichedPt14_skims_nominal.root", "lists/MTT_QCD_pt30to50_bEnriched_MuEnrichedPt14_semimu.list"],
        ["MC_QCD_pt50to150_bEnriched_MuEnrichedPt14_skims_nominal.root", "lists/MTT_QCD_pt50to150_bEnriched_MuEnrichedPt14_semimu.list"],
        ["MC_QCD_pt150_bEnriched_MuEnrichedPt14_skims_nominal.root", "lists/MTT_QCD_pt150_bEnriched_MuEnrichedPt14_semimu.list"],
        ]

def launch(input, output):
    args = ["./preSkim", "--input-list", input, "-o", output, "--mc"]
    if "semie" in input:
        args.append("--semie")
    elif "semimu" in input:
        args.append("--semimu")

    #args.append("--weight %.15f" % weight)

    return " ".join(args)

tmpfile = tempfile.NamedTemporaryFile(dir = '/scratch/', delete = False)

# Build output tree structure
for type in ["semie", "semimu"]:
    path = "skims/%s/%s" % (d, type)
    try:
        os.makedirs(path)
    except:
        pass

print("Skimming datasets...")

for file in files:
    for type in ["semie", "semimu"]:
        path = "skims/%s/%s" % (d, type)
        if "Enriched" in file[1]:
            if ("MuEnriched" in file[1] and type == "semimu") or ("EMEnriched" in file[1] and type == "semie"):
                tmpfile.write(launch(file[1], os.path.join(path, file[0])) + "\n");
        else:
            tmpfile.write(launch(file[1] % type, os.path.join(path, file[0])) + "\n");

tmpfile.flush()

args = ["parallel", "-u", "-a", tmpfile.name, "-j", "28"] 
subprocess.call(args)
