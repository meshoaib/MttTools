#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

#include <json/json.h>
#include <tclap/CmdLine.h>

#include <TString.h>

#include "Utils.h"

#include <TGraphErrors.h>
#include <TMultiGraph.h>
#include <TF1.h>
#include <TCanvas.h>

std::string base_path = "";

void loadSelection(const std::string& jecType, int btag, const int (&masses)[6], float (&nSelectionMu)[6], float (&errNSelectionMu)[6], float (&nSelectionE)[6], float (&errNSelectionE)[6]) {

  Json::Reader reader;
  Json::Value root;
  std::ifstream file((base_path + "/frit_efficiencies.json").c_str());
  bool success = reader.parse(file, root);
  file.close();

  if (! success) {
    std::cerr << "ERROR: Can't parse " << "frit_efficiencies.json" << ". Exiting" << std::endl;
    exit(1);
  }

  root = root[getAnalysisUUID()];

  for (int i = 0; i < 5; i++) {
    const int& mass = masses[i];

    std::stringstream ss;
    ss << mass;
    std::string strMass = ss.str();

    ss.clear(); ss.str(std::string());
    ss << btag;
    std::string btagStr = ss.str();

    if (! root.isMember(strMass)) {
      std::cerr << "ERROR: mass '" << mass << "' not found in JSON file. Exiting." << std::endl;
      exit(1);
    }

    Json::Value massNode = root[strMass][btagStr];

    if (! massNode.isMember(jecType)) {
      std::cerr << "ERROR: '" << jecType << "' not found for m=" << mass << " in JSON file. Setting to 0." << std::endl;
      
      nSelectionMu[i] = 0;
      errNSelectionMu[i] = 0;
      nSelectionE[i] = 0;
      errNSelectionE[i] = 0;

      continue;
    }

    Json::Value jecNode = massNode[jecType];

    nSelectionMu[i] = jecNode["muon"]["events"].asDouble();
    errNSelectionMu[i] = jecNode["muon"]["error"].asDouble();

    nSelectionE[i] = jecNode["electron"]["events"].asDouble();
    errNSelectionE[i] = jecNode["electron"]["error"].asDouble();
  }
}

class Efficiencies {
  public: 
    bool   isInterpolated;
    int    mass;

    float effTrig_mu;
    float effTrig_e;
    float error_effTrig_mu;
    float error_effTrig_e;

    float selectionEff_mu;
    float selectionEff_e;
    float error_selectionEff_mu;
    float error_selectionEff_e;

    void copy(const Efficiencies& from) {
      effTrig_mu = from.effTrig_mu;
      effTrig_e  = from.effTrig_e;
      error_effTrig_mu = from.error_effTrig_mu;
      error_effTrig_e  = from.error_effTrig_e;

      selectionEff_mu  = from.selectionEff_mu;
      selectionEff_e   = from.selectionEff_e;
      error_selectionEff_mu = from.error_selectionEff_mu;
      error_selectionEff_e  = from.error_selectionEff_e;
    }

    Efficiencies(int m) {
      effTrig_mu = 1.; effTrig_e = 1.;
      selectionEff_mu = 0; selectionEff_e = 0;

      mass = m;
      isInterpolated = (mass != 500 && mass != 750 && mass != 1000 && mass != 1250 && mass != 1500 && mass != 2000);
    }

    Efficiencies() {

    }

    Efficiencies(const Efficiencies& from) {
      operator=(from);
    }

    Efficiencies& operator=(const Efficiencies& from) {
      isInterpolated = from.isInterpolated;
      mass = from.mass;

      copy(from);

      return *this;
    }

    Json::Value getAsJSON() {
      
      Json::Value array(Json::arrayValue);
      array.append(selectionEff_mu);
      array.append(selectionEff_e);
      array.append(effTrig_mu);
      array.append(effTrig_e);
      array.append(error_selectionEff_mu / selectionEff_mu);
      array.append(error_selectionEff_e / selectionEff_e);
      array.append(error_effTrig_mu / effTrig_mu);
      array.append(error_effTrig_e / effTrig_e);

      return array;
    }

    friend std::ostream& operator<<(std::ostream& stream, const Efficiencies& eff);
};

std::ostream& operator<<(std::ostream& stream, const Efficiencies& eff) {
  stream << "M_Z' = " << eff.mass<< std::endl;
  stream << "Selection efficiency: "
    << '\t' << "muon = " << eff.selectionEff_mu << " +/- " << eff.error_selectionEff_mu 
    << '\t' << "electron = " << eff.selectionEff_e << " +/- " << eff.error_selectionEff_e;
  stream << std::endl;
  stream << "Trigger efficiency: "
    << '\t' << "muon = " << eff.effTrig_mu << " +/- " << eff.error_effTrig_mu 
    << '\t' << "electron = " << eff.effTrig_e << " +/- " << eff.error_effTrig_e;

  return stream;
}

