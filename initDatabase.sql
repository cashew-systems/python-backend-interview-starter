create table employees (
  id SERIAL primary key,
  name TEXT
);

create table hourly_compensations (
  id SERIAL primary key,
  employee_id INTEGER references employees(id),
  amount numeric(15,6)
);

CREATE TYPE payroll_run_status AS ENUM ('PENDING', 'COMPLETED');

create table payroll_runs (
  id SERIAL primary key,
  status payroll_run_status
);

create table payroll_run_employee_payments (
  id SERIAL primary key,
  employee_id INTEGER references employees(id),
  payroll_run_id INTEGER references payroll_runs(id),
  amount numeric(15,6)
);


insert into employees(name) values ('David');
insert into employees(name) values ('Anthony');
insert into employees(name) values ('Aman');
insert into employees(name) values ('Steve');

insert into hourly_compensations(employee_id, amount) values (1, '10.01');
insert into hourly_compensations(employee_id, amount) values (3, '30.01');
insert into hourly_compensations(employee_id, amount) values (4, '40.01');
