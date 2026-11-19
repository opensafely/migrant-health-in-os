
# A script to define the numerators for the QOF disease registers

from ehrql import INTERVAL
from ehrql.tables.tpp import clinical_events, patients

from analysis import codelists


def resolve_codelists(name):
    if name is None:
        return None

    return getattr(codelists, name)




def build_disease_numerator(
    codelist,
    resolved_codelist=None,
    diagnosis_start_date=None,
    exclusion_includes_same_day=False,
    min_age=None, # note: I have included min_age here (even though it is also in the measures.py denominator) to allow for this function to be re-usable for QOF calculations in projects that are not using the measures framework.
):

    codelist = resolve_codelists(codelist)
    resolved_codelist = resolve_codelists(resolved_codelist)

    events = clinical_events.where(
        clinical_events.date <= INTERVAL.end_date
    )

    diagnosis = events.where(
        events.snomedct_code.is_in(codelist)
    )

    if diagnosis_start_date is not None:
        diagnosis = diagnosis.where(
            diagnosis.date >= diagnosis_start_date
        )

    if resolved_codelist is None:
        numerator = diagnosis.exists_for_patient()

    else:
        resolved = events.where(
            events.snomedct_code.is_in(resolved_codelist)
        )

        latest_diagnosis = diagnosis.date.maximum_for_patient()

        if exclusion_includes_same_day:
            exclusion_after_diagnosis = resolved.where(
                resolved.date >= latest_diagnosis
            )
        else:
            exclusion_after_diagnosis = resolved.where(
                resolved.date > latest_diagnosis
            )

        numerator = (
            latest_diagnosis.is_not_null()
            & ~exclusion_after_diagnosis.exists_for_patient()
        )

    if min_age is not None:
        numerator = (
            numerator
            & (patients.age_on(INTERVAL.end_date) >= min_age)
        )

    return numerator


def build_ndh_numerator(config):

    events = clinical_events.where(
        clinical_events.date <= INTERVAL.end_date
    )

    ndh_codes = resolve_codelists(config["codelist"])
    gdm_codes = resolve_codelists(config["gdm_codelist"])
    diabetes_codes = resolve_codelists(config["diabetes_codelist"])
    resolved_codes = resolve_codelists(config["resolved_codelist"])

    qualifying_codes = ndh_codes + gdm_codes

    ndh = events.where(
        events.snomedct_code.is_in(ndh_codes)
    )

    gdm = events.where(
        events.snomedct_code.is_in(gdm_codes)
    )

    qualifying = events.where(
        events.snomedct_code.is_in(qualifying_codes)
    )

    diabetes = events.where(
        events.snomedct_code.is_in(diabetes_codes)
    )

    resolved = events.where(
        events.snomedct_code.is_in(resolved_codes)
    )

    latest_diabetes = diabetes.date.maximum_for_patient()

    latest_resolution = (
        resolved
        .where(resolved.date > latest_diabetes) # use of > aligns with the QOF definition of resolved diabetes ("the date of the latest diabetes resolved code recorded after each associated previous diabetes diagnosis")
        .date.maximum_for_patient()
    )

    no_diabetes = latest_diabetes.is_null()
    diabetes_resolved = latest_resolution.is_not_null()

    qualifying_during_interval = qualifying.where(
        qualifying.date >= INTERVAL.start_date
    )

    first_diabetes = diabetes.date.minimum_for_patient()

    qualifying_before_diabetes = (
        qualifying_during_interval
        .where(
            first_diabetes.is_null()
            | (qualifying_during_interval.date < first_diabetes)
        )
        .exists_for_patient()
    )

    latest_resolution_any = resolved.date.maximum_for_patient()

    diabetes_before_resolution = (
        diabetes
        .where(diabetes.date < latest_resolution_any)
        .date.maximum_for_patient()
    )

    qualifying_after_diabetes = (
        qualifying_during_interval
        .where(
            qualifying_during_interval.date >= diabetes_before_resolution
        )
        .exists_for_patient()
    )

    qualifying_before_start = qualifying.where(
        qualifying.date < INTERVAL.start_date
    )

    latest_diabetes_at_start = (
        diabetes
        .where(diabetes.date <= INTERVAL.start_date)
        .date.maximum_for_patient()
    )

    diabetes_at_start_resolved = (
        resolved
        .where(resolved.date > latest_diabetes_at_start)
        .exists_for_patient()
    )

    rule_1 = (
        gdm.exists_for_patient()
        |
        (
            (patients.age_on(INTERVAL.end_date) >= 18)
            & ndh.exists_for_patient()
        )
    )

    rule_2 = no_diabetes

    rule_3 = diabetes_resolved

    rule_4 = (
        qualifying_during_interval.exists_for_patient()
        &
        (
            qualifying_before_diabetes
            |
            (
                latest_resolution_any.is_not_null()
                & diabetes_before_resolution.is_not_null()
                & qualifying_after_diabetes
            )
        )
    )

    rule_5 = (
        qualifying_before_start.exists_for_patient()
        &
        (
            latest_diabetes_at_start.is_null()
            | diabetes_at_start_resolved
        )
    )

    return (
        rule_1
        &
        (
            rule_2
            | rule_3
            | rule_4
            | rule_5
        )
    )



def build_ckd_numerator(config):

    events = clinical_events.where(
        clinical_events.date <= INTERVAL.end_date
    )

    ckd_stage_3_to_5_codes = resolve_codelists(config["codelist"])
    ckd_stage_1_to_2_codes = resolve_codelists(config["ckd_1_2_codelist"])
    ckd_resolved_codes = resolve_codelists(config["resolved_codelist"])

    ckd_3_5 = events.where(
        events.snomedct_code.is_in(ckd_stage_3_to_5_codes)
    )

    ckd_1_2 = events.where(
        events.snomedct_code.is_in(ckd_stage_1_to_2_codes)
    )

    ckd_resolved = events.where(
        events.snomedct_code.is_in(ckd_resolved_codes)
    )

    latest_ckd_3_5 = (
        ckd_3_5.date.maximum_for_patient()
    )

    ckd_1_2_after_ckd_3_5 = ckd_1_2.where(
        ckd_1_2.date > latest_ckd_3_5
    )

    latest_ckd_1_2_after_ckd_3_5 = (
        ckd_1_2_after_ckd_3_5.date.maximum_for_patient()
    )

    ckd_resolved_after_ckd_3_5 = ckd_resolved.where(
        ckd_resolved.date > latest_ckd_3_5
    )

    latest_ckd_resolved_after_ckd_3_5 = (
        ckd_resolved_after_ckd_3_5.date.maximum_for_patient()
    )

    rule_1 = (
        patients.age_on(INTERVAL.end_date) >= 18
    )

    rule_2 = (
        latest_ckd_3_5.is_not_null()
        & latest_ckd_1_2_after_ckd_3_5.is_null()
        & latest_ckd_resolved_after_ckd_3_5.is_null()
    )

    return rule_1 & rule_2


def build_numerator(config):

    if config.get("numerator_type") == "custom_ndh":
        return build_ndh_numerator(config)

    if config.get("numerator_type") == "custom_ckd":
        return build_ckd_numerator(config)

    return build_disease_numerator(
    codelist=config["codelist"],
    resolved_codelist=config["resolved_codelist"],
    diagnosis_start_date=config.get("diagnosis_start_date"),
    exclusion_includes_same_day=config.get(
        "exclusion_includes_same_day", False
    ),
    min_age=config.get("min_age")
    )
