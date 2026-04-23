with filtered as (
    select
        a.appointment_id,
        a.patient_id,
        a.clinic_id,
        c.clinic_name,
        a.appointment_date,
        coalesce(a.total_amount, 0) as total_amount
    from appointments a
    join clinics c on c.clinic_id = a.clinic_id
    where a.status = 'completed'
),
dedup as 
(
    select * from 
    (
        select 
        	*, row_number() over (partition by patient_id, clinic_id, appointment_date order by total_amount desc nulls last) as rn 
        from filtered
    )
    where rn = 1
),
with_month as 
(
    select
        *,
        date_trunc('month', appointment_date)::date as month
    from dedup
),
first_visit as 
(
    select
        patient_id,
        clinic_id,
        min(appointment_date) as first_visit_date
    from dedup
    group by 1,2
),
result as 
(
    select
        w.clinic_name,
        w.month,
        count(1) as total_completed_visits,
        count(distinct w.patient_id) as unique_patients,
        count(distinct case 
            when w.appointment_date = f.first_visit_date then w.patient_id 
        end) as first_time_patients,
        sum(w.total_amount) as total_revenue
    from with_month w
    join first_visit f
        on w.patient_id = f.patient_id
       and w.clinic_id = f.clinic_id
    group by 1,2
)
select
    clinic_name,
    month,
    total_completed_visits,
    unique_patients,
    first_time_patients,
    (unique_patients - first_time_patients) as returning_patients,
    round((unique_patients - first_time_patients) * 100.0 / nullif(unique_patients, 0), 2) as retention_rate_pct,
    total_revenue
from result
order by clinic_name, month
