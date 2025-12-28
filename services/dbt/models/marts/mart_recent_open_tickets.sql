{{ config(materialized='view') }}

with source_data as (
    select
        *
    from {{ ref('stg_tickets') }}
),

final as (
    select *
    from source_data
    where ticket_status = 'Open'
    order by ticket_id desc
    limit 10
)

select * from final
