select 'Get count of rentals by store and month, along with a 
running total over all the months for that store.';
select
    DATE_TRUNC('month', r.rental_date) as rental_month,
    i.store_id,
    count(*) as monthly_rentals,
    sum(count(*)) over (
        partition by i.store_id order by date_trunc('month', r.rental_date)
    ) as running_total

from rental r
join inventory i on r.inventory_id = i.inventory_id
group by date_trunc('month', r.rental_date), i.store_id
order by i.store_id, rental_month;


