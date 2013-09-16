#include "Extractor2Histos.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <vector>
#include <TProfile.h>
#include <fstream>

#include "../PUReweighting/PUReweighter.h"
#include "tclap/CmdLine.h"

void Extractor2Histos::Loop()
{

  TH1::SetDefaultSumw2(true);

  TH1D *hNVtx_noweight = new TH1D("hNVtx_noweight", "", 70, 0., 70);
  TH1D *hNVtx = new TH1D("hNVtx", "", 70, 0., 70);
  TH1D *hNVtx_beforesel = new TH1D("hNVtx_beforesel", "", 70, 0., 70);

  TH1D *hNTrueInt = new TH1D("hNTrueInt", "", 70, 0., 70);
  TH1D *hNTrueInt_nosel = new TH1D("hNTrueInt_nosel", "", 70, 0., 70);

  TH1D *hLeptonPt = new TH1D("hLeptonPt", "", 50, 20., 200.);
  TH1D *hLeptonPt_beforesel = new TH1D("hLeptonPt_beforesel", "", 50, 20., 200.);

  TH1D *hMuRelIso = new TH1D("hMuRelIso", "", 50, 0., 0.15);
  TH1D *hMuRelIso_beforesel = new TH1D("hMuRelIso_beforesel", "", 50, 0., 0.15);

  TH1D *hElRelIso = new TH1D("hElRelIso", "", 50, 0., 0.15);
  TH1D *hElRelIso_beforesel = new TH1D("hElRelIso_beforesel", "", 50, 0., 0.15);

  TH1D *h1stjetpt = new TH1D("h1stjetpt", "", 100, 70., 640.);
  TH1D *h1stjetpt_beforesel = new TH1D("h1stjetpt_beforesel", "", 100, 70., 640.);

  TH1D *h2ndjetpt = new TH1D("h2ndjetpt", "", 100, 50., 620.);
  TH1D *h2ndjetpt_beforesel = new TH1D("h2ndjetpt_beforesel", "", 100, 50., 620.);

  TH1D *h3rdjetpt = new TH1D("h3rdjetpt", "", 50, 30., 300.);
  TH1D *h3rdjetpt_beforesel = new TH1D("h3rdjetpt_beforesel", "", 50, 30., 300.);

  TH1D *h4thjetpt = new TH1D("h4thjetpt", "", 50, 30., 300.);
  TH1D *h4thjetpt_beforesel = new TH1D("h4thjetpt_beforesel", "", 50, 30., 300.);

  TH1D *hMET = new TH1D("hMET", "", 100, 20., 400.);
  TH1D *hMET_beforesel = new TH1D("hMET_beforesel", "", 100, 20., 400.);

  TH1D *hmtlep = new TH1D("hmtlep", "", 100, 120., 240.);
  TH1D *hmthad = new TH1D("hmthad", "", 150, 120., 300.);
  
  TH1D *hmtt_MC = new TH1D("hmtt_MC", "", 250, 0., 2500.);
  TH1D *hmtt_MC_nosel = new TH1D("hmtt_MC_nosel", "", 250, 0., 2500.);

  TH1D *hmttSelected_btag_sel = new TH1D("hmttSelected_btag_sel", "", 250, 0., 2500.);
  TH1D *hmttSelected_btag_sel_mass_cut = new TH1D("hmttSelected_btag_sel_mass_cut", "", 250, 0., 2500.);

  TH1D *hNGoodMuons = new TH1D("hNGoodMuons", "", 5, -0.5, 4.5);

  TH1D *hNGoodJets = new TH1D("hNGoodJets", "", 6, 3.5, 9.5);
  TH1D *hNGoodJets_beforesel = new TH1D("hNGoodJets_beforesel", "", 6, 3.5, 9.5);

  TH1D *hNBtaggedJets = new TH1D("hNBtaggedJets", "", 5, -0.5, 4.5);
  TH1D *hNBtaggedJets_beforesel = new TH1D("hNBtaggedJets_beforesel", "", 5, -0.5, 4.5);

  TProfile *pMttResolution_btag_sel = new TProfile("pMttResolution_btag_sel", "", 250, 0., 2500.);
  pMttResolution_btag_sel->SetXTitle("m_{t#bar{t}} [GeV/c^{2}]");


  if (mIsSemiMu) {
    hLeptonPt->SetXTitle("#mu p_{T} [GeV/c]");
    hLeptonPt_beforesel->SetXTitle("#mu p_{T} [GeV/c]");
  } else {
    hLeptonPt_beforesel->SetXTitle("e p_{T} [GeV/c]");
    hLeptonPt->SetXTitle("e p_{T} [GeV/c]");
  }

  h1stjetpt->SetXTitle("1^{st} jet p_{T} [GeV/c]");
  h1stjetpt_beforesel->SetXTitle("1^{st} jet p_{T} [GeV/c]");

  h2ndjetpt->SetXTitle("2^{nd} jet p_{T} [GeV/c]");
  h2ndjetpt_beforesel->SetXTitle("2^{nd} jet p_{T} [GeV/c]");

  h3rdjetpt->SetXTitle("3^{rd} jet p_{T} [GeV/c]");
  h3rdjetpt_beforesel->SetXTitle("3^{rd} jet p_{T} [GeV/c]");

  h4thjetpt_beforesel->SetXTitle("4^{th} jet p_{T} [GeV/c]");

  hMET->SetXTitle("MET [GeV]");
  hMET_beforesel->SetXTitle("MET [GeV]");

  hmtlep->SetXTitle("leptonic m_{t} [GeV/c^{2}]");
  hmthad->SetXTitle("hadronic m_{t} [GeV/c^{2}]");
  
  hmtt_MC->SetXTitle("m_{t#bar{t}} (gen level) [GeV/c^{2}]");
  hmtt_MC_nosel->SetXTitle("m_{t#bar{t}} (gen level) [GeV/c^{2}]");

  hmttSelected_btag_sel->SetXTitle("m_{t#bar{t}} [GeV/c^{2}]");
  hmttSelected_btag_sel_mass_cut->SetXTitle("m_{t#bar{t}} [GeV/c^{2}]");
  hNGoodMuons->SetXTitle("Num good #mu");
  hNGoodJets->SetXTitle("Num good jets");
  hNGoodJets_beforesel->SetXTitle("Num good jets");

  hNBtaggedJets->SetXTitle("Num TCHEL jets");
  hNBtaggedJets_beforesel->SetXTitle("Num TCHEL jets");

  Long64_t nentries = fMTT->GetEntries();

  //PUReweighter puReweighter(mIsSemiMu, mDataset);
  PUReweighter puReweighter(mIsSemiMu);

  std::cout << "Processing..." << std::endl;

  for (Long64_t jentry = 0; jentry < nentries; jentry++)
  {
    if (jentry % 100000 == 0)
      std::cout << "Processing entry #" << (jentry + 1) << " over " << nentries << " (" << (float) jentry / nentries * 100 << "%)" << std::endl;

    GetEntry(jentry);

    double eventWeight = 1.;
    if (mIsMC) {
      eventWeight *= puReweighter.weight(n_trueInteractions);
    } else {
      eventWeight *= m_weight;
    }

    hNTrueInt_nosel->Fill(n_trueInteractions, eventWeight);
    hmtt_MC_nosel->Fill(MC_mtt, eventWeight);

    if (!mIsMC && !m_triggerPassed) {
      continue;
    }

    double ptLepton = -1;
    double ptLeptonCut = -1;
    if (mIsSemiMu)
    {
      if (nGoodMuons <= 0)
        continue;

      ptLepton = muonPt[0];
      ptLeptonCut = 25.;
    }
    else
    {
      if (nGoodElectrons <= 0)
        continue;

      ptLepton = electronPt[0];
      ptLeptonCut = 30.;
    }

    if (ptLepton > ptLeptonCut && isSel == 1 && numComb > 0)
    {

      hNGoodJets_beforesel->Fill(nJets, eventWeight);
      hNBtaggedJets_beforesel->Fill(nBtaggedJets_CSVM, eventWeight);

      hLeptonPt_beforesel->Fill(ptLepton, eventWeight);
      if (mIsSemiMu)
        hMuRelIso_beforesel->Fill(muRelIso[0], eventWeight);
      else
        hElRelIso_beforesel->Fill(elRelIso[0], eventWeight);
      
      hMET_beforesel->Fill(MET, eventWeight);

      h1stjetpt_beforesel->Fill(p_1stjetpt, eventWeight);
      h2ndjetpt_beforesel->Fill(p_2ndjetpt, eventWeight);
      h3rdjetpt_beforesel->Fill(p_3rdjetpt, eventWeight);
      h4thjetpt_beforesel->Fill(p_4thjetpt, eventWeight);

      hNVtx_beforesel->Fill(n_vertices, eventWeight);

      bool btagSel = false;
      if (mBTag == 1)
        btagSel = nBtaggedJets_CSVM == 1;
      else if (mBTag == 2)
        btagSel = nBtaggedJets_CSVM > 1;

      if (btagSel && p_1stjetpt > 70. && p_2ndjetpt > 50 && mtt_AfterChi2 > 0. && bestSolChi2 < 500)
      {
        hLeptonPt->Fill(ptLepton, eventWeight);
        h1stjetpt->Fill(p_1stjetpt, eventWeight);
        h2ndjetpt->Fill(p_2ndjetpt, eventWeight);
        h3rdjetpt->Fill(p_3rdjetpt, eventWeight);
        h4thjetpt->Fill(p_4thjetpt, eventWeight);
        hMET->Fill(MET, eventWeight);

        hNGoodJets->Fill(nJets, eventWeight);
        hNBtaggedJets->Fill(nBtaggedJets_CSVM, eventWeight);

        hNVtx_noweight->Fill(n_vertices);
        hNVtx->Fill(n_vertices, eventWeight);
        hNTrueInt->Fill(n_trueInteractions, eventWeight);

        if (mIsSemiMu)
          hMuRelIso->Fill(muRelIso[0], eventWeight);
        else
          hElRelIso->Fill(elRelIso[0], eventWeight);

        hmtlep->Fill(mLepTop_AfterChi2, eventWeight);
        hmthad->Fill(mHadTop_AfterChi2, eventWeight);

        hmtt_MC->Fill(MC_mtt, eventWeight);

        hmttSelected_btag_sel->Fill(mtt_AfterChi2, eventWeight);
        pMttResolution_btag_sel->Fill(MC_mtt , TMath::Abs(MC_mtt-mtt_AfterChi2), eventWeight);

        if (mtt_AfterChi2 > 500)
        {
          hmttSelected_btag_sel_mass_cut->Fill(mtt_AfterChi2, eventWeight);
        }
      }
    }
  }

  TFile * output = TFile::Open(mOutputFile.c_str(), "recreate");
  output->cd();

  hNVtx_noweight->Write();
  hNVtx->Write();
  hNVtx_beforesel->Write();

  hNTrueInt_nosel->Write();
  hNTrueInt->Write();

  hLeptonPt->Write();
  hLeptonPt_beforesel->Write();

  hMuRelIso->Write();
  hMuRelIso_beforesel->Write();

  hElRelIso->Write();
  hElRelIso_beforesel->Write();

  h1stjetpt->Write();
  h1stjetpt_beforesel->Write();

  h2ndjetpt->Write();
  h2ndjetpt_beforesel->Write();

  h3rdjetpt->Write();
  h3rdjetpt_beforesel->Write();

  h4thjetpt->Write();
  h4thjetpt_beforesel->Write();

  hMET_beforesel->Write();
  hMET->Write();

  hmtlep->Write();
  hmthad->Write();
  hmtt_MC->Write();
  hmtt_MC_nosel->Write();

  hmttSelected_btag_sel->Write();
  hmttSelected_btag_sel_mass_cut->Write();

  hNGoodMuons->Write();
  hNGoodJets->Write();
  hNGoodJets_beforesel->Write();

  hNBtaggedJets->Write();
  hNBtaggedJets_beforesel->Write();

  pMttResolution_btag_sel->Write();

  output->Close();
  delete output;

}

