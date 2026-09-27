# ___________________________________________
# Evaluation questions in dict format (Luke), making 16. You guys can remove 6 or something if I made too many.
# ___________________________________________
eval_questions_dict = {"inverter question":"What are the current Australian standards for inverters?", # Based on a google suggestion
                       "STC question":"Who should be accredited for STCs?",
                       "STC question":"What are the maximum daily of installations I can do to claim STCs?",
                       "STC question":"Can a stackable battery system be eligible for STCs?",
                       "STC question":"What should my photos look like for evidence to get STCs?",
                       "STC question":"Do I need to have evidence to get an STC?",
                       "RET question":"What is the renewable energy target?",
                       "miscellaneous":"What are Postcode zones?",
                       "miscellaneous":"What does each postcode zone represent?",
                       "RET question":"How does the RET work?",
                       "STC question":"What types of small scale renewable energy systems are eligible under the SRES?",
                       "STC question":"What capacity and annual electricity output limits apply to wind and hydro systems for STC eligibility?",
                       "STC question":"When upgrading an existing solar PV system with new panels and an inverter, what conditions must be met for the upgrade to be eligible for STCs?",
                       "STC question":"If a household completely replaces its existing rooftop solar system, what conditions must the new system meet to be eligible for STCs?",
                       "RET question":"What is the difference between a small scale system and a power station under the Renewable Energy Target?",
                       "RET question":"What requirements must a power station meet under the Renewable Energy Target?",
                       "STC question":"What conditions must a solar PV, battery, wind or hydro system meet to be eligible for STCs?",
                       "Solar question":"What deeming period applies to a solar PV system installed in 2024?",
                       "installations":"When can I apply to mid-scale solar installation in 2026?",
                       "Solar question":"Can I apply to a rebate to switch to solar?",
                       "inverter question":"Can I apply for a new inverter to my existing system if my inverter is not on the CEC approved products list",
                       "installations":"Can my solar battery be created within 24 months of the installation",
                       "installations":"What if my additional new inverter has a rating of 100kW, can I install this into my house",
                       "Solar question":"What do I need to keep in mind when replacing my original rooftop solar system",
                       "installations":"What is the total annual electricity output requirement to install a wind turbine system",
                       "miscellaneous":"How do you define a small-scale system?",
                       "Out-of-scope-question":"How to build a power station", #Strange question
                       "miscellaneous":"If a Chint New Energy Technology Co Ltd models with multiple suffixes gets damaged can one alternate the suffix so it aligns with the current CEC listing suffix format", # No questionmark questions will be interesting.
                       "inverter question":"Would inverters after installation need a connection to a meter or main grid",
                       "evidence/compliance/safety question":"What are the necessary steps regarding Installer on-site verification photos",
                       "inverter question":"Does Force 5S (AS4777-2 2020) come under the list of approved inverters by Clean Energy Council",
                       "Solar question":"Under what circumstances can multiple installers work on the same solar installation?",
                       "STC question":"Under what circumstances would a STC claim fail:", # colon?
                       "evidence/compliance/safety question":"What requirements must products meet to connect to Australian electricity networks using CSIP-AUS?",
                       "miscellaneous":"What was the New Expiry date of  AERL LiFe2-5120S?",
                       "inverter question":"What is the requirements for the isolation of the inverter inputs when PV is the energy source?",
                       "miscellaneous":"Is uasge of the new AS/NZS 5033:2021 before the commencement date practical/viable/allowed?", # A typo might be good to test for hallucinations e.c.t.
                       "identifier question (who is in charge)":"Which standard governs general electrical installations in Australia?",
                       "installations":"What are the most vital OH&S regulations when it comes to installing electrical equipment?",
                       "evidence/compliance/safety question":"What tests must be performed before energising new electrical equipment/work?",
                       "evidence/compliance/safety question":"How do you verify equipment safety compliance prior to setup?",
                       "installations":"What isolation steps are required before starting installation?",
                       "STC question":"How long after installation do I have to claim STCs (Small-scale Technology Certificate) for a system?",
                       "identifier question (who is in charge)":"Who accredits solar installers in Australia, CEA or SAA?",
                       "identifier question (who is in charge)":"What Australian Standard governs the installation of electrical equipment in hazardous areas?",
                       "evidence/compliance/safety question":"How often must portable electrical equipment on a worksite be tested?",
                       "installations":"What separation distance must be maintained from overhead powerlines during installation work?",
                       "identifier question (who is in charge)":"Who is legally authorised to issue a Certificate of Electrical Safety?"}


for eval_questions_dict.values():
    for key in eval_questions_dict.keys():
        if key == "installations":
            print(eval_questions_dict[key])