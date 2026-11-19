from ehrql import codelist_from_csv

# QOF - codelists for registries 

diabetes_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
    category_column="term"
)
diabetes_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code",
    category_column="term"
)

af_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-afib_cod.csv",
    column="code",
    category_column="term"
)

af_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-afibres_cod.csv",
    column="code",
    category_column="term"
)

chd_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-chd_cod.csv",
    column="code",
    category_column="term"
)

hf_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hf_cod.csv",
    column="code",
    category_column="term"
)

hf_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hfres_cod.csv",
    column="code",
    category_column="term"
)

hyp_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
    column="code",
    category_column="term"
)

hyp_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hypres_cod.csv",
    column="code",
    category_column="term"
)

stroke_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-strk_cod.csv",
    column="code"
)

tia_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-tia_cod.csv",
    column="code"
)

stroke_tia_codelist = stroke_codelist + tia_codelist

ndh_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ndh_cod.csv",
    column="code"
) 

igt_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-igt_cod.csv",
    column="code"
)

gestational_diabetes_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-gestdiab_cod.csv",
    column="code"
)   

prediabetes_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-prd_cod.csv",
    column="code"
)

ndh_combined_codelist = (
    ndh_codelist
    + prediabetes_codelist
    + igt_codelist
)

asthma_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ast_cod.csv",
    column="code"
)

dementia_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dem_cod.csv",
    column="code"
)

cancer_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-can_cod.csv",
    column="code"
)   

ckd_stage_3_to_5_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ckd_cod.csv",
    column="code"
)

ckd_stage_1_to_2_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ckd1and2_cod.csv",
    column="code"
)

ckd_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ckdres_cod.csv",
    column="code"
)   

depression_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-depr_cod.csv",
    column="code"
)

depression_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-depres_cod.csv",
    column="code"
)

epilepsy_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-epil_cod.csv",
    column="code"
)   

epilepsy_resolved_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-epilres_cod.csv",
    column="code"
)   

learning_disability_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ld_cod.csv",
    column="code"
)

learning_disability_exclusion_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ldrem_cod.csv",
    column="code"
)

rheumatoid_arthritis_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-rarth_cod.csv",
    column="code"
)

# Migration codelists

all_migrant_codes = codelist_from_csv(
    "codelists/opensafely-migration-status.csv", 
    column="code")

uk_cob_codes = codelist_from_csv(
    "codelists/opensafely-born-in-the-uk.csv", 
    column="code")

cob_migrant_codes = codelist_from_csv(
    "codelists/opensafely-born-outside-the-uk.csv", 
    column="code")

immigra_status_excl_ref_and_asylum_codes = codelist_from_csv(
    "codelists/opensafely-immigration-status-excl-refugee-asylum.csv", 
    column="code")

asylum_refugee_migrant_codes = codelist_from_csv(
    "codelists/opensafely-asylum-or-refugee-status.csv", 
    column="code")

english_not_main_language_excl_interpreter_migrant_codes = codelist_from_csv(
    "codelists/opensafely-english-not-main-language.csv", 
    column="code")

interpreter_migrant_codes = codelist_from_csv(
    "codelists/opensafely-interpreter-required.csv", 
    column="code")

trafficking_codes = codelist_from_csv(
    "codelists/opensafely-trafficking-and-modern-slavery.csv", 
    column="code")

british_ethnicities_codes = codelist_from_csv(
    "codelists/opensafely-british-ethnicities.csv", 
    column="code")

date_of_uk_entry = codelist_from_csv(
    "codelists/opensafely-date-of-uk-entry.csv", 
    column="code")


