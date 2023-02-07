create table overwatch_diskservicelog
(
    id         bigint auto_increment
        primary key,
    timestamp  datetime(6) not null,
    available  tinyint(1)  not null,
    free_space bigint      not null,
    used_space bigint      not null,
    service_id bigint      not null,
    constraint overwatch_diskservic_service_id_ed761280_fk_overwatch
        foreign key (service_id) references overwatch_diskservice (id)
);

create index overwatch_diskservicelog_timestamp_a0509397
    on overwatch_diskservicelog (timestamp);
