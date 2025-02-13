select '
Here are two methods for doing the same thing: using a select statement to run
a window function that computes a running average, and then, in a different
select statement (to avoid recalculation), doing a computation against that
running average (in this case, determine if a payment amount is more than double the
running avg)
';

select 'First method: subquery';
explain
select
    customer_id,
    payment_date,
    amount,
    round(running_avg::numeric, 2) as running_avg,
    amount > 2 * running_avg as is_anomaly
from (
        select 
            customer_id,
            payment_date,
            amount,
            avg(amount) over (
                partition by customer_id 
                order by payment_date 
                rows between 3 preceding and 1 preceding
            ) as running_avg
        from 
            payment
    ) subquery
where 
    customer_id in (100, 101, 102)
order by
    payment_date desc
limit 15;

select 'second method: CTE';
explain analyze
with payments_with_running_avg as (
    select 
        customer_id,
        payment_date,
        amount,
        avg(amount) over (
            partition by customer_id 
            order by payment_date 
            rows between 3 preceding and 1 preceding
        ) as running_avg
    from 
        payment
)
select
    customer_id,
    payment_date,
    amount,
    round(running_avg::numeric, 2) as running_avg,
    amount > 2 * running_avg as is_anomaly
from
    payments_with_running_avg
where 
    customer_id in (100, 101, 102)
order by 
    payment_date desc
limit 15;
