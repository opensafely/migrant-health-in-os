
from ehrql import INTERVAL, maximum_of, minimum_of, case, when

from ehrql.tables.tpp import patients, practice_registrations, ons_deaths

def build_common_population():

    date_of_death = case(
        when(
            patients.date_of_death.is_not_null()
            & ons_deaths.date.is_not_null()
            & (patients.date_of_death <= ons_deaths.date)
        ).then(patients.date_of_death),

        when(
            patients.date_of_death.is_not_null()
            & ons_deaths.date.is_not_null()
            & (ons_deaths.date < patients.date_of_death)
        ).then(ons_deaths.date),

        when(
            patients.date_of_death.is_not_null()
        ).then(patients.date_of_death),

        when(
            ons_deaths.date.is_not_null()
        ).then(ons_deaths.date)
    )

    is_alive = (
        date_of_death.is_null()
        | (date_of_death > INTERVAL.end_date)
    )

    was_registered_at_year_end = (
        practice_registrations
        .where(
            practice_registrations.start_date
            <= INTERVAL.end_date
        )
        .except_where(
            practice_registrations.end_date
            < INTERVAL.end_date
        )
        .exists_for_patient()
    )

    eligible_group = (
        is_alive & was_registered_at_year_end
    )

    registrations_in_interval = (
        practice_registrations
        .where(
            (
                practice_registrations.start_date
                .is_on_or_before(INTERVAL.end_date)
            )
            &
            (
                practice_registrations.end_date
                .is_on_or_after(INTERVAL.start_date)
                |
                practice_registrations.end_date.is_null()
            )
        )
    )

    registration_start = maximum_of(
        registrations_in_interval
        .start_date.minimum_for_patient(),
        INTERVAL.start_date
    )

    registration_end = case(
        when(
            registrations_in_interval
            .where(
                registrations_in_interval.end_date.is_null()
            )
            .exists_for_patient()
        ).then(INTERVAL.end_date),
        otherwise=minimum_of(
            registrations_in_interval
            .end_date.maximum_for_patient(),
            INTERVAL.end_date
        )
    )

    registration_duration = (
        registration_end - registration_start
    ).days + 1

    return eligible_group, registration_duration


def apply_age_restriction(
    eligible_group,
    registration_duration,
    min_age=None,
    max_age=None,
):

    if min_age is None and max_age is None:
        return eligible_group, registration_duration

    age = patients.age_on(INTERVAL.end_date)

    if min_age is not None:
        age_eligible = age >= min_age
    else:
        age_eligible = age <= max_age

    if max_age is not None:
        age_eligible = age_eligible & (age <= max_age)

    eligible_group = eligible_group & age_eligible

    registration_duration = case(
        when(age_eligible).then(registration_duration),
        otherwise=0
    )

    return eligible_group, registration_duration