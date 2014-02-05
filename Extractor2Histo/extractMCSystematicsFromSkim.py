#!/usr/bin/env python

from __future__ import division
import os, subprocess, tempfile, datetime

d = datetime.datetime.now().strftime("%d%b%y")

files = [
        # Background + Signal
        ["Signal_S0_S_i_M400_cpl1_scalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M400_cpl1_scalar_%s_%s.root"],
        ["Signal_S0_S_i_M500_cpl1_scalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M500_cpl1_scalar_%s_%s.root"],
        ["Signal_S0_S_i_M600_cpl1_scalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M600_cpl1_scalar_%s_%s.root"],
        ["Signal_S0_S_i_M700_cpl1_scalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M700_cpl1_scalar_%s_%s.root"],
        ["Signal_S0_S_i_M800_cpl1_scalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M800_cpl1_scalar_%s_%s.root"],

        ["Signal_S0_S_i_M400_cpl1_pseudoscalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M400_cpl1_pseudoscalar_%s_%s.root"],
        ["Signal_S0_S_i_M500_cpl1_pseudoscalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M500_cpl1_pseudoscalar_%s_%s.root"],
        ["Signal_S0_S_i_M600_cpl1_pseudoscalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M600_cpl1_pseudoscalar_%s_%s.root"],
        ["Signal_S0_S_i_M700_cpl1_pseudoscalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M700_cpl1_pseudoscalar_%s_%s.root"],
        ["Signal_S0_S_i_M800_cpl1_pseudoscalar_histos_%s.root", "skims/Systematics/MTT_S0_S_i_M800_cpl1_pseudoscalar_%s_%s.root"],

        # Signal Z'
        ["Signal_ZPrimeToTTJets_M500GeV_W50GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M500GeV_W50GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M750GeV_W75GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M750GeV_W75GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1000GeV_W100GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1000GeV_W100GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1250GeV_W125GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1250GeV_W125GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1500GeV_W150GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1500GeV_W150GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M2000GeV_W200GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M2000GeV_W200GeV_%s_%s.root"],

        ["Signal_ZPrimeToTTJets_M500GeV_W50GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M500GeV_W50GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M750GeV_W75GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M750GeV_W75GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1000GeV_W100GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1000GeV_W100GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1250GeV_W125GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1250GeV_W125GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1500GeV_W150GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1500GeV_W150GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M2000GeV_W200GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M2000GeV_W200GeV_ext_%s_%s.root"],

        ["Signal_ZPrimeToTTJets_M500GeV_W5GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M500GeV_W5GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M750GeV_W7p5GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M750GeV_W7p5GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1000GeV_W10GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1000GeV_W10GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1250GeV_W12p5GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1250GeV_W12p5GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1500GeV_W15GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1500GeV_W15GeV_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M2000GeV_W20GeV_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M2000GeV_W20GeV_%s_%s.root"],

        ["Signal_ZPrimeToTTJets_M500GeV_W5GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M500GeV_W5GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M750GeV_W7p5GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M750GeV_W7p5GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1000GeV_W10GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1000GeV_W10GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1250GeV_W12p5GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1250GeV_W12p5GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M1500GeV_W15GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M1500GeV_W15GeV_ext_%s_%s.root"],
        ["Signal_ZPrimeToTTJets_M2000GeV_W20GeV_ext_histos_%s.root", "skims/Systematics/MTT_ZPrimeToTTJets_M2000GeV_W20GeV_ext_%s_%s.root"],

        # Background
        ["MC_TT_powheg_histos_%s.root", "skims/Systematics/MTT_TT_powheg_%s_%s.root"],

        ["MC_T_tW-channel_histos_%s.root", "skims/Systematics/MTT_T_tW-channel_%s_%s.root"],
        ["MC_T_s-channel_histos_%s.root", "skims/Systematics/MTT_T_s-channel_%s_%s.root"],
        ["MC_T_t-channel_histos_%s.root", "skims/Systematics/MTT_T_t-channel_%s_%s.root"],

        ["MC_Tbar_tW-channel_histos_%s.root", "skims/Systematics/MTT_Tbar_tW-channel_%s_%s.root"],
        ["MC_Tbar_s-channel_histos_%s.root", "skims/Systematics/MTT_Tbar_s-channel_%s_%s.root"],
        ["MC_Tbar_t-channel_histos_%s.root", "skims/Systematics/MTT_Tbar_t-channel_%s_%s.root"],

        ["MC_DY1JetsToLL_M-50_histos_%s.root", "skims/Systematics/MTT_DY1JetsToLL_M-50_%s_%s.root"],
        ["MC_DY2JetsToLL_M-50_histos_%s.root", "skims/Systematics/MTT_DY2JetsToLL_M-50_%s_%s.root"],
        ["MC_DY3JetsToLL_M-50_histos_%s.root", "skims/Systematics/MTT_DY3JetsToLL_M-50_%s_%s.root"],
        ["MC_DY4JetsToLL_M-50_histos_%s.root", "skims/Systematics/MTT_DY4JetsToLL_M-50_%s_%s.root"],

        ["MC_W1JetsToLNu_histos_%s.root", "skims/Systematics/MTT_W1JetsToLNu_%s_%s.root"],
        ["MC_W2JetsToLNu_histos_%s.root", "skims/Systematics/MTT_W2JetsToLNu_%s_%s.root"],
        ["MC_W3JetsToLNu_histos_%s.root", "skims/Systematics/MTT_W3JetsToLNu_%s_%s.root"],
        ["MC_W4JetsToLNu_histos_%s.root", "skims/Systematics/MTT_W4JetsToLNu_%s_%s.root"],

        ["MC_QCD_Pt_20_30_EMEnriched_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_20_30_EMEnriched_%s_semie.root"],
        ["MC_QCD_Pt_30_80_EMEnriched_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_30_80_EMEnriched_%s_semie.root"],
        ["MC_QCD_Pt_80_170_EMEnriched_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_80_170_EMEnriched_%s_semie.root"],
        ["MC_QCD_Pt_170_250_EMEnriched_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_170_250_EMEnriched_%s_semie.root"],
        ["MC_QCD_Pt_250_350_EMEnriched_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_250_350_EMEnriched_%s_semie.root"],
        ["MC_QCD_Pt_350_EMEnriched_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_350_EMEnriched_%s_semie.root"],

        ["MC_QCD_Pt_30_80_BCtoE_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_30_80_BCtoE_%s_semie.root"],
        ["MC_QCD_Pt_80_170_BCtoE_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_80_170_BCtoE_%s_semie.root"],
        ["MC_QCD_Pt_170_250_BCtoE_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_170_250_BCtoE_%s_semie.root"],
        ["MC_QCD_Pt_250_350_BCtoE_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_250_350_BCtoE_%s_semie.root"],
        ["MC_QCD_Pt_350_BCtoE_histos_%s.root", "skims/Systematics/MTT_QCD_Pt_350_BCtoE_%s_semie.root"],

        ["MC_QCD_pt15to30_bEnriched_MuEnrichedPt14_histos_%s.root", "skims/Systematics/MTT_QCD_pt15to30_bEnriched_MuEnrichedPt14_%s_semimu.root"],
        ["MC_QCD_pt30to50_bEnriched_MuEnrichedPt14_histos_%s.root", "skims/Systematics/MTT_QCD_pt30to50_bEnriched_MuEnrichedPt14_%s_semimu.root"],
        ["MC_QCD_pt50to150_bEnriched_MuEnrichedPt14_histos_%s.root", "skims/Systematics/MTT_QCD_pt50to150_bEnriched_MuEnrichedPt14_%s_semimu.root"],
        ["MC_QCD_pt150_bEnriched_MuEnrichedPt14_histos_%s.root", "skims/Systematics/MTT_QCD_pt150_bEnriched_MuEnrichedPt14_%s_semimu.root"],
        ]

