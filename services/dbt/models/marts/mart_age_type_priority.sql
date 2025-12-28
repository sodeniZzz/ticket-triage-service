with source_data as (
    select
        age_type,
        predicted_priority
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        age_type as group,
        predicted_priority,
        count() as count
    from source_data
    group by
        group,
        predicted_priority
)

select * from aggregated