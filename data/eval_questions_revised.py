eval_questions_dict = {
    "c1": {
        "known": [
            {
                "id": "c1k1",
                "question": "When can I apply to mid-scale solar installation in 2026?",
                "expected_answer": "You can apply for mid-scale solar installation from 1st of October 2026. Applications will be accepted from this date onwards.",
                "source_id": 1
            },
            {
                "id" : "c1i4",
                "question": "To install a wind turbine system what is the total annual electricity output requirement?",
                "expected_answer": "The total annual electricity output requirement to install a wind turbine system is 25 MWh.",
                "source_id": 12
            }
        ],
        "inferred": [
            {
                "id": "c1i2",
                "question": "Can my solar battery be created within 24 months of the installation?",
                "expected_answer": "No, the maximum is 12 months",
                "source_id": [17, 43, 22]
            },
            {
                "id": "c1i3",
                "question": "What if my additional new inverter has a rating of 100kW, can I install this into my house?",
                "expected_answer": "If the additional new inverter has a rating of 100kW, you cannot add it to an existing system. Adding this will increase the total system capacity 100kw for STC eligibility, which is not allowed. The maximum system capacity for STC eligibility",
                "source_id": [21, 23, 13]
            }   
        ]
    }
}