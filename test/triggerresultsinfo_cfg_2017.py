import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Diagnosis")


options = VarParsing.VarParsing ('analysis')
options.inputFiles =  '/store/data/Run2017C/BTagCSV/MINIAOD/PromptReco-v2/000/300/395/00000/1ECA5C25-E07B-E711-B6BE-02163E01A1E9.root',
#options.inputFiles =  '/store/data/Run2017C/BTagCSV/MINIAOD/PromptReco-v1/000/299/368/00000/7ED71BDC-8D6D-E711-A6CE-02163E014491.root',
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
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v8')


process.triggerinfo = cms.EDAnalyzer('TriggerResultsInfo',
   TriggerResults = cms.InputTag("TriggerResults","","HLT"), 
)


process.p = cms.Path(process.triggerinfo)

# ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
JSONfile = 'txtfiles/json_300395.txt'
myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
process.source.lumisToProcess.extend(myLumis)
