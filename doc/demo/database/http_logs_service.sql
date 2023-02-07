create table http_logs_service
(
    id                bigint auto_increment
        primary key,
    name              longtext    not null,
    type              varchar(40) not null,
    log_position      bigint      not null,
    log_path          longtext    not null,
    modification_time datetime(6) not null,
    running           tinyint(1)  not null,
    constraint web_service_name_d1ae3bf6_uniq
        unique (name) using hash
);

create index http_logs_service_type_60491304
    on http_logs_service (type);
insert into NanoSiem.http_logs_service (id, name, type, log_position, log_path, modification_time, running) values (38, 'Traefik', 'traefik', 2000, '/var/log/access.log', '2022-12-12 00:47:13.287344', 0);
