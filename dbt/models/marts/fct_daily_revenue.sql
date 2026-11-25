select
    date_trunc('day', updated_at) as revenue_date,
    sum(amount) as revenue
from {{ ref('stg_orders') }}
group by 1
