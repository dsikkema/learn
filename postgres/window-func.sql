select 'Get count of rentals by store and month, along with a 
running total over all the months for that store.';

select
    DATE_TRUNC('month', r.rental_date) as rental_month,
    i.store_id,
    count(*) as monthly_rentals,
    /*
     below, the reference to count(*) is the equivalent of referencing the alias
     monthly_rentals, except of course that that's not allowed: window functions
     run before SELECT and therefore before aliases are available. But count(*)
     itself is computed during GROUP BY execution.
    
     Hence, we have this logic: count(*) gets, for each (grouped) rows, the 
     number of rentals for that month (monthly_rentals). Because there's a partitition by store ID,
     we'll sum() monthly_rentals for that given store ID. But, because we have "order by",
     the window function only includes rows up to and including the "current" row (an
     ordering relation is defined that makes it coherent to consider some rows to be
     "before" or "after" a given row.)
    
     That's why it's a running total by month.
    */
    sum(count(*)) over (
        partition by i.store_id order by date_trunc('month', r.rental_date)
    ) as running_total

from rental r
join inventory i on r.inventory_id = i.inventory_id
group by date_trunc('month', r.rental_date), i.store_id
order by i.store_id, rental_month;

select 'more basic example: number the rentals from 1, ordered by date';
select 
    rental_date,
    row_number() over (
        order by rental_date
    ) as rental_number
from rental
limit 5;

select 'now the same, but number rentals by store as well as by overall.
Can see that the overall rental number is different from the order by 
store, and when the first rental is made at each respective store, the
count starts from 1 for that store';

select 
    rental_date,
    i.store_id,
    row_number() over (
        partition by i.store_id order by rental_date
    ) as rental_number_by_store,
    row_number() over (
        order by rental_date
    ) as rental_number_overall,
    row_number() over (
        partition by i.store_id -- order by not given, row_number() is unpredictable
    ) as who_knows_what
from rental r
join inventory i on r.inventory_id = i.inventory_id
order by rental_number_overall
limit 7;

select 'for payments: select payment amounts, compared against the average amout
of a payment made by that customer (averaged over all payments from that customer).
 Use a CTE so that result of the row_number()
window function can be used to limit output into something manageable by showing
only a few rows per customer, and thereby seeing the different results for different
cusomters even with LIMIT 15 at the end.';

with numbered_rows as (
    select 
        customer_id,
        amount,
        avg(amount) over (
            -- No order by clause - this means the window function computes over
            -- the entire partition, not up to the "current row"
            partition by customer_id 
        ),
        row_number() over (
            -- row_number() always returns the current row and thus, in a sense,
            -- requires there to *be* a current row, which means some kind of 
            -- ordering is necessary. If you omit order by clause here, postgres
            -- kind of comes up with some sort of ordering, but it's best practice
            -- to supply it
            partition by customer_id order by payment_date
        ) as customer_row_num
    from
        payment
)
select 
    *
from 
    numbered_rows
WHERE
    customer_row_num <= 3
limit 7
;

select 'same as above, except with the addition of an order by clause
to the avg() window: this causes avg() to be computed not over all payments
by the customer, but over all up to that point in time: in other words, running
average till now.';


with numbered_rows as (
    select 
        customer_id,
        amount,
        avg(amount) over (
            partition by customer_id order by payment_date
        ),
        row_number() over (
            partition by customer_id order by payment_date
        ) as customer_row_num
    from
        payment
)
select 
    *
from 
    numbered_rows
WHERE
    customer_row_num <= 3
limit 7
;

select 'LEAD basic: get row ahead, or N rows ahead';

select 
    customer_id,
    rental_date,
    LEAD(rental_date) over (
        partition by customer_id order by rental_date
    ) as next_rental_date,
    LEAD(rental_date, 2) over (
        partition by customer_id order by rental_date
    ) as the_rental_after_next_date
from 
    rental
where 
    customer_id in (100, 101, 102)
order by
    rental_date
limit 10;

select 'use LEAD() - get, for each rental, the next time the customer made a rental. 
Put that into a CTE so that it can be used without redundant recalculation (remember, 
aliases aren''t available yet) to compute the time it took after this rental in order
to make the next.

LEAD essentially just looks at which row comes after.
';

with rentals_with_next as (
    select 
        customer_id,
        rental_date,
        LEAD(rental_date) over (
            partition by customer_id order by rental_date
        ) as next_rental
    from 
        rental
) select 
    *,
    /**
     * This works because NULL - datetime produces NULL, but the next
     * example will show explicitly handling the NULL case.
     */
    next_rental - rental_date as time_till_next_rental
from
    rentals_with_next
order by
    rental_date 
limit 5;

select 'Now, we''ll do the same thing except ordering the result
set in descending order by rental_date to show what happens when 
there is no next row: what is LEAD() for the last row in a partition?
It produces NULL for the asked-fow column.';

with rentals_with_next as (
    select 
        customer_id,
        rental_date,
        LEAD(rental_date) over (
            partition by customer_id order by rental_date
        ) as next_rental
    from 
        rental
) select 
    *,
    /**
     * Strictly speaking the below unnecessary: NULL-datetime produces NULL,
     * but this just shows how to explicitly handle these things.
     */
    CASE
        when next_rental is null then null
        else next_rental - rental_date
    END as time_till_next_rental
from
    rentals_with_next
order by
    rental_date desc
limit 10;

select 'Now let''s look at LAG() - the same, but for the previous row.
Find payment amount along with the previous payment amount for each customer.

Also ordering result set descending because the initial payments
don''t have previous payments so they render as null';

select
    customer_id,
    payment_date,
    amount,
    LAG(amount) over (
        partition by customer_id order by payment_date
    ) as prev_payment
from 
    payment
order by
    payment_date desc
limit 10;

select 'By the way, here''s how to use coalesce to default null values. 
Same as above but order ascending to handle nulls. We''ll need to convert the 
previous payment to a string so it''s a consistent datatype no matter what';

select
    customer_id,
    payment_date,
    amount,
    coalesce(
        LAG(amount) over (
            partition by customer_id order by payment_date
        )::varchar, -- convert 'numberic' type to 'varchar'
        'n/a (first payment)' -- alternately, but less sensibly, we could default this to a numeric like 0
    ) as prev_payment
from 
    payment
order by
    payment_date asc -- asc is default anyway, just showing it explicitly
limit 10;

select 'anomaly detecting: detect whether the payment amount for a rental
is more than double the running average for that customer over their 3 most 
recent rentals.

Use ROWS BETWEEN to establish a sliding window, not just from the beginning
until current, and not just "all the rows", but arbitrary: X rows before and 
Y rows after

use a subquery this time rather than CTE';

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

/**
* Note: there are also FIRST_VALUE/LAST_VALUE window functions with return
* first and last value in the window.
* 
* Other interesting ones to touch on later include:
* RANK/DENSE_RANK
* NTILE
**/