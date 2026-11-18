# A script with a dictionary of the required information to create the QOF condition registers 

DISEASES = {
    "chd": {
        "codelist": "chd_codelist",
        "resolved_codelist": None,
        "min_age": None,
        "output_name": "coronary_heart_disease",
    },
    "diabetes": {
        "codelist": "diabetes_codelist",
        "resolved_codelist": "diabetes_resolved_codelist",
        "min_age": 17,
        "output_name": "diabetes",
    },
    "af": {
        "codelist": "af_codelist",
        "resolved_codelist": "af_resolved_codelist",
        "min_age": None,
        "output_name": "atrial_fibrillation",
    },
    "hf": {
        "codelist": "hf_codelist",
        "resolved_codelist": "hf_resolved_codelist",
        "min_age": None,
        "output_name": "heart_failure",
    },
    "hyp": {
        "codelist": "hyp_codelist",
        "resolved_codelist": "hyp_resolved_codelist",
        "min_age": None,
        "output_name": "hypertension",
    },
    "stroke": {
        "codelist": "stroke_tia_codelist",
        "resolved_codelist": None,
        "min_age": None,
        "output_name": "stroke",
    },
    "ndh": {
        "numerator_type": "custom_ndh",
        "codelist": "ndh_combined_codelist",
        "gdm_codelist": "gestational_diabetes_codelist",
        "diabetes_codelist": "diabetes_codelist",
        "resolved_codelist": "diabetes_resolved_codelist",
        "min_age": None,
        "output_name": "non_diabetic_hyperglycaemia",
    },
}