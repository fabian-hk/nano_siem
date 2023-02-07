create table overwatch_diskservice
(
    id                bigint auto_increment
        primary key,
    name              longtext    not null,
    type              varchar(10) not null,
    device            longtext    not null,
    mount_point       longtext    not null,
    uuid              longtext    null,
    available         tinyint(1)  not null,
    notified          tinyint(1)  not null,
    modification_time datetime(6) not null,
    constraint overwatch_diskservice_name_type_9ea1644d_uniq
        unique (name, type) using hash
);

create index overwatch_diskservice_type_75054f5c
    on overwatch_diskservice (type);
