with source_data as (
    select predicted_priority
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        predicted_priority,
        count() as tickets_count
    from source_data
    group by predicted_priority
)

select * from aggregated
