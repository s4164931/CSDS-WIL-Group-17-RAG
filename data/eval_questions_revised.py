eval_questions_dict = {
    "c1": {
        "known": [
            {
                "id": "c1k1",
                "question": "When can I apply to mid-scale solar installation in 2026?",
                "expected_answer": "You can apply for mid-scale solar installation from 1st of October 2026. Applications will be accepted from this date onwards.",
                "source_id": 19
            },
            {
                "id" : "c1k2",
                "question": "To install a wind turbine system what is the total annual electricity output requirement?",
                "expected_answer": "The total annual electricity output requirement to install a wind turbine system is 25 MWh.",
                "source_id": 12
            },
            {
                "id": "c1k3",
                "question": "What isolation steps are required before starting installation?",
                "expected_answer": "Shut down and isolate all energy sources, lock out and tag out (LOTO), then test to verify zero voltage/energy before starting work.",
                "source_id": 42
            },
            {
                "id": "c1k4",
                "question": "What separation distance must be maintained from overhead powerlines during installation work?",
                "expected_answer": "A minimum separation distance of 3 metres must be maintained from overhead powerlines when using a registered spotter, for distribution lines up to 132 kV.",
                "source_id": 47
            }
        ],
        "inferred": [
            {
                "id": "c1i1",
                "question": "Can my solar battery be created within 24 months of the installation?",
                "expected_answer": "No, the maximum is 12 months",
                "source_id": [17, 43, 22]
            },
            {
                "id": "c1i2",
                "question": "What if my additional new inverter has a rating of 100kW, can I install this into my house?",
                "expected_answer": "If the additional new inverter has a rating of 100kW, you cannot add it to an existing system. Adding this will increase the total system capacity 100kw for STC eligibility, which is not allowed. The maximum system capacity for STC eligibility",
                "source_id": [21, 23, 13]
            },
            {
                "id": "c1i3",
                "question": "What are the most vital OH&S regulations when it comes to installing electrical equipment?",
                "expected_answer": "Electrical installation must follow OH&S requirements including risk assessment, safe isolation/lock-out and testing, appropriate electrical testing, and SWMS for high-risk work, in accordance with AS/NZS 3000.",
                "source_id": [38, 39, 40, 41, 42]
            },
        ]
    },
    "c2": {
        "known":[
            {
                "id": "c2k1",
                "question": "What are the maximum daily of installations I can do to claim STCs?",
                "expected_answer": "No more than 2 installations a day",
                "source": 3
            },
            {
                "id": "c2k2",
                "question": "Can a stackable battery system be eligible for STCs?",
                "expected_answer": "Yes. A stackable battery system can be eligible for STCs if the final configuration is on the CEC approved product list, the system is compatible and within manufacturer specifications, and the SAA-accredited installer re-certifies the complete system.",
                "source": 4 
            },
            {
                "id": "c2k3",
                "question": "Do I need to have evidence to get an STC?",
                "expected_answer": "Yes. You must have evidence proving you were on site during the 3 stages of installation. Photos are the easiest method.",
                "source": 6
            },
            {
                "id": "c2k4",
                "question": "If a household completely replaces its existing rooftop solar system, what conditions must the new system meet to be eligible for STCs?",
                "expected_answer": "The new system must be no more than 100 kW, with new panels and inverter that have had no previous STC claims, listed on the approved products list and compliant with current standards.",
                "source_id": 24 
            },
            {
                "id": "c2k5",
                "question": "Under what circumstances would a STC claim fail",
                "expected_answer": "A claim may fail if the required evidence does not show the 3 stages of installation.",
                "source_id": 33 
            }
        ],
        "inferred":[
            {
                "id": "c2i1",
                "question": "Who should be accredited for STCs?",
                "expected_answer": "The designer and installer must be accredited by Solar Accreditation Australia (SAA) for the relevant installation type to be eligible for STCs.",
                "source": [2, 17, 22]
            },
            {
                "id": "c2i2",
                "question": "What should my photos look like for evidence to get STCs?",
                "expected_answer": "Photos should clearly show your face and the 3 installation stages: setup, mid-installation and testing/commissioning. They must include date/time metadata and geolocation and match the compliance paperwork.",
                "source": [5, 30] 
            },
            {
                "id": "c2i3",
                "question": "What types of small scale renewable energy systems are eligible under the SRES?",
                "expected_answer": "Solar PV, solar batteries, wind turbines, hydro systems, solar water heaters and air-source heat pumps.",
                "source_id": [11, 26]
            },
            {
                "id": "c2i4",
                "question": "What capacity and annual electricity output limits apply to wind and hydro systems for STC eligibility?",
                "expected_answer": "The total system must be no more than 100 kW, new panels and inverter must be on the approved products list, the inverter must have sufficient capacity, all components must meet current standards and laws, and existing panels cannot be included in the new STC claim.",
                "source_id": [13, 21] 
            },
            {
                "id": "c1i5",
                "question": "What conditions must a solar PV, battery, wind or hydro system meet to be eligible for STCs?",
                "expected_answer": "The system must have STCs created within 12 months, use approved products, meet Australian/New Zealand standards, be designed and installed by appropriately accredited SAA personnel, follow SAA guidelines, comply with relevant laws and be classified as small-scale.",
                "source_id": [17, 22] 
            },
            {
                "id": "c1i6",
                "question": "How long after installation do I have to claim STCs (Small-scale Technology Certificate) for a system?",
                "expected_answer": "STCs must be created within 12 months of installation",
                "source_id": [17, 43] 
            },
        ]
    },
    "c3": {
        "known":[
            {
                "id": "c3k1",
                "question": "What are the current Australian standards for inverters?",
                "expected_answer": "The current Australian standard will be the AS/NZS 4777.2:2020 version.",
                "source_id": 1    
            },
            {
                "id": "c3k2",
                "question": "Would inverters after installation need a connection to a meter or main grid",
                "expected_answer": "For grid-connected systems, inverters don't need a connection to a meter or main grid to classify as complete.",
                "source_id": 29
            },
            {
                "id": "c3k3",
                "question": "Does Force 5S (AS4777-2 2020) come under the list of approved inverters by Clean Energy Council",
                "expected_answer": "Yes, Force 5S (AS4777-2 2020) is included in the list of approved inverters by the Clean Energy Council.",
                "source_id": 31     
            },
            {
                "id": "c3k4",
                "question": "What is the requirements for the isolation of the inverter inputs when PV is the energy source?",
                "expected_answer": "The requirement (AS/NZS 5033): Clause 4.4.1.1 requires a means to isolate PV arrays from the inverter. Clause 4.4.1.2 then provides three options that an installer may choose which would meet the requirement of the previous clause (These options are either: An adjacent and physically separate dc isolator, a dc isolator that is mechanically interlocked with a replaceable module of the inverter which allows for the removal of the module without risk of electric shock or a dc isolator located in the same external enclosure as the other components of the inverter and when in the open position, there shall be no risk of electrical hazards when any inverter external cover is removed.",
                "source_id": 36    
            }
        ],
        "inferred":[
            {
                "id": "c3i1",
                "question": "Can I apply for a new inverter to my existing system if my inverter is not on the CEC approved products list",
                "expected_answer": "For an upgrade or replacement of an existing inverter, the new inverter must be on the CEC approved products list. If it is not on the list, you cannot apply for a new inverter to your existing system.",
                "source_id": [29, 31]     
            },
        ]
    },
    "c4": {
        "known":[
            {
                "id": "c4k1",
                "question": "What requirements must products meet to connect to Australian electricity networks using CSIP-AUS?",
                "expected_answer": "To support connection to Australian electricity networks using CSIP-AUS, relevant parties must: Ensure products are certified to CSIP-AUS, Ensure products are listed with the CEC; and Pre-register and onboard to NEPKI to obtain PKI certificates for secure communications.",
                "source_id": 34
            },
            {
                "id": "c4k2",
                "question": "What tests must be performed before energising new electrical equipment/work?",
                "expected_answer": "There are five electrical tests: protective earth continuity, insulation resistance, polarity, RCD operating time, and earth fault loop impedance.",
                "source_id": 40
            },
            {
                "id": "c4k3",
                "question": "How do you verify equipment safety compliance prior to setup?",
                "expected_answer": "To Verify equipment safety compliance prior to setup requires: ensure required documentation is available and verified, and check the equipment design, electrical connections, safety checks, calibration, operating conditions, procedures, and validation instruments.",
                "source_id": 41
            },
            {
                "id": "c4k4",
                "question": "How often must portable electrical equipment on a worksite be tested?",
                "expected_answer": "Portable electrical equipment on a worksite must be tested every 3 months if used on construction and demolition sites, or every 6 months if used in factories, workshops, and manufacturing environments.",
                "source_id": 46
            },

        ],
        "inferred":[
            {
                "id": "c4i1",
                "question": "What are the necessary steps regarding Installer on-site verification photos",
                "expected_answer": "As an installer you must take: geotagged and time-stamped photos (\u2018selfies\u2019) at each phase of installation (including: job setup, mid-installation and testing and commissioning.) and a final \u2018completion\u2019 photo that matches the test date on the electrical certificate of compliance (or equivalent).",
                "source_id": [5, 30]
            },
        ]
    },
    "c5": {
        "known": [
            {
                "id": "c5k1",
                "question": "Which standard governs general electrical installations in Australia?",
                "expected_answer": "AS/NZS 3000, also known as the Australian/New Zealand Wiring Rules.",
                "source_id": 38 
            },
            {
                "id": "c5k2",
                "question": "Who accredits solar installers in Australia, CEC or SAA?",
                "expected_answer": "Solar Accreditation Australia (SAA) took over responsibility for accrediting solar installers and designers from the Clean Energy Council (CEC) on 29 February 2024.",
                "source_id": 44 
            },
            {
                "id": "c5k3",
                "question": "What Australian Standard governs the installation of electrical equipment in hazardous areas?",
                "expected_answer": "The AS/NZS 60079 series, alongside AS/NZS 3000.",
                "source_id": 45
            },
            {
                "id": "c5k4",
                "question": "Who is legally authorised to issue a Certificate of Electrical Safety?",
                "expected_answer": "Licensed Electrical Workers (A-grade or B-grade) and Registered Electrical Contractors (RECs) can issue a Certificate of Electrical Safety in Victoria, provided they meet the requirements for the work",
                "source_id": 48
            },
        ]
    },
    "c6": {
        "known":[
            {
                "id": "c6k1",
                "question": "What is the renewable energy target?",
                "expected_answer": "The Renewable Energy Target (RET) is an Australian Government scheme that aims to reduce greenhouse gas emissions and increase renewable electricity generation, with a target of 33,000 GWh of additional renewable electricity each year from 2020 to 2030.",
                "source_id": 7 
            },
            {
                "id": "c6k2",
                "question": "How does the RET work?",
                "expected_answer": "The RET creates tradable renewable energy certificates, with each certificate representing one MWh of renewable electricity generated or displaced, which liable entities must purchase and surrender.",
                "source_id": 10 
            },
            {
                "id": "c6k3",
                "question": "What is the difference between a small scale system and a power station under the Renewable Energy Target?",
                "expected_answer": "Small-scale systems are classified based on system capacity, while systems with higher generation capacity are classified as power stations under the LRET.",
                "source_id": 15 
            },          
        ],
        "inferred":[
            {
                "id": "c6i1",
                "question": "What requirements must a power station meet under the Renewable Energy Target?",
                "expected_answer": "Power stations must apply for accreditation, meet the eligibility requirements and maintain ongoing accreditation and compliance obligations.",
                "source_id":[16, 27]
            },           
        ]
    },
    "c7": {
        "known":[
            {
                "id": "c7k1",
                "question": "What are Postcode zones?",
                "expected_answer": "Postcode zones are factors used to calculate the number of renewable energy certificates a solar PV system may be eligible for after installation",
                "source_id": 8 
            },
            {
                "id": "c7k2",
                "question": "What does each postcode zone represent?",
                "expected_answer": "Each postcode zone represents the level of solar radiation for a geographical area.",
                "source_id": 9 
            },
            {
                "id": "c7k3",
                "question": "Is usage of the new AS/NZS 5033:2021 before the commencement date practical/viable/allowed?",
                "expected_answer": "Yes. The 2021 edition may be used prior to the commencement date.",
                "source_id": 37 
            },
        ],
        "inferred": [
            {
                "id": "c7i1",
                "question": "How do you define a small-scale system?",
                "expected_answer": "A small-scale system is classified based on its system capacity.",
                "source_id": [11, 15, 26] 
            }
        ]
    },
    "c8": {
        "known":[
            {
                "id": "c8k1",
                "question": "What deeming period applies to a solar PV system installed in 2024?",
                "expected_answer": "For systems installed in 2024, the maximum deeming period is 7 years.",
                "source_id": 19
            },
            {
                "id": "c8k2",
                "question": "Can I apply to a rebate to switch to solar?",
                "expected_answer": "Solar Victoria offers rebates and interest-free loans to support eligible households to switch to solar, including: A $1,400 rebate and interest-free loan to install rooftop solar panels (PV) on a home or rental property.",
                "source_id": 20
            },                      
            {
                "id": "c8k3",
                "question": "Under what circumstances can multiple installers work on the same solar installation?",
                "expected_answer": "There can be multiple installers on an installation if: multiple installers are needed throughout, an installer can't complete the whole installation or the job is handed over from one installer to another.",
                "source_id": 32
            }            
        ],
        "inferred":[
            {
                "id": "c8i1",
                "question": "What do I need to keep in mind when replacing my original rooftop solar system",
                "expected_answer": "When replacing your original rooftop solar system, you need to ensure that the new system meets the eligibility requirements for STCs, including being no more than 100 kW, using new panels and inverter that have had no previous STC claims, being listed on the approved products list, and complying with current standards. STCs can only be claimed if the certificates are created within 12 months of installation.",
                "source_id":[24, 43]
            },           
        ]
    }
}

out_of_scope_dict = {
        "o1": "What is the current price of an STC?",
        "o2": "How much does it cost to install a solar battery?",
        "o3": "What brand of solar panel is the most reliable?",
        "o4": "How much electricity will my solar system generate each year?",
        "o5": "What is the best solar battery for my home?",
        "o6": "How much money can I save by installing solar panels?"
}