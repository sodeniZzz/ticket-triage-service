with source_data as (
    select
        product_purchased,
        predicted_priority
    from {{ ref('stg_tickets') }}
),

aggregated as (
    select
        product_purchased,
        count() as tickets_count,
        countIf(predicted_priority = 'Critical') as critical_count,
        critical_count / tickets_count as critical_rate
    from source_data
    group by product_purchased
),

final as (
    select *
    from aggregated
    where tickets_count >= 10
    order by critical_rate desc, tickets_count desc
    limit 10
)

select * from final
