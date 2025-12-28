{{ config(materialized='view') }}

with source as (

    select
        ticket_id,
        predicted_priority,
        customer_age,
        customer_gender,
        product_purchased,
        ticket_type,
        ticket_channel,
        ticket_status,
        ticket_subject,
        age_type,
        days_from_purchase
    from {{ source('db_tickets', 'tickets') }}

),

renamed as (
    select
        ticket_id,
        predicted_priority,
        customer_age,
        customer_gender,
        product_purchased,
        ticket_type,
        ticket_channel,
        ticket_status,
        ticket_subject,
        age_type,
        days_from_purchase
    from source
)

select * from renamed
