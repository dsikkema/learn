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
limit 15;

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
    customer_row_num <= 5
limit 15
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
    customer_row_num <= 5
limit 15
;

select 'use LEAD() - get, for each rental, the next time the customer made a rental. 
Put that into a CTE so that it can be used without redundant recalculation (remember, 
aliases aren''t available yet) to compute the time it took after this rental in order
to make the next.';

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
    next_rental - rental_date as time_till_next_rental
from
    rentals_with_next
order by
    rental_date
limit 15;