int main(int argc, char** argv) {

  try {
    TCLAP::CmdLine cmd("Compute efficiencies", ' ', "0.1");

    TCLAP::ValueArg<int> btagArg("", "b-tag", "Number of b-tagged jets", false, 2, "int", cmd);
    TCLAP::ValueArg<std::string> jecArg("", "jec", "Type of JEC", false, "nominal", "nominal/JECup/JECdown", cmd);

    // TCLAP::SwitchArg ignoreInterpolatedArg("", "ignore-interpolated", "Ignore interpolated mass for extrapolation", cmd, false);

    cmd.parse(argc, argv);

    int btag = btagArg.getValue();
    std::string jec = jecArg.getValue();

    std::stringstream stream;
    stream << btag;

    std::string btagStr = stream.str();

    base_path = "./analysis/" + getAnalysisUUID();
    bool ignoreInterpolated = !analysisUseInterpolation();

    std::map<int, Efficiencies> efficiencies;
    for (int i = 500; i <= 2000; i += 125) {
      efficiencies[i] = Efficiencies(i);
    }

    const int M[] = {500, 750, 1000, 1250, 1500, 2000};

    // HLT efficiencies
    // See https://docs.google.com/spreadsheet/ccc?key=0AsI4zLOlSqcUdHhiYmFKbDIxY3YwWlJHdE9NSVhMSnc
    // and https://docs.google.com/spreadsheet/ccc?key=0AsI4zLOlSqcUdEkySy11MFlYczNRcE9BNTZvTjRFMWc
    // for details about effiencies

    TGraphErrors trig_e;
    TGraphErrors trig_e_low;
    TGraphErrors trig_e_high;

    TGraphErrors trig_mu;
    TGraphErrors trig_mu_low;
    TGraphErrors trig_mu_high;

    int index = 0;

    for (auto& i: efficiencies) {

      if (i.second.isInterpolated)
        continue;

      if (btag == 1) {
        switch (i.first) {
          case 750:

            i.second.effTrig_mu = 0.915122446654598;
            i.second.effTrig_e = 0.96969953545322;
            i.second.error_effTrig_mu = 0.004642381230494;
            i.second.error_effTrig_e = 0.002879505024457;
            break;
          case 1000:

            i.second.effTrig_mu = 0.918923622827662;
            i.second.effTrig_e = 0.95921905206221;
            i.second.error_effTrig_mu = 0.004375487331033;
            i.second.error_effTrig_e = 0.003205576076252;
            break;
          case 1250:

            i.second.effTrig_mu = 0.912991926623528;
            i.second.effTrig_e = 0.96208121973835;
            i.second.error_effTrig_mu = 0.004608858750741;
            i.second.error_effTrig_e = 0.003105605567111;
            break;
          case 1500:

            i.second.effTrig_mu = 0.921745651170932;
            i.second.effTrig_e = 0.95439771390689;
            i.second.error_effTrig_mu = 0.004688169399042;
            i.second.error_effTrig_e = 0.003656738673623;
            break;
        }

      } else if (btag == 2) {
        switch (i.first) {
          case 750:

            i.second.effTrig_mu = 0.917163304486474;
            i.second.effTrig_e = 0.962889078839;
            i.second.error_effTrig_mu = 0.004446650436803;
            i.second.error_effTrig_e = 0.003200162475621;
            break;
          case 1000:

            i.second.effTrig_mu = 0.920284402024634;
            i.second.effTrig_e = 0.97122799548137;
            i.second.error_effTrig_mu = 0.004263819222257;
            i.second.error_effTrig_e = 0.002739894204469;
            break;
          case 1250:

            i.second.effTrig_mu = 0.906055190143938;
            i.second.effTrig_e = 0.96165533977795;
            i.second.error_effTrig_mu = 0.004919248449977;
            i.second.error_effTrig_e = 0.003277588820738;
            break;
          case 1500:

            i.second.effTrig_mu = 0.920540646888956;
            i.second.effTrig_e = 0.95867889687774;
            i.second.error_effTrig_mu = 0.005035374383869;
            i.second.error_effTrig_e = 0.003762430369621;
            break;
        }
      }

      if (! ignoreInterpolated && i.first != 500 && i.first != 2000) {
        trig_mu.SetPoint(index, i.first, i.second.effTrig_mu);
        trig_mu.SetPointError(index, 0., i.second.error_effTrig_mu);

        trig_mu_low.SetPoint(index, i.first, i.second.effTrig_mu - i.second.error_effTrig_mu);
        trig_mu_low.SetPointError(index, 0., i.second.error_effTrig_mu); // Needed for fit
        trig_mu_high.SetPoint(index, i.first, i.second.effTrig_mu + i.second.error_effTrig_mu);
        trig_mu_high.SetPointError(index, 0., i.second.error_effTrig_mu); // Needed for fit

        trig_e.SetPoint(index, i.first, i.second.effTrig_e);
        trig_e.SetPointError(index, 0., i.second.error_effTrig_e);

        trig_e_low.SetPoint(index, i.first, i.second.effTrig_e - i.second.error_effTrig_e);
        trig_e_low.SetPointError(index, 0., i.second.error_effTrig_e); // Needed for fit
        trig_e_high.SetPoint(index, i.first, i.second.effTrig_e + i.second.error_effTrig_e);
        trig_e_high.SetPointError(index++, 0., i.second.error_effTrig_e); // Needed for fit
      }
    }

    TF1 triggerEff_fit_mu("sel_eff_fit_mu", "pol1", 500, 2000);
    TF1* triggerEff_fit_mu_low = (TF1*) triggerEff_fit_mu.Clone("triggerEff_fit_mu_low");
    TF1* triggerEff_fit_mu_high = (TF1*) triggerEff_fit_mu.Clone("triggerEff_fit_mu_high");

    TF1 triggerEff_fit_e("sel_eff_fit_e", "pol1", 500, 2000);
    TF1* triggerEff_fit_e_low = (TF1*) triggerEff_fit_e.Clone("triggerEff_fit_e_low");
    TF1* triggerEff_fit_e_high = (TF1*) triggerEff_fit_e.Clone("triggerEff_fit_e_high");

    if (! ignoreInterpolated) {
      trig_mu.Fit(&triggerEff_fit_mu, "QMR");
      trig_mu_low.Fit(triggerEff_fit_mu_low, "QMR");
      trig_mu_high.Fit(triggerEff_fit_mu_high, "QMR");

      trig_e.Fit(&triggerEff_fit_e, "QR");
      trig_e_low.Fit(triggerEff_fit_e_low, "QR");
      trig_e_high.Fit(triggerEff_fit_e_high, "QR");
    }

    TCanvas c("c", "c", 800, 800);
    
    {
      TMultiGraph *mg = new TMultiGraph();

      mg->Add(&trig_e, "lp");
      mg->Add(&trig_e_low, "lp");
      mg->Add(&trig_e_high, "lp");

      mg->Draw("a");

      c.Print("interpolation_trigger_eff.root");

      delete mg;
    }

    //--- selection efficiencies
    const float N0[] = {
      237512,
      216768,
      205479,
      195664,
      197349,
      186658
    };

    float Nsel_mu[6];
    float ErrNsel_mu[6];
    float Nsel_e[6];
    float ErrNsel_e[6];
    loadSelection(jec, btag, M, Nsel_mu, ErrNsel_mu, Nsel_e, ErrNsel_e);

    TGraphErrors e_mu;
    TGraphErrors e_mu_low;
    TGraphErrors e_mu_high;

    TGraphErrors e_e;
    TGraphErrors e_e_low;
    TGraphErrors e_e_high;

    TF1 selectionEff_fit_mu("sel_eff_fit_mu", "pol3", 500, 2000);
    TF1* selectionEff_fit_mu_low = (TF1*) selectionEff_fit_mu.Clone("sel_eff_fit_mu_low");
    TF1* selectionEff_fit_mu_high = (TF1*) selectionEff_fit_mu.Clone("sel_eff_fit_mu_high");

    TF1 selectionEff_fit_e("sel_eff_fit_e", "pol3", 500, 2000);
    TF1* selectionEff_fit_e_low = (TF1*) selectionEff_fit_e.Clone("sel_eff_fit_e_low");
    TF1* selectionEff_fit_e_high = (TF1*) selectionEff_fit_e.Clone("sel_eff_fit_e_high");

    index = 0;
    Efficiencies* lowMass_eff = nullptr;
    for (auto& i: efficiencies) {
      Efficiencies& eff = i.second;

      if (! i.second.isInterpolated) {
        lowMass_eff = &eff;

        eff.selectionEff_mu = Nsel_mu[index] / N0[index];
        eff.selectionEff_e  = Nsel_e[index] / N0[index];
        eff.error_selectionEff_mu = ErrNsel_mu[index] / N0[index];
        eff.error_selectionEff_e = ErrNsel_e[index] / N0[index];

        if (! ignoreInterpolated) {
          e_mu.SetPoint(index, i.first, i.second.selectionEff_mu);
          e_mu.SetPointError(index, 0, i.second.error_selectionEff_mu);

          e_mu_low.SetPoint(index, i.first, i.second.selectionEff_mu - i.second.error_selectionEff_mu);
          e_mu_high.SetPoint(index, i.first, i.second.selectionEff_mu + i.second.error_selectionEff_mu);

          e_e.SetPoint(index, i.first, i.second.selectionEff_e);
          e_e.SetPointError(index, 0, i.second.error_selectionEff_e);

          e_e_low.SetPoint(index, i.first, i.second.selectionEff_e - i.second.error_selectionEff_e);
          e_e_high.SetPoint(index, i.first, i.second.selectionEff_e + i.second.error_selectionEff_e);
        }

        index++;
      } else if (ignoreInterpolated) {
        eff.copy(*lowMass_eff);
      }
    }

    if (! ignoreInterpolated) {
      e_mu.Fit(&selectionEff_fit_mu, "QR");
      e_mu_low.Fit(selectionEff_fit_mu_low, "QR");
      e_mu_high.Fit(selectionEff_fit_mu_high, "QR");

      e_e.Fit(&selectionEff_fit_e, "QR");
      e_e_low.Fit(selectionEff_fit_e_low, "QR");
      e_e_high.Fit(selectionEff_fit_e_high, "QR");
    }

    {
      TMultiGraph *mg = new TMultiGraph();

      mg->Add(&e_mu, "lp");
      mg->Add(&e_mu_low, "lp");
      mg->Add(&e_mu_high, "lp");

      mg->Draw("a");

      c.Print("interpolation_selection_eff.root");

      delete mg;
    }

    if (! ignoreInterpolated) {
      for (auto& i: efficiencies) {
        Efficiencies& eff = i.second;

        if (i.second.isInterpolated) {
          eff.selectionEff_mu = selectionEff_fit_mu.Eval(i.first);
          eff.selectionEff_e  = selectionEff_fit_e.Eval(i.first);

          eff.error_selectionEff_mu = fabs(selectionEff_fit_mu_high->Eval(i.first) - selectionEff_fit_mu_low->Eval(i.first)) / 2.;
          eff.error_selectionEff_e = fabs(selectionEff_fit_e_high->Eval(i.first) - selectionEff_fit_e_low->Eval(i.first)) / 2.; 
        }

        if (i.second.isInterpolated || i.first == 500 || i.first == 2000) {

          eff.effTrig_mu = triggerEff_fit_mu.Eval(i.first);
          eff.effTrig_e = triggerEff_fit_e.Eval(i.first);

          eff.error_effTrig_mu = fabs(triggerEff_fit_mu_high->Eval(i.first) - triggerEff_fit_mu_low->Eval(i.first)) / 2.;
          eff.error_effTrig_e = fabs(triggerEff_fit_e_high->Eval(i.first) - triggerEff_fit_e_low->Eval(i.first)) / 2.;
        }
      }
    }

    Json::Value root;
    getJsonRoot(base_path + "/efficiencies.json", root, false);

    for (auto& i: efficiencies) {

      if (ignoreInterpolated && i.second.isInterpolated)
        continue;

      std::stringstream ss;
      ss << i.first;
      std::string mass = ss.str();

      root[getAnalysisUUID()][mass][btagStr][jec] = i.second.getAsJSON();
      std::cout << i.second << std::endl;
      std::cout << std::endl;
    }

    Json::StyledWriter writer;
    std::ofstream output(base_path + "/efficiencies.json");
    output << writer.write(root);
    output.close();
    std::cout << "Efficiencies saved as 'efficiences.json'" << std::endl;

    if (jec == "nominal") {
      TString noteFilename = TString::Format("%s/efficiencies_table_%s_%d_btag.tex", base_path.c_str(), getAnalysisName().c_str(), btagArg.getValue());

      // table latex pour la note :
      std::ofstream latex(noteFilename);
      latex << "\\mtt";

      for (auto& i: efficiencies) {
        if (i.second.isInterpolated)
          continue;
        latex << " & " << i.first << " GeV";
      }

      latex << "\\\\" << std::endl << "\\hline" << std::endl;
      latex << std::setiosflags(std::ios::fixed) << std::setprecision(2);

      latex << "$\\epsilon(Z^{\\prime}), semi-mu$ (\\%)";
      for (auto& i: efficiencies) {
        if (i.second.isInterpolated)
          continue;
        latex << " & " << i.second.selectionEff_mu * 100 << " $\\pm$ " << std::setprecision(4) << i.second.error_selectionEff_mu * 100 << std::setprecision(2);
      }
      latex << "\\\\" << std::endl;

      latex << "$\\epsilon(Z^{\\prime}), semi-e$ (\\%)"; 
      for (auto& i: efficiencies) {
        if (i.second.isInterpolated)
          continue;
        latex << " & " << i.second.selectionEff_e * 100 << " $\\pm$ " << std::setprecision(4) << i.second.error_selectionEff_e * 100 << std::setprecision(2);
      }
      latex << "\\\\" << std::endl;

      latex.close();

      std::cout << "Latex table saved as '" << noteFilename << "'" << std::endl;
    }

  } catch (TCLAP::ArgException& e) {

  }

}