void loadChain(const std::vector<std::string>& inputFiles, const std::string& treeName, TChain*& output) {

  output = new TChain(treeName.c_str());

  for (const std::string& file: inputFiles) {
    output->Add(file.c_str());
  }
}

Extractor2Histos::Extractor2Histos(const std::vector<std::string>& inputFiles, const std::string& outputFile, bool isSemiMu, bool isMC, int btag) : fMTT(0), fVertices(0), fEvent(0)
{
  mIsSemiMu = isSemiMu;
  mIsMC = isMC;
  mOutputFile = outputFile;
  mBTag = btag;

  // Get trees
  loadChain(inputFiles, "Mtt", fMTT);
  loadChain(inputFiles, "Vertices", fVertices);
  loadChain(inputFiles, "event", fEvent);

  Init();
}

Extractor2Histos::~Extractor2Histos()
{
  if (fMTT)
    delete fMTT->GetCurrentFile();

  /*if (fVertices)
    delete fVertices->GetCurrentFile();

    if (fEvent)
    delete fEvent->GetCurrentFile();*/
}

Int_t Extractor2Histos::GetEntry(Long64_t entry)
{
  if (fMTT)
    fMTT->GetEntry(entry);

  if (fVertices)
    fVertices->GetEntry(entry);

  if (fEvent)
    fEvent->GetEntry(entry);

  return 1;
}

