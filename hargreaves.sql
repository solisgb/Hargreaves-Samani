select e.c_clima , round(st_y(st_transform(e.geom, 4326))::numeric, 0) latitud, t.fh_medida , t.tmax , t.tmin , (t.tmax + t.tmin)*0.5 tavg 
from met.cl_est_climat e
	left join met.cl_temper_diaria t using (c_clima)
where t.fh_medida > '1985-01-01' and t.fh_medida < '2015-01-01'
order by e.c_clima , st_y(e.geom), t.fh_medida;

create table met.r0 (
	lat integer,
	r01 float4,
	r02 float4,
	r03 float4,
	r04 float4,
	r05 float4,
	r06 float4,
	r07 float4,
	r08 float4,
	r09 float4,
	r10 float4,
	r11 float4,
	r12 float4,
	primary key (lat)
	);

update r0 set r0=0.0 where r0<0;

select * from r0 order by lat, "month";