from ehrql import create_measures, INTERVAL, years
from ehrql.tables.tpp import patients, practice_registrations, clinical_events
import codelists 
import migration_status_variables

measures = create_measures()
measures.configure_dummy_data(population_size=1000)
measures.configure_disclosure_control(enabled=False)  # enable on real data

# numerator

events_in_interval = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

latest_diabetes_in_interval = (
    events_in_interval
    .where(
        clinical_events.snomedct_code.is_in(
            codelists.diabetes_codelist
        )
    )
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

latest_diabetes_resolved_in_interval = (
    events_in_interval
    .where(clinical_events.snomedct_code.is_in(codelists.diabetes_resolved_codelist
                                               ))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

diabetes_and_not_resolved = (latest_diabetes_resolved_in_interval < latest_diabetes_in_interval) | (
    latest_diabetes_in_interval.is_not_null() & latest_diabetes_resolved_in_interval.is_null())

# denominator

aged_17_or_older = patients.age_on(INTERVAL.end_date) >= 17

is_alive = patients.is_alive_on(INTERVAL.end_date)

was_registered_at_any_point_during_interval = practice_registrations.where(
    practice_registrations.start_date.is_on_or_before(INTERVAL.end_date)
    &
    (
        practice_registrations.end_date.is_on_or_after(INTERVAL.start_date)
        |
        practice_registrations.end_date.is_null()
    )
).exists_for_patient()

eligible_group = aged_17_or_older & is_alive & was_registered_at_any_point_during_interval

# grouping 

migrant_status = migration_status_variables.build_migrant_indicators(INTERVAL.end_date)
mig3_expr = migration_status_variables.build_mig_status_3_cat(migrant_status)

# measure

measures.define_defaults(
    intervals=years(17).starting_on("2009-04-01"),
)

## by 3-cat migrant status
measures.define_measure(
    name="diabetes_by_mig_status_3cat",
    denominator=eligible_group,
    numerator=diabetes_and_not_resolved,
    group_by={
        "migrant_status": mig3_expr
    }
)

## overall
measures.define_measure(
    name="diabetes_overall",
    denominator= eligible_group,
    numerator=diabetes_and_not_resolved
)

## individual migrant statuses

for key, expr in migrant_status.items():
    safe_label = (
        key.lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    migrant_eligible_group = eligible_group & expr

    measures.define_measure(
        name=f"{safe_label}",
        denominator= migrant_eligible_group,
        numerator=diabetes_and_not_resolved
    )