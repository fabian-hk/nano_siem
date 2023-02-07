create table overwatch_networkservice
(
    id                bigint auto_increment
        primary key,
    name              longtext    not null,
    type              varchar(10) not null,
    host              longtext    not null,
    port              int         not null,
    available         tinyint(1)  not null,
    notified          tinyint(1)  not null,
    modification_time datetime(6) not null,
    constraint overwatch_networkservice_name_type_cd2d371b_uniq
        unique (name, type) using hash
);

create index overwatch_networkservice_type_c3831ae4
    on overwatch_networkservice (type);

insert into NanoSiem.overwatch_networkservice (id, name, type, host, port, available, notified, modification_time) values (17, 'Google', 'http', 'https://google.com', 0, 1, 0, '2023-02-06 20:38:02.399778');
insert into NanoSiem.overwatch_networkservice (id, name, type, host, port, available, notified, modification_time) values (18, 'Cloudflare DNS', 'tcp', '1.1.1.1', 443, 1, 0, '2023-02-06 20:38:04.425908');
insert into NanoSiem.overwatch_networkservice (id, name, type, host, port, available, notified, modification_time) values (19, 'Google DNS', 'ping', '8.8.8.8', 0, 1, 0, '2023-02-06 20:38:07.461347');
insert into NanoSiem.overwatch_networkservice (id, name, type, host, port, available, notified, modification_time) values (20, 'badssl.com', 'http', 'https://self-signed.badssl.com/', 0, 0, 1, '2023-02-06 20:38:07.772458');
