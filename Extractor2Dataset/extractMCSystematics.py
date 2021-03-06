#!/usr/bin/env python

import os, subprocess, tempfile, datetime

d = datetime.datetime.now().strftime("%d%b%y")

files = [
    ##
    ### JEC
    ##

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_JECup.root", "Systematics/JECup/MTT_Zprime_2000_Large_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_JECdown.root", "Systematics/JECdown/MTT_Zprime_2000_Large_full_stat_%s.list"],

    # KK gluons
    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_RSGluon700_JECup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_RSGluon1000_JECup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_RSGluon1200_JECup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_RSGluon1500_JECup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JECup.root",  "Systematics/JECup/MTT_RSGluon2000_JECup_02Mar13_%s.list"],

    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_RSGluon700_JECdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_RSGluon1000_JECdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_RSGluon1200_JECdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_RSGluon1500_JECdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JECdown.root",  "Systematics/JECdown/MTT_RSGluon2000_JECdown_02Mar13_%s.list"],

    ##
    ### JER
    ##

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_JERup.root", "Systematics/JERup/MTT_Zprime_2000_Large_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_JERdown.root", "Systematics/JERdown/MTT_Zprime_2000_Large_full_stat_%s.list"],

    # KK gluons
    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_RSGluon700_JERup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_RSGluon1000_JERup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_RSGluon1200_JERup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_RSGluon1500_JERup_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JERup.root",  "Systematics/JERup/MTT_RSGluon2000_JERup_02Mar13_%s.list"],

    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_RSGluon700_JERdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_RSGluon1000_JERdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_RSGluon1200_JERdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_RSGluon1500_JERdown_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_JERdown.root",  "Systematics/JERdown/MTT_RSGluon2000_JERdown_02Mar13_%s.list"],

    ##
    ### Pile up
    ##

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_puUp.root",  "MC/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_puUp.root",  "MC/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_puUp.root", "MC/MTT_Zprime_2000_Large_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_puDown.root",  "MC/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_puDown.root",  "MC/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_puDown.root", "MC/MTT_Zprime_2000_Large_full_stat_%s.list"],

    # KK gluons
    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_RSGluon700_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_RSGluon1000_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_RSGluon1200_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_RSGluon1500_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_puUp.root",  "MC/MTT_RSGluon2000_02Mar13_%s.list"],

    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_RSGluon700_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_RSGluon1000_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_RSGluon1200_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_RSGluon1500_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_puDown.root",  "MC/MTT_RSGluon2000_02Mar13_%s.list"],

    ##
    ### PDF systematics
    ##

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_Zprime_500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_Zprime_750_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_1000_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_1250_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_1500_Narrow_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_2000_Narrow_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_pdfUp.root",  "MC/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_pdfUp.root",  "MC/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_pdfUp.root", "MC/MTT_Zprime_2000_Large_full_stat_%s.list"],

    ["MTT_Signal_Zprime_500_Large_2012_dataset_%s_pdfDown.root",  "MC/MTT_Zprime_500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_750_Large_2012_dataset_%s_pdfDown.root",  "MC/MTT_Zprime_750_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1000_Large_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_1000_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1250_Large_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_1250_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_1500_Large_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_1500_Large_full_stat_%s.list"],
    ["MTT_Signal_Zprime_2000_Large_2012_dataset_%s_pdfDown.root", "MC/MTT_Zprime_2000_Large_full_stat_%s.list"],

    # KK gluons
    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_RSGluon700_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_RSGluon1000_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_RSGluon1200_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_RSGluon1500_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_pdfUp.root",  "MC/MTT_RSGluon2000_02Mar13_%s.list"],

    #["MTT_Signal_Zprime_750_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_RSGluon700_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1000_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_RSGluon1000_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1250_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_RSGluon1200_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_1500_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_RSGluon1500_02Mar13_%s.list"],
    #["MTT_Signal_Zprime_2000_Narrow_2012_dataset_%s_pdfDown.root",  "MC/MTT_RSGluon2000_02Mar13_%s.list"],
  ]

def launch(input, output):
  args = ["./extractor2Dataset", "--input-list", input, "-o", output, "--mc"]
  if "semie" in input:
    args.append("--type semie")
  elif "semimu" in input:
    args.append("--type semimu")

  if "puUp" in output:
    args.append("--pileup-syst up")
  elif "puDown" in output:
    args.append("--pileup-syst down")

  if "pdfUp" in output:
    args.append("--pdf-syst up")
  elif "pdfDown" in output:
    args.append("--pdf-syst down")

  return " ".join(args)

tmpfile = tempfile.NamedTemporaryFile(dir = '/scratch/', delete = False)

print("Extracting dataset ...")
for file in files:
  for type in ["semie", "semimu"]:
    tmpfile.write(launch(file[1] % type, file[0] % type) + "\n");

tmpfile.flush()

args = ["parallel", "-u", "-a", tmpfile.name, "-j", "6"] 
subprocess.call(args)

# Merge files
for file in files:
  merged_file = file[0].replace("_%s", "_merged_%s" % d)
  args = ["hadd", merged_file, file[0] % "semimu", file[0] % "semie"]
  subprocess.call(args)

for file in files:
  os.remove(file[0] % "semimu")
  os.remove(file[0] % "semie")
