// -*- C++ -*-
//
// Package:    Analysis/Diagnosis
// Class:      TriggerResultsInfo
// 
/**\class TriggerResultsInfo TriggerResultsInfo.cc Analysis/Diagnosis/plugins/TriggerResultsInfo.cc

 Description: Obtain trigger information from a EDM file. For MC it is straightforward, 
              for data be careful how you use the information!

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Roberval Walsh
//         Created:  Tue, 18 Oct 2016 09:19:51 GMT
//
//


// system include files
#include <memory>
#include <iostream>
#include <fstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Trigger related includes
#include "DataFormats/Common/interface/TriggerResults.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"


//
// class declaration
//

class TriggerResultsInfo : public edm::EDAnalyzer
{
   public:
      explicit TriggerResultsInfo(const edm::ParameterSet&);
      ~TriggerResultsInfo();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
      virtual void beginRun(const edm::Run&, const edm::EventSetup&); 
      virtual void endRun(const edm::Run&, const edm::EventSetup&); 

      // ----------member data ---------------------------
      
      bool first_;
      edm::InputTag triggerResults_;
      edm::EDGetTokenT<edm::TriggerResults> triggerResultsTokens_;
      HLTPrescaleProvider hltPrescaleProvider_;
      HLTConfigProvider hltConfig_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
TriggerResultsInfo::TriggerResultsInfo(const edm::ParameterSet& config):
   first_(true),
   triggerResults_(config.getParameter<edm::InputTag> ("TriggerResults")),
   triggerResultsTokens_(consumes<edm::TriggerResults>(triggerResults_)),
   hltPrescaleProvider_(config, consumesCollector(), *this)
{
   //now do what ever initialization is needed
   
}


TriggerResultsInfo::~TriggerResultsInfo()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void TriggerResultsInfo::analyze(const edm::Event& event, const edm::EventSetup& setup)
{
   using namespace edm;

}


// ------------ method called once each job just before starting event loop  ------------
void TriggerResultsInfo::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void TriggerResultsInfo::endJob() 
{
}


void TriggerResultsInfo::beginRun(const edm::Run & run, const edm::EventSetup & setup)
{

   // MAIN STUFF
   // to be called every run
   bool changed(true);
   // initialise the holders of trigger information
   hltPrescaleProvider_.init(run, setup, triggerResults_.process(), changed);
   hltConfig_ = hltPrescaleProvider_.hltConfigProvider();
   // -------------
   
   // PRINT NAMES AND OBJECTS FOR ALL TRIGGERS
   // be careful! not supposed to be used directly in an analysis, need further changes in the code
   // this info may change if config changes but it will be printed for the first event only 
   if ( first_ )
   {
   
      std::string tablename = hltConfig_.tableName();  // menu
      std::string globaltag = hltConfig_.globalTag();  // global tag
      
      // Output the trigger paths and corresponding objects into a text file
      std::string outfileName = tablename;
      outfileName.erase(0,1);
      std::replace( outfileName.begin(), outfileName.end(), '/', '_');
      outfileName += "-";
      outfileName += globaltag;
      outfileName += ".txt";
      std::ofstream outfile(outfileName.c_str());
      
      outfile << "HLT ConfDB table name = " <<tablename << std::endl;
      outfile << "GlobalTag = " << globaltag << std::endl;
      outfile << "========================================" << std::endl;
      outfile << std::endl;
      
      // Loop over all triggers
      std::vector<std::string> triggerNames = hltConfig_.triggerNames();
      for ( size_t i = 0 ; i < triggerNames.size() ; ++i )
      {
         // L1 seeds
         const std::vector< std::string > & l1TSeeds = hltConfig_.hltL1TSeeds(triggerNames.at(i));
         
         // trigger objects
         const std::vector<std::string> & saveTags = hltConfig_.saveTagsModules(triggerNames.at(i));
         outfile << triggerNames.at(i) << std::endl;
         
         for ( size_t j = 0; j < l1TSeeds.size(); ++j )
         {
            outfile << "   L1T Seed: " << l1TSeeds.at(j) << ","<< std::endl;
         }
         for ( size_t j = 0; j < saveTags.size() ; ++j )
         {
            outfile << "           Trigger Object:               '" << saveTags.at(j) << "'," << std::endl;
         }
         outfile << "----------------------------------------" << std::endl;
         outfile << std::endl;
      }
      
      
      // Loop over all triggers
      for ( size_t i = 0 ; i < triggerNames.size() ; ++i )
      {
         // L1 seeds
         const std::vector< std::string > & l1TSeeds = hltConfig_.hltL1TSeeds(triggerNames.at(i));
         
         // trigger objects
         const std::vector<std::string> & saveTags = hltConfig_.saveTagsModules(triggerNames.at(i));
         outfile << "| " << triggerNames.at(i) << " | ";
         
         for ( size_t j = 0; j < l1TSeeds.size(); ++j )
         {
            if ( j > 0 ) break;
            outfile << l1TSeeds.at(j) << " | ";
            
         }
         for ( size_t j = 0; j < saveTags.size() ; ++j )
         {
            outfile << saveTags.at(j) << " <br> ";
         }
         outfile << " |  | " << std::endl;
         outfile << std::endl;
      }
      
      
      first_ = false;
      outfile.close();
      
   }

}


// ------------ method called when ending the processing of a run  ------------

void TriggerResultsInfo::endRun(edm::Run const& run, edm::EventSetup const& setup)
{
   
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TriggerResultsInfo::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerResultsInfo);
