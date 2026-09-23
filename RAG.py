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


data_dict = {1:"From 18 December 2021, the current Australian standard will be the AS/NZS 4777.2:2020 version.",
             2:"Any individual who wishes to design or install Grid Connected PV systems (GCPV), Grid Connected Battery systems (GCBS) or Stand-alone Power Systems (SPS), must be accredited under the SAA Scheme in order to be eligible for small-scale technology certificates (STCs).",
             3:"Installers can claim no more than 2 installations per day. This may include: 2 solar batteries, 2 solar PV systems or 1 solar PV system and 1 solar battery.",
             4:"To be eligible for STCs, new battery modules added to an existing stackable battery system must meet these requirements: The final configuration of the stackable battery system is on the CEC’s approved product list at the date of certification. If the battery management module, or another component no longer matches the current approved product, then the system is ineligible. The SAA accredited installer completes the installation and re-certifies the entire system (including the connection to the electrical installation) as safe, compliant and meeting all requirements. The installer is expected to identify and upgrade any parts of the existing system as needed. There may be other jurisdictional requirements installers need to comply with such as inspections or notifications to Distribution Network Service Providers. The additional modules and existing system are compatible in all ways and are within manufacturer specifications to add modules in that way.",
             5:"Your photos should: clearly show your face, show the 3 stages of installation, (for example: a letterbox or the front of the property for setup, racking visible on the roof for mid-installation and the installed system for testing and commissioning.), include date and time metadata and geolocation and match the time and dates of compliance paperwork like certificates and forms.",
             6:"You must have evidence to prove you were on site for the 3 stages of installation. The easiest way is through photos.",
             7:"The Renewable Energy Target (RET) is an Australian Government scheme that aims to reduce greenhouse gas emissions in the electricity sector and increase renewable electricity generation. The RET sets a target to deliver an extra 33,000 gigawatt-hours (GWh) of electricity from renewable sources every year from 2020 to 2030.",
             8:"Postcode zones are one of the factors used to calculate the quantity of renewable energy certificates a solar photovoltaic (PV) system may be eligible for once it is installed.",
             9:"Each zone represents the level of solar radiation for a geographical area. ",
             10:"The RET operates by creating tradable renewable energy certificates, which can be traded to offset the cost of installing an eligible renewable energy system. Each certificate represents one megawatt hour of electricity generated or displaced by a renewable energy system. Liable entities are required to purchase and surrender renewable energy certificates. This increases the demand for renewable energy and stimulates investment in renewable energy technologies, reduces the cost of renewable energy over time and contributes to the reduction of greenhouse gas emissions.",
             11:"The six types of small scale systems eligible under the scheme are solar PV systems, solar batteries, wind turbines, hydro systems, solar water heaters and air source heat pumps. Classification as a small scale system is based on system capacity.",
             12:"A wind turbine system must have a capacity less than 10 kW and annual electricity output less than 25 MWh. A hydro system must have a capacity less than 6.4 kW and annual electricity output less than 25 MWh.",
             13:"The total system capacity after the upgrade must be no more than 100 kW. The new panels and inverter must be on the approved products list, the new inverter must have sufficient capacity, all components must meet current relevant standards and the system must comply with state and territory laws. Existing panels cannot be included in the new STC claim.",
             14:"The new system must have a rating of no more than 100 kW. The panels and inverter must be new and have had no previous STC claims, must be on the approved products list at the time of installation, and must meet all relevant current standards.",
             15:"Classification as a small scale system is based on system capacity. Systems with higher generation capacity are classified as power stations under the LRET. Solar batteries, solar water heaters and air source heat pumps are not eligible under the LRET.",
             16:"Power stations participating in the LRET must apply for accreditation. The application is assessed against eligibility requirements and accredited power stations have ongoing accreditation and compliance obligations.",
             17:"The system must have STCs created within 12 months of installation, have relevant panels, batteries or inverters listed on the approved products list, meet Australian and New Zealand standards, be designed and installed by appropriately accredited SAA personnel, comply with SAA design and installation guidelines, satisfy relevant local/state/territory/federal requirements and be classified as small scale.",
             18:"The deeming period for solar PV, solar water heaters, and air-sourced heat pumps decreases by one year for all systems installed after 1 January 2024. For systems installed in 2024, the maximum deeming period is 7 years.",
             19:"The Renewable Energy (Electricity) Regulations 2011 have been amended to expand eligibility for solar PV systems under the Small-scale Renewable Energy Scheme from 100 kW to 1 MW. These changes will apply to mid-scale solar installed from 1 October 2026. Applications are expected to open in mid to late November 2026. Eligible systems installed on or after 1 October 2026 will be able to apply once applications open.",
             20:"Solar Victoria offers rebates and interest-free loans to support eligible households to switch to solar, including: A $1,400 rebate and interest-free loan to install rooftop solar panels (PV) on a home or rental property and a $1,000 rebate to install a heat pump or solar hot water system. More than 250,000 Victorian households have switched to solar with help from a Solar Victoria rebate to-date.",
             21:"A home adds a new inverter and new panels to an existing system. The existing panels are in good condition, so the householder wants to connect both the existing panels and the new panels to the new inverter. STCs have already been claimed for the existing system. The upgrade will be eligible if: the total system capacity after the upgrade has a rating of no more than 100 kW, the new panels and new inverter are on the CEC approved products list, the new inverter has sufficient capacity, all components meet the current relevant standards, the system meets all relevant state and territory laws, including electrical safety regulations and the existing panels are not included in the new claim for STCs.",
             22:"A solar PV, solar battery, wind or hydro system must have STCs created within 12 months of the installation, have its panels, batteries or inverters listed on the Clean Energy Council (CEC) list of approved components, meet Australian and New Zealand standard, be designed and installed by a Solar Accreditation Australia (SAA) accredited designer and installer appropriately accredited for the installation type, meet SAA design and install guidelines, comply with all local, state, territory and federal requirements, including electrical safety, be classified as small-scale.",
             23:"A house has an existing rooftop solar system. They install an additional inverter and new panels. The additional system will be eligible if: the combined capacity of the systems has a rating of no more than 100 kW, the new panels and new inverter are on the CEC approved products list and all components meet the current relevant standards.",
             24:"A house replaces its original rooftop solar system in its entirety. This includes removing the original system to install a new inverter and panels. The new system will be eligible if: the system has a rating of no more than 100 kW, the panels and inverter are new, with no previous STC claims, the new panels and new inverter are on the CEC approved products list at the time of installation and all components meet the current relevant standards.",
             25:"To be eligible to earn STCs, your wind turbine system must: have a capacity less than 10 kW and have a total annual electricity output less than 25 MWh. To be eligible to earn STCs, your hydro system must: have a capacity less than 6.4 kW and have a total annual electricity output less than 25 MWh. If you want a wind or hydro system to supply power to your school, community organisation or small business, your system may need a higher capacity or output.",
             26:"Six types of small-scale systems are eligible under the scheme: solar PV systems, solar batteries, wind turbines, hydro systems, solar water heaters and air source heat pumps. Classification as a small-scale system is based on the system's capacity. Systems that generate energy with higher capacity are classified as power stations under the LRET. Water heaters, air-sourced heat pumps and solar batteries aren't eligible under the LRET.",
             27:"Power stations: must apply for accreditation, are subject to technical assessment and have ongoing obligations to maintain accreditation.",
             28:"", # Leon needs to show what data we need for this entry.
             29:"For grid-connected systems, inverters don't need a connection to a meter or main grid to classify as complete.",
             30:"As an installer you must take: geotagged and time-stamped photos (‘selfies’) at each phase of installation (including: job setup, mid-installation and testing and commissioning.) and a final ‘completion’ photo that matches the test date on the electrical certificate of compliance (or equivalent).",
             31:"", # Leon also needs to decide what data specifically here.
             32:"There can be multiple installers on an installation if: multiple installers are needed throughout, an installer can't complete the whole installation or the job is handed over from one installer to another. Before the installation, you must notify us of: details of the installation, details of each installer and a rationale for the change of installer. Each installer must: be accredited for the installation type (off grid or on grid) and have an electrical licence for all installation stages.",
             33:"We may fail an STC claim if your evidence doesn't show the 3 stages of installation.",
             34:"To support connection to Australian electricity networks using CSIP-AUS, relevant parties must: Ensure products are certified to CSIP-AUS, Ensure products are listed with the CEC; and Pre-register and onboard to NEPKI to obtain PKI certificates for secure communications.",
             35:"December 2027 (New date suggested regularly).",
             36:"The requirement (AS/NZS 5033): Clause 4.4.1.1 requires a means to isolate PV arrays from the inverter. Clause 4.4.1.2 then provides three options that an installer may choose which would meet the requirement of the previous clause (These options are either: An adjacent and physically separate dc isolator, a dc isolator that is mechanically interlocked with a replaceable module of the inverter which allows for the removal of the module without risk of electric shock or a dc isolator located in the same external enclosure as the other components of the inverter and when in the open position, there shall be no risk of electrical hazards when any inverter external cover is removed).",
             37:"Yes, the 2021 edition may be used prior to the commencement date.",
             38:"The primary standard governing industrial electrical installation in Australia is AS/NZS 3000, universally known as the Australian/New Zealand Wiring rules.",
             39:"Employers must eliminate electrical risks so far as reasonably practicable, or otherwise reduce them. Where electrical work counts as high-risk construction work (HRCW), a Safe Work Method Statement (SWMS) must be prepared beforehand, describing the risk controls, how they’ll be implemented, and how de-energisation will be verified.",
             40:"There are five electrical tests that are most consistently required across Australian workplaces and electrical installations. The first is a continuity test of the protective earth conductor, which verifies that the earth conductor connecting a piece of electrical equipment or an installation back toe the main earth is intact and has sufficiently low resistance. The second is an insulation resistance test that measures the resistance of the insulation surrounding electrical conductors. The third is a polarity verification test that confirms that active, neutral, and earth conductors have been correctly connected throughout a fixed installation. The fourth is a Residual Current Device (RCD) operating time test, which are the primary protection against electric shock in Australian electrical installations and workplaces. And the fifth is an earth fault loop impedance (ELFI) test that measures the total impedance of the path a fault current would travel if an active conductor came into contact with an earthed metal part.",
             41:"Verifying equipment safety compliance prior to setup requires a variety of protocols that need to be kept in mind for successful equipment validation, this includes ensuring that all required documentation are verified and available, verifying the design of the equipment and its components in accordance with specifications and verification norms, thoroughly checking all electrical connections and power supply the equipment before starting the validation process, verifying the quality of input supplies and connections and checking for leaks, testing safety checks and their compliance, calibrating any sensors or monitoring instruments appropriately, checking instruments for operation in various environments, ensure that standard operating procedures are available, and listing and verifying the instruments used to validate the installation qualification and ensuring they are within the due date for re-calibration.",
             42:"Safe isolation before starting installation requires shutting down, locking and tagging all energy sources, and testing to prove a zero-energy state. Key isolation steps include consulting and notifying with the site manager, identifying all energy sources, shutting down and switching off the specific circuit, complete LOTO (lock out and tag out), and testing and proving that zero voltage or energy is present before touching the equipment.",
             43:"STCs can only be claimed if certificates are created within 12 months of installation, and the panels and inverter must be listed on the Clean Energy Council’s approved components list at the time of installation.",
             44:"Effective 29 February 2024, Solar Accreditation Australia (SAA) took over responsibility for the accreditation of solar installers and designers from the Clean Energy Council.",
             45:"The installation of electrical equipment in hazardous areas in Australia is primarily governed by the AS/NZS 60079 series, which operates alongside the general wiring rules in AS/NZS 3000.",
             46:"Portable electrical equipment on a worksite must be tested every 3 months if used on construction and demolition sites, or every 6 months if used in factories, workshops, and manufacturing environments.",
             47:"The required separation distance from overhead powerlines during work depends heavily on the voltage, equipment used, and local regulations, with a standard baseline of 3 metres for distribution lines up to 132kV when using a registered spotter.",
             48:"Only two types of licensed practitioners can issue a CES in Victoria: Licensed Electrical Workers (Licensed Electricians), individuals who hold an A-grade or B-grade electrical license issues by ESV. They can issue certificates for work they personally performed or supervised. And Registered Electrical Contractors (REC), businesses or individuals who hold a contractor license from ESV. A REC can issue certificates for work carried out by employees or subcontractors, provided the workers are licensed. Importantly, the person issuing the certificate must be the one who performed or directly supervised the work. A property owner, builder, or unlicensed tradesperson cannot issue a valid compliance certificate."}

# I changed some parts of the data, like Making the first letter of each data entry a capital letter and finishing with a full stop.
# I also "flattened" lists and added parentheses for nested lists, with some capitalisation fixing too.
# this also meant removing numbered points and any dot points too.
# I also removed duplicated data in the same entry as well. (30 had this problem, which is Q3 Leon)
# Number 36 seems more like legal data, so i'm unsure the way I've converted the data is right, please check over it everyone.
# Finally, I'm removing some "opens in a new window", as this is irrelevant for the RAG model.