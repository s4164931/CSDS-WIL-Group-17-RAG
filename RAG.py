from deepagents import create_deep_agent
from langchain.messages import HumanMessage

"""electric_Energy_Docs = ["https://en.wikipedia.org/wiki/Electrical_energy",
                        "https://www.thoughtco.com/electrical-energy-definition-and-examples-4119325",
                        "https://www.eia.gov/energyexplained/electricity/the-science-of-electricity.php",
                        "https://en.wikipedia.org/wiki/Electric_current",
                        "https://www.britannica.com/technology/electric-circuit",
                        "https://en.wikipedia.org/wiki/Voltage",
                        "https://learn.sparkfun.com/tutorials/alternating-current-ac-vs-direct-current-dc/all",
                        "https://www.wevolver.com/article/parallel-vs-series-circuits-differences-theory-and-practical-applications",
                        "https://en.wikipedia.org/wiki/Watt",
                        "https://cc-techgroup.com/blog/what-is-resistance/",
                        "https://en.wikipedia.org/wiki/Electrolysis",
                        "https://www.britannica.com/science/electricity"]"""
# electric energy, voltage, electric circuit, electric current, AC/DC, watts, parrallel vs series circuits, resistance, ohms, electrolysis,
# electricity, energy
# this was the old websites, which we might not use.

# ___________________________________________
# Evaluation questions in dict format (Luke), making 16. You guys can remove 6 or something if I made too many.
# ___________________________________________

eval_questions_dict = {1:"What are the current Australian standards for inverters?", # Based on a google suggestion
                       2:"Who should be accredited for STCs?",
                       3:"What are the maximum daily of installations I can do to claim STCs?",
                       4:"Can a stackable battery system be eligible for STCs?",
                       5:"What should my photos look like for evidence to get STCs?",
                       6:"Do I need to have evidence to get an STC?",
                       7:"What is the renewable energy target?",
                       8:"What are Postcode zones?",
                       9:"What does each postcode zone represent?",
                       10:"How does the RET work?",
                       11:"What types of small scale renewable energy systems are eligible under the SRES?",
                       12:"What capacity and annual electricity output limits apply to wind and hydro systems for STC eligibility?",
                       13:"When upgrading an existing solar PV system with new panels and an inverter, what conditions must be met for the upgrade to be eligible for STCs?",
                       14:"If a household completely replaces its existing rooftop solar system, what conditions must the new system meet to be eligible for STCs?",
                       15:"What is the difference between a small scale system and a power station under the Renewable Energy Target?",
                       16:"What requirements must a power station meet under the Renewable Energy Target?",
                       17:"What conditions must a solar PV, battery, wind or hydro system meet to be eligible for STCs?",
                       18:"What deeming period applies to a solar PV system installed in 2024?",
                       19:"When can I apply to mid-scale solar installation in 2026?",
                       20:"Can I apply to a rebate to switch to solar?",
                       21:"",
                       22:"", # Hassini's questions will go here.
                       23:"",
                       24:"",
                       25:"",
                       26:"",
                       27:"",
                       28:"If a Chint New Energy Technology Co Ltd models with multiple suffixes gets damaged can one alternate the suffix so it aligns with the current CEC listing suffix format", # No questionmark questions will be interesting.
                       29:"Would inverters after installation need a connection to a meter or main grid",
                       30:"What are the necessary steps regarding Installer on-site verification photos",
                       31:"Does Force 5S (AS4777-2 2020) come under the list of approved inverters by Clean Energy Council",
                       32:"Under what circumstances can multiple installers work on the same solar installation?",
                       33:"Under what circumstances would a STC claim fail:", # colon?
                       34:"What requirements must products meet to connect to Australian electricity networks using CSIP-AUS?",
                       35:"What was the New Expiry date of  AERL LiFe2-5120S?",
                       36:"What is the requirements for the isolation of the inverter inputs when PV is the energy source?",
                       37:"Is uasge of the new AS/NZS 5033:2021 before the commencement date practical/viable/allowed?", # A typo might be good to test for hallucinations e.c.t.
                       38:"Which standard governs general electrical installations in Australia?",
                       39:"What are the most vital OH&S regulations when it comes to installing electrical equipment?",
                       40:"What tests must be performed before energising new electrical equipment/work?",
                       41:"How do you verify equipment safety compliance prior to setup?",
                       42:"What isolation steps are required before starting installation?",
                       43:"How long after installation do I have to claim STCs (Small-scale Technology Certificate) for a system?",
                       44:"Who accredits solar installers in Australia, CEA or SAA?",
                       45:"What Australian Standard governs the installation of electrical equipment in hazardous areas?",
                       46:"How often must portable electrical equipment on a worksite be tested?",
                       47:"What separation distance must be maintained from overhead powerlines during installation work?",
                       48:"Who is legally authorised to issue a Certificate of Electrical Safety?"}


placeholder = {1:"What is one houshold item that is using a lot of energy consumption?",
                       2:"How can I reduce my energy consumption?",
                       3:"What is causing the most energy consumption? The fridge, the oven or the kettle?",
                       4:"Would using solar panels reduce energy consumption?",
                       5:"Would five solar panels be able to generate enough energy for all household items in the average household?",
                       6:"What is one household item that is using little energy consumption?",
                       7:"What are simple things that I can do right now to reduce energy consumption?",
                       8:"Do lights use more energy consumption than fans?",
                       9:"Would leaving everything on reduce energy consumption?", # this should give a no answer.
                       10:"How many solar panels do we need for a large house with a lot of household items?", # a little ambiguous
                       11:"What is the average energy consumption for any household?",
                       12:"What would increase my energy consumption?",
                       13:"Do solar panels use more energy consumption than traditional methods?",
                       14:"What is using the least energy consumption? The lights, the TV or the fridge?",
                       15:"How do I reduce my energy consumption, without having to decrease the quality of life?", # Maybe?
                       16:"Would ten solar panels be able to generate enough energy for all household items in a large household?"}