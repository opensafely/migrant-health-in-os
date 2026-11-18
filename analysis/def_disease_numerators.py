
# A script to define the numerators for the QOF disease registers

from ehrql import INTERVAL, combine_codelists
from ehrql.tables.tpp import clinical_events

from analysis import codelists


def resolve_codelists(names):
    if names is None:
        return None

    if isinstance(names, str):
        names = [names]

    lists = [getattr(codelists, name) for name in names]

    return lists[0] if len(lists) == 1 else combine_codelists(*lists)


def build_disease_numerator(codelist, resolved_codelist=None):

    codelist = resolve_codelists(codelist)
    resolved_codelist = resolve_codelists(resolved_codelist)

    events = clinical_events.where(
        clinical_events.date.is_on_or_before(INTERVAL.end_date)
    )

    if resolved_codelist is None:
        return (
            events
            .where(events.snomedct_code.is_in(codelist))
            .exists_for_patient()
        )

    latest_diagnosis = (
        events
        .where(events.snomedct_code.is_in(codelist))
        .sort_by(events.date)
        .last_for_patient()
        .date
    )

    latest_resolved = (
        events
        .where(events.snomedct_code.is_in(resolved_codelist))
        .sort_by(events.date)
        .last_for_patient()
        .date
    )

    return (
        (latest_resolved < latest_diagnosis)
        |
        (
            latest_diagnosis.is_not_null()
            & latest_resolved.is_null()
        )
    )
