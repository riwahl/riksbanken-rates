{{ config(
    materialized= 'table',
    unique_key = 'id'
)}}

SELECT
    *
FROM {{ ref('stg_five_year_rate') }}

UNION ALL

SELECT
    *
FROM {{ ref('stg_two_year_rate') }}

UNION ALL

SELECT
    *
FROM {{ ref('stg_reference_rate') }}