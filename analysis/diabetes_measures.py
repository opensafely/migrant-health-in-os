from ehrql import create_measures, INTERVAL, years, maximum_of, minimum_of, case, when, days
from ehrql.tables.tpp import patients, practice_registrations, clinical_events, ons_deaths
import codelists 
import analysis.def_migration_status_variables as def_migration_status_variables
import analysis.def_subgroups as def_subgroups

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
    .where(clinical_events.snomedct_code.is_in(codelists.diabetes_resolved_codelist))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

diabetes_and_not_resolved = (latest_diabetes_resolved_in_interval < latest_diabetes_in_interval) | (
    latest_diabetes_in_interval.is_not_null() & latest_diabetes_resolved_in_interval.is_null())

# qof register denominator: aged 17 or older and registered on the 31st March of each year (as per QoF register)

aged_17_or_older = patients.age_on(INTERVAL.end_date) >= 17

is_alive = patients.is_alive_on(INTERVAL.end_date)

was_registered_at_year_end = (
    practice_registrations.where(practice_registrations.start_date <= INTERVAL.end_date)
    .except_where(practice_registrations.end_date < INTERVAL.end_date)
    .exists_for_patient()
)

eligible_group = aged_17_or_older & is_alive & was_registered_at_year_end

# denominator: person-time (secondary analysis)

registrations_in_interval = practice_registrations.where(
    (practice_registrations.start_date.is_on_or_before(
        INTERVAL.end_date))
    &
    (practice_registrations.end_date.is_on_or_after(
        INTERVAL.start_date)
        |
        practice_registrations.end_date.is_null())
)

## earliest registration start date within the year
registration_start = maximum_of(
    registrations_in_interval.start_date.minimum_for_patient(),
    INTERVAL.start_date
)

## latest registration end date within the year
## treat NULL end dates as extending to the end of the year
registration_end = case(
    when(
        registrations_in_interval
        .where(registrations_in_interval.end_date.is_null())
        .exists_for_patient()
    ).then(INTERVAL.end_date),
    otherwise=minimum_of(
        registrations_in_interval.end_date.maximum_for_patient(),
        INTERVAL.end_date
    )
)

## calculate registration duration in days
registration_duration = (
    registration_end - registration_start
).days + 1

# only keep registration duration for patients aged 17+
registration_duration_17plus = case(
    when(aged_17_or_older).then(registration_duration),
    otherwise=0
)

# migration grouping 

migrant_status = def_migration_status_variables.build_migrant_indicators(INTERVAL.end_date)
mig3_expr = def_migration_status_variables.build_mig_status_3_cat(migrant_status)


# run measures

measures.define_defaults(
    intervals=def_subgroups.annual_intervals,
)

## by 3-cat migrant status and age
measures.define_measure(
    name="diabetes_by_mig_status_3cat",
    denominator=eligible_group,
    numerator=diabetes_and_not_resolved,
    group_by={
        "migrant_status": mig3_expr,
        "age_band": def_subgroups.age_band
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
        name=f"diabetes_by_{safe_label}",
        denominator= migrant_eligible_group,
        numerator=diabetes_and_not_resolved
    )

## with person-time as the denominator
measures.define_measure(
    name="diabetes_by_mig_status_3cat_person_time_denom",
    denominator=registration_duration_17plus,
    numerator=diabetes_and_not_resolved,
    group_by={
        "migrant_status": mig3_expr
    }
)
