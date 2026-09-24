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


