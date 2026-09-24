
from ehrql import case, when
from ehrql.tables.tpp import clinical_events, patients
import codelists

migrant_flags = {
    "any_migrant": codelists.all_migrant_codes,
    "born_in_uk": codelists.uk_cob_codes,
    "not_born_in_uk": codelists.cob_migrant_codes,
    "immig_status_excl_refugee_asylum": codelists.immigra_status_excl_ref_and_asylum_codes,
    "refugee_asylum_status": codelists.asylum_refugee_migrant_codes,
    "english_not_main_language": codelists.english_not_main_language_excl_interpreter_migrant_codes,
    "interpreter_required": codelists.interpreter_migrant_codes,
    "trafficking": codelists.trafficking_codes,
    "british_ethnicities": codelists.british_ethnicities_codes,
    "date_of_uk_entry": codelists.date_of_uk_entry
}

def build_migrant_indicators(date):

    return {
        name: (
            clinical_events
            .where(clinical_events.snomedct_code.is_in(codes))
            .where(clinical_events.date.is_on_or_between(patients.date_of_birth, date))
            .where((clinical_events.date.is_on_or_before(patients.date_of_death)) | (patients.date_of_death.is_null()))
            .exists_for_patient()
        )
        for name, codes in migrant_flags.items()
    }
   

def build_mig_status_3_cat(migrant_indicators):
    """
    3-category migrant status:
      - "Migrant" if migrant_indicators["migrant"] OR migrant_indicators["date_of_uk_entry"] is TRUE
      - "Non-migrant" if born_in_uk OR british_ethnicities AND no migrant code)
      - "Unknown" otherwise
    """
    migrant = migrant_indicators.get("any_migrant", False)
    date_of_uk_entry  = migrant_indicators.get("date_of_uk_entry", False)
    born_in_uk = migrant_indicators.get("born_in_uk", False)
    british_ethnicities = migrant_indicators.get("british_ethnicities", False)

    migrant_cond = (migrant | date_of_uk_entry) & ~born_in_uk
    non_migrant_cond = born_in_uk | ((british_ethnicities) & ~migrant_cond)

    return case(
        when(migrant_cond).then("Migrant"),
        when(non_migrant_cond).then("Non-migrant"),
        otherwise="Unknown"
    )

