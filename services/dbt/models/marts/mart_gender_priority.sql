with source_data as (
    select
        customer_gender,
        predicted_priority
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        customer_gender as group,
        predicted_priority,
        count() as count
    from source_data
    group by
        group,
        predicted_priority
)

select * from aggregated
