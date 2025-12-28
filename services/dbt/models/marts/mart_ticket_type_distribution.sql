with source_data as (
    select ticket_type
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        ticket_type,
        count() as tickets_count
    from source_data
    group by ticket_type

)

select * from aggregated
