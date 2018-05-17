import copy

Malaria_Drug_Params = {
    "Abstract": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 100,
        "Drug_Decay_T1": 10,
        "Drug_Decay_T2": 10,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 3,
        "Drug_Gametocyte02_Killrate": 0.0,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 10,
        "Drug_Vd": 1,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.25,
                "Upper_Age_In_Years": 3
            },
            {
                "Fraction_Of_Adult_Dose": 0.5,
                "Upper_Age_In_Years": 6
            },
            {
                "Fraction_Of_Adult_Dose": 0.75,
                "Upper_Age_In_Years": 10
            }
        ],
        "Max_Drug_IRBC_Kill": 4.8
    },
    "Amodiaquine": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 478,
        "Drug_Decay_T1": 2.7,
        "Drug_Decay_T2": 60,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 3,
        "Drug_Gametocyte02_Killrate": 0.0,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 0.0064,
        "Drug_Vd": 16,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.16,
                "Upper_Age_In_Years": 1
            },
            {
                "Fraction_Of_Adult_Dose": 0.2,
                "Upper_Age_In_Years": 2
            },
            {
                "Fraction_Of_Adult_Dose": 0.25,
                "Upper_Age_In_Years": 3
            },
            {
                "Fraction_Of_Adult_Dose": 0.27,
                "Upper_Age_In_Years": 4
            },
            {
                "Fraction_Of_Adult_Dose": 0.32,
                "Upper_Age_In_Years": 5
            }
        ],
        "Max_Drug_IRBC_Kill": 3.5
    },
    "Artemether": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 114,
        "Drug_Decay_T1": 0.12,
        "Drug_Decay_T2": 0.12,
        "Drug_Dose_Interval": 0.5,
        "Drug_Fulltreatment_Doses": 6,
        "Drug_Gametocyte02_Killrate": 2.5,
        "Drug_Gametocyte34_Killrate": 1.5,
        "Drug_GametocyteM_Killrate": 0.7,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 0.6,
        "Drug_Vd": 1,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.25,
                "Upper_Age_In_Years": 3
            },
            {
                "Fraction_Of_Adult_Dose": 0.5,
                "Upper_Age_In_Years": 6
            },
            {
                "Fraction_Of_Adult_Dose": 0.75,
                "Upper_Age_In_Years": 10
            }
        ],
        "Max_Drug_IRBC_Kill": 8.9
    },
    "Chloroquine": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 150,
        "Drug_Decay_T1": 8.9,
        "Drug_Decay_T2": 244,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 3,
        "Drug_Gametocyte02_Killrate": 0.0,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 150,
        "Drug_Vd": 3.9,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.17,
                "Upper_Age_In_Years": 5
            },
            {
                "Fraction_Of_Adult_Dose": 0.33,
                "Upper_Age_In_Years": 9
            },
            {
                "Fraction_Of_Adult_Dose": 0.67,
                "Upper_Age_In_Years": 14
            }
        ],
        "Max_Drug_IRBC_Kill": 4.8
    },
    "DHA": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 200,
        "Drug_Decay_T1": 0.12,
        "Drug_Decay_T2": 0.12,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 3,
        "Drug_Gametocyte02_Killrate": 2.5,
        "Drug_Gametocyte34_Killrate": 1.5,
        "Drug_GametocyteM_Killrate": 0.7,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 0.6,
        "Drug_Vd": 1,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.375,
                "Upper_Age_In_Years": 0.83
            },
            {
                "Fraction_Of_Adult_Dose": 0.5,
                "Upper_Age_In_Years": 2.83
            },
            {
                "Fraction_Of_Adult_Dose": 0.625,
                "Upper_Age_In_Years": 5.25
            },
            {
                "Fraction_Of_Adult_Dose": 0.75,
                "Upper_Age_In_Years": 7.33
            },
            {
                "Fraction_Of_Adult_Dose": 0.875,
                "Upper_Age_In_Years": 9.42
            }
        ],
        "Max_Drug_IRBC_Kill": 9.2
    },
    "Lumefantrine": {
        "Bodyweight_Exponent": 0.35,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 1017,
        "Drug_Decay_T1": 1.3,
        "Drug_Decay_T2": 2.0,
        "Drug_Dose_Interval": 0.5,
        "Drug_Fulltreatment_Doses": 6,
        "Drug_Gametocyte02_Killrate": 2.4,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 280,
        "Drug_Vd": 1.2,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.25,
                "Upper_Age_In_Years": 3
            },
            {
                "Fraction_Of_Adult_Dose": 0.5,
                "Upper_Age_In_Years": 6
            },
            {
                "Fraction_Of_Adult_Dose": 0.75,
                "Upper_Age_In_Years": 10
            }
        ],
        "Max_Drug_IRBC_Kill": 4.8
    },
    "Piperaquine": {
        "Bodyweight_Exponent": 0,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 30,
        "Drug_Decay_T1": 0.17,
        "Drug_Decay_T2": 41,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 3,
        "Drug_Gametocyte02_Killrate": 2.3,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 5,
        "Drug_Vd": 49,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.375,
                "Upper_Age_In_Years": 0.83
            },
            {
                "Fraction_Of_Adult_Dose": 0.5,
                "Upper_Age_In_Years": 2.83
            },
            {
                "Fraction_Of_Adult_Dose": 0.625,
                "Upper_Age_In_Years": 5.25
            },
            {
                "Fraction_Of_Adult_Dose": 0.75,
                "Upper_Age_In_Years": 7.33
            },
            {
                "Fraction_Of_Adult_Dose": 0.875,
                "Upper_Age_In_Years": 9.42
            }
        ],
        "Max_Drug_IRBC_Kill": 4.6
    },
    "Primaquine": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 75,
        "Drug_Decay_T1": 0.36,
        "Drug_Decay_T2": 0.36,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 1,
        "Drug_Gametocyte02_Killrate": 2.0,
        "Drug_Gametocyte34_Killrate": 5.0,
        "Drug_GametocyteM_Killrate": 50.0,
        "Drug_Hepatocyte_Killrate": 0.1,
        "Drug_PKPD_C50": 15,
        "Drug_Vd": 1,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.17,
                "Upper_Age_In_Years": 5
            },
            {
                "Fraction_Of_Adult_Dose": 0.33,
                "Upper_Age_In_Years": 9
            },
            {
                "Fraction_Of_Adult_Dose": 0.67,
                "Upper_Age_In_Years": 14
            }
        ],
        "Max_Drug_IRBC_Kill": 0.0
    },
    "Pyrimethamine": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 281,
        "Drug_Decay_T1": 3,
        "Drug_Decay_T2": 3,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 1,
        "Drug_Gametocyte02_Killrate": 0.0,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 0.24,
        "Drug_Vd": 1,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.16,
                "Upper_Age_In_Years": 1
            },
            {
                "Fraction_Of_Adult_Dose": 0.2,
                "Upper_Age_In_Years": 2
            },
            {
                "Fraction_Of_Adult_Dose": 0.25,
                "Upper_Age_In_Years": 3
            },
            {
                "Fraction_Of_Adult_Dose": 0.27,
                "Upper_Age_In_Years": 4
            },
            {
                "Fraction_Of_Adult_Dose": 0.32,
                "Upper_Age_In_Years": 5
            }
        ],
        "Max_Drug_IRBC_Kill": 3.5
    },
    "Sulfadoxine": {
        "Bodyweight_Exponent": 1,
        "Drug_Adherence_Rate": 1.0,
        "Drug_Cmax": 64,
        "Drug_Decay_T1": 7,
        "Drug_Decay_T2": 7,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 1,
        "Drug_Gametocyte02_Killrate": 0.0,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 0.62,
        "Drug_Vd": 1,
        "Fractional_Dose_By_Upper_Age": [
            {
                "Fraction_Of_Adult_Dose": 0.16,
                "Upper_Age_In_Years": 1
            },
            {
                "Fraction_Of_Adult_Dose": 0.2,
                "Upper_Age_In_Years": 2
            },
            {
                "Fraction_Of_Adult_Dose": 0.25,
                "Upper_Age_In_Years": 3
            },
            {
                "Fraction_Of_Adult_Dose": 0.27,
                "Upper_Age_In_Years": 4
            },
            {
                "Fraction_Of_Adult_Dose": 0.32,
                "Upper_Age_In_Years": 5
            }
        ],
        "Max_Drug_IRBC_Kill": 3.5
    },
    "Vehicle": {
        "Bodyweight_Exponent": 0,
        "Drug_Cmax": 10,
        "Drug_Decay_T1": 1,
        "Drug_Decay_T2": 1,
        "Drug_Dose_Interval": 1,
        "Drug_Fulltreatment_Doses": 1,
        "Drug_Gametocyte02_Killrate": 0.0,
        "Drug_Gametocyte34_Killrate": 0.0,
        "Drug_GametocyteM_Killrate": 0.0,
        "Drug_Hepatocyte_Killrate": 0.0,
        "Drug_PKPD_C50": 5,
        "Drug_Vd": 10,
        "Fractional_Dose_By_Upper_Age": [],
        "Max_Drug_IRBC_Kill": 0.0
    }
}


def update_drugs(list_drug_param, value, malaria_drug_params=Malaria_Drug_Params):
    # list_drug_param takes arguments as a list of parameter fields and the values
    if len(list_drug_param) == 1:
        malaria_drug_params[list_drug_param[0]] = value
    elif len(list_drug_param) == 2:
        malaria_drug_params[list_drug_param[0]][list_drug_param[1]] = value
    elif len(list_drug_param) == 2:
        malaria_drug_params[list_drug_param[0]][list_drug_param[1]][list_drug_param[2]] = value

    return malaria_drug_params
