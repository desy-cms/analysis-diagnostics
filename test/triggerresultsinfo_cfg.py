import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Diagnosis")

options = VarParsing.VarParsing ('analysis')
options.inputFiles =  '/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/SKIM/mc/2017/Neutrino/83x/L1Menu_Collisions2017_dev_r2/PU53to57/SingleNeutrino/Neutrino83x/170511_093734/0000/L1REPACK_FullMC_SKIM_99.root',
#options.inputFiles =  'file:/afs/desy.de/user/w/walsh/cms/analysis/cmssw/hlt/CMSSW_8_0_24/src/HLTrigger/Configuration/mssmhbb/QCD_Pt-120to170_MuEnrichedPt5_User_tranche4_l1repack.root',
#options.inputFiles =  '/store/mc/RunIISummer16DR80/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/130000/08C6F278-E0A2-E611-BE0C-002590D9DA9C.root',
options.parseArguments()

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.source = cms.Source ("PoolSource",
                             fileNames      = cms.untracked.vstring (options.inputFiles),
                             )

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2017_TSG_Hcal_V3')


process.triggerinfo = cms.EDAnalyzer('TriggerResultsInfo',
   TriggerResults = cms.InputTag("TriggerResults","","SIM"),
)


process.p = cms.Path(process.triggerinfo)