void Extractor2Histos::SetBranchAddress(TTree* t, const char* branchName, void* ptr, TBranch** branch) {
  t->SetBranchStatus(branchName, 1);
  t->SetBranchAddress(branchName, ptr, branch);
}

void Extractor2Histos::Init()
{
  fCurrent = -1;
  fMTT->SetMakeClass(1);

  fMTT->SetBranchStatus("*", 0);
  //SetBranchAddress(fMTT, "MC_channel", &MC_channel, &b_MC_channel);
  SetBranchAddress(fMTT, "MC_mtt", &MC_mtt, &b_MC_mtt);
  //SetBranchAddress(fMTT, "MC_nPU", &MC_nPU, &b_m_nPU);
  SetBranchAddress(fMTT, "nGoodMuons", &nGoodMuons, &b_nGoodMuons);
  //SetBranchAddress(fMTT, "nLooseGoodMuons", &nLooseGoodMuons, &b_nLooseGoodMuons);
  if (mIsSemiMu) {
    SetBranchAddress(fMTT, "muonPt", muonPt, &b_muonPt);
    //SetBranchAddress(fMTT, "2DDrMin", p_2DDrMin, &b_2DDrMin);
    //SetBranchAddress(fMTT, "2DpTrel", p_2DpTrel, &b_2DpTrel);
    SetBranchAddress(fMTT, "muRelIso", muRelIso, &b_muRelIso);
  } else {
    SetBranchAddress(fMTT, "nGoodElectrons", &nGoodElectrons, &b_nGoodElectrons);
    SetBranchAddress(fMTT, "electronPt", &electronPt, &b_electronPt);
    SetBranchAddress(fMTT, "elRelIso", &elRelIso, &b_elRelIso);
    //SetBranchAddress(fMTT, "hyperTight1MC", &hyperTight1MC, &b_hyperTight1MC);
  }
  SetBranchAddress(fMTT, "1stjetpt", &p_1stjetpt, &b_1stjetpt);
  SetBranchAddress(fMTT, "2ndjetpt", &p_2ndjetpt, &b_2ndjetpt);
  SetBranchAddress(fMTT, "3rdjetpt", &p_3rdjetpt, &b_3rdjetpt);
  SetBranchAddress(fMTT, "4thjetpt", &p_4thjetpt, &b_4thjetpt);
  SetBranchAddress(fMTT, "nJets", &nJets, &b_nJets);
  //SetBranchAddress(fMTT, "jetEta", jetEta, &b_jetEta);
  SetBranchAddress(fMTT, "jetPt", jetPt, &b_jetPt);
  SetBranchAddress(fMTT, "nBtaggedJets_CSVM", &nBtaggedJets_CSVM, NULL);
  //SetBranchAddress(fMTT, "nBtaggedJets_TCHEM", &nBtaggedJets_TCHEM, &b_nBtaggedJets_TCHEM);
  //SetBranchAddress(fMTT, "nBtaggedJets_TCHET", &nBtaggedJets_TCHET, &b_nBtaggedJets_TCHET);
  //SetBranchAddress(fMTT, "nBtaggedJets_TCHPL", &nBtaggedJets_TCHPL, &b_nBtaggedJets_TCHPL);
  //SetBranchAddress(fMTT, "nBtaggedJets_TCHPM", &nBtaggedJets_TCHPM, &b_nBtaggedJets_TCHPM);
  //SetBranchAddress(fMTT, "nBtaggedJets_TCHPT", &nBtaggedJets_TCHPT, &b_nBtaggedJets_TCHPT);
  //SetBranchAddress(fMTT, "nBtaggedJets_SSVHEM", &nBtaggedJets_SSVHEM, &b_nBtaggedJets_SSVHEM);
  //SetBranchAddress(fMTT, "nBtaggedJets_SSVHPT", &nBtaggedJets_SSVHPT, &b_nBtaggedJets_SSVHPT);
  SetBranchAddress(fMTT, "MET", &MET, &b_MET);
  SetBranchAddress(fMTT, "isSel", &isSel, &b_isSel);
  //SetBranchAddress(fMTT, "oneMatchedCombi", &oneMatchedCombi, &b_oneMatchedCombi);
  SetBranchAddress(fMTT, "bestSolChi2", &bestSolChi2, &b_bestSolChi2);
  //SetBranchAddress(fMTT, "isBestSolMatched", &isBestSolMatched, &b_isBestSolMatched);
  //SetBranchAddress(fMTT, "KFChi2", &KFChi2, &b_KFChi2);
  SetBranchAddress(fMTT, "numComb", &numComb, &b_numComb);
  //SetBranchAddress(fMTT, "solChi2", solChi2, &b_solChi2);
  SetBranchAddress(fMTT, "mLepTop_AfterChi2", &mLepTop_AfterChi2, &b_mLepTop_AfterChi2);
  SetBranchAddress(fMTT, "mHadTop_AfterChi2", &mHadTop_AfterChi2, &b_mHadTop_AfterChi2);
  SetBranchAddress(fMTT, "mtt_AfterChi2", &mtt_AfterChi2, &b_mtt_AfterChi2);
  //SetBranchAddress(fMTT, "mLepTop_AfterChi2andKF", &mLepTop_AfterChi2andKF, &b_mLepTop_AfterChi2andKF);
  //SetBranchAddress(fMTT, "mHadTop_AfterChi2andKF", &mHadTop_AfterChi2andKF, &b_mHadTop_AfterChi2andKF);
  //SetBranchAddress(fMTT, "mtt_AfterChi2andKF", &mtt_AfterChi2andKF, &b_mtt_AfterChi2andKF);
  SetBranchAddress(fMTT, "weight", &m_weight, NULL);

  if (fMTT->GetBranch("trigger_passed")) {
    SetBranchAddress(fMTT, "trigger_passed", &m_triggerPassed, NULL);
  } else {
    // Backward compatibilty
    m_triggerPassed = true;
  }

  fVertices->SetMakeClass(1);
  fVertices->SetBranchAddress("n_vertices", &n_vertices, NULL);
  fVertices->SetBranchStatus("*", 0);
  fVertices->SetBranchStatus("n_vertices", 1);

  fEvent->SetMakeClass(1);
  fEvent->SetBranchAddress("nTrueInteractions", &n_trueInteractions, NULL);
  fEvent->SetBranchStatus("*", 0);
  fEvent->SetBranchStatus("nTrueInteractions", 1);
}

