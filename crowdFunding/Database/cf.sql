drop database CrowdFunding;
create database CrowdFunding;
use CrowdFunding;

create table location(
location_id int auto_increment primary key,
location_name varchar(255) not null unique
);

create table verifier(
verifier_id int auto_increment primary key,
verifier_name varchar(255) not null,
verifier_email varchar(255) not null unique,
verifier_phone varchar(255) not null unique,
verifier_password varchar(255) not null,
verifier_address varchar(255) not null,
location_id int,
foreign key (location_id) references location(location_id)
);

create table hospitals(
hospital_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
hospital_type varchar(255) not null,
hospital_code varchar(255) not null,
address varchar(255) not null,
status varchar(255) not null,
location_id int,
foreign key (location_id) references location(location_id)
);

create table seekers(
seeker_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
status varchar(255) not null,
location_id int,
foreign key (location_id) references location(location_id)
);

create table donor(
donor_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
location_id int,
foreign key (location_id) references location(location_id)
);

create table raise_request(
raise_request_id int auto_increment primary key,
cause varchar(255) not null,
required_amount varchar(255) not null unique,
upload_photo varchar(255) not null ,
upload_reports varchar(255) not null,
description varchar(255) not null,
status varchar(255) not null,
date varchar(255) not null,
seeker_id int,
foreign key (seeker_id) references seekers(seeker_id),
hospital_id int,
foreign key (hospital_id) references hospitals(hospital_id),
verifier_id int,
foreign key (verifier_id) references verifier(verifier_id)
);

create table bankAccount(
bankAccountt_id int auto_increment primary key,
account_number varchar(255) not null,
account_balance varchar(255) not null,
account_holder varchar(255) not null,
hospital_id int,
foreign key (hospital_id) references hospitals(hospital_id)
);

create table donations(
donations_id int auto_increment primary key,
sender varchar(255) not null,
receiver varchar(255) not null,
amount varchar(255) not null,
donation_type varchar(255) not null,
date  varchar(255) not null,
donor_id int,
foreign key (donor_id) references donor(donor_id),
raise_request_id int,
foreign key (raise_request_id) references raise_request(raise_request_id)
);
