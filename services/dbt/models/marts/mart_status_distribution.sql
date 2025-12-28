with source_data as (
    select ticket_status
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        ticket_status,
        count() as tickets_count
    from source_data
    group by ticket_status
)

select * from aggregated
