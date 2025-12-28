with source_data as (
    select ticket_channel
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        ticket_channel,
        count() as tickets_count
    from source_data
    group by ticket_channel
)

select * from aggregated