void loadInputFiles(const std::string& filename, std::vector<std::string>& files) {

  ifstream ifs(filename.c_str());
  std::string line;

  while (getline(ifs, line))
    files.push_back(line);

  ifs.close();
}

int main(int argc, char** argv) {

  try {

    TCLAP::CmdLine cmd("Convert extractor tuples to histograms", ' ', "0.1");

    TCLAP::ValueArg<std::string> inputListArg("", "input-list", "A text file containing a list of input files", true, "", "string");
    TCLAP::ValueArg<std::string> inputFileArg("i", "input-file", "The input file", true, "", "string");

    cmd.xorAdd(inputListArg, inputFileArg);

    TCLAP::ValueArg<std::string> outputFileArg("o", "output-file", "output file", true, "", "string", cmd);

    TCLAP::SwitchArg dataArg("", "data", "Is this data?", false);
    TCLAP::SwitchArg mcArg("", "mc", "Is this mc?", false);

    cmd.xorAdd(dataArg, mcArg);

    TCLAP::SwitchArg semimuArg("", "semimu", "Is this semi-mu channel?", false);
    TCLAP::SwitchArg semieArg("", "semie", "Is this semi-e channel?", false);

    cmd.xorAdd(semimuArg, semieArg);

    TCLAP::ValueArg<int> btagArg("", "b-tag", "Number of b-tagged jet to require", true, 2, "int", cmd);

    TCLAP::ValueArg<std::string> pileupArg("", "pileup", "PU profile used for MC production", false, "S10", "string", cmd);

    TCLAP::ValueArg<std::string> pileupSystArg("", "pileup-syst", "PU profile to use for pileup reweigthing", false, "nominal", "string", cmd);
    TCLAP::ValueArg<std::string> pdfSystArg("", "pdf-syst", "PDF systematic to compute", false, "nominal", "string", cmd);


    TCLAP::ValueArg<int> maxEntriesArg("n", "", "Maximal number of entries to process", false, -1, "int", cmd);
    TCLAP::ValueArg<double> generatorWeightArg("", "weight", "MC generator weight", false, 1., "double", cmd);

    cmd.parse(argc, argv);

    PUProfile puProfile;
    std::string p = pileupArg.getValue();
    std::transform(p.begin(), p.end(), p.begin(), ::tolower);
    if (p == "s6")
      puProfile = PUProfile::S6;
    else if (p == "s7")
      puProfile = PUProfile::S7;
    else if (p == "s10")
      puProfile = PUProfile::S10;

    std::string puSyst = pileupSystArg.getValue();
    std::transform(puSyst.begin(), puSyst.end(), puSyst.begin(), ::tolower);
    if (puSyst != "nominal" && puSyst != "up" && puSyst != "down") {
      std::cerr << "--pilup-syst can only be 'nominal', 'up' or 'down'" << std::endl;
      exit(1);
    }

    std::string pdfSyst = pdfSystArg.getValue();
    std::transform(pdfSyst.begin(), pdfSyst.end(), pdfSyst.begin(), ::tolower);
    if (pdfSyst != "nominal" && pdfSyst != "up" && pdfSyst != "down") {
      std::cerr << "--pdf-syst can only be 'nominal', 'up' or 'down'" << std::endl;
      exit(1);
    }
    
    bool isData = dataArg.isSet();

    std::vector<std::string> inputFiles;
    if (inputFileArg.isSet()) {
      inputFiles.push_back(inputFileArg.getValue());
    } else {
      loadInputFiles(inputListArg.getValue(), inputFiles);
    }
    
    Extractor2Histos convertor(inputFiles, outputFileArg.getValue(), semimuArg.isSet(), !isData, btagArg.getValue());
    convertor.Loop();

  } catch (TCLAP::ArgException &e) {
    std::cerr << "error: " << e.error() << " for arg " << e.argId() << std::endl;
    return 1;
  }

  return 0;
}