systs = {"JECup": ["JECup", ""], "JECdown": ["JECdown", ""], "JERup": ["JERup", ""], "JERdown": ["JERdown", ""], "puUp": ["nominal", "--pileup-syst up"], "puDown": ["nominal", "--pileup-syst down"]}

if False:
    syst["pdfUp"] = ["nominal", "--pdf-syst up"]
    syst["pdfDown"] = ["nominal", "--pdf-syst down"]

def launch(input, output, btag, extra):
    args = ["./extractorToHisto", "-i", input, "-o", output, "--mc", "--skim", "--b-tag", str(btag)]

    if len(extra) > 0:
        args.append(extra)

    if "semie" in input:
        args.append("--semie")
    elif "semimu" in input:
        args.append("--semimu")

    return " ".join(args)

tmpfile = tempfile.NamedTemporaryFile(dir = '/scratch/', delete = False)

# Build output tree structure
for btag in [1, 2]:
    for type in ["semie", "semimu"]:
        path = "plots/%s/%d-btag/%s/Systematics" % (d, btag, type)
        try:
            os.makedirs(path)
        except:
            pass

print("Extracting datasets...")

for file in files:
    for btag in [1, 2]:
        for type in ["semie", "semimu"]:
            for syst, extra in systs.items():
                if not "%s_%s" in file[1] and not type in file[1]:
                    continue

                path = "plots/%s/%d-btag/%s/Systematics" % (d, btag, type)
                if not "%s_%s" in file[1]:
                    tmpfile.write(launch(file[1] % extra[0], os.path.join(path, file[0] % syst), btag, extra[1]) + "\n");
                else:
                    tmpfile.write(launch(file[1] % (extra[0], type), os.path.join(path, file[0] % syst), btag, extra[1]) + "\n");

tmpfile.flush()

args = ["parallel", "-u", "-a", tmpfile.name, "-j", "30"] 
subprocess.call(args)
