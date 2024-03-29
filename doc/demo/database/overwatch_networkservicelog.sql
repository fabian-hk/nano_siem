create table overwatch_networkservicelog
(
    id         bigint auto_increment
        primary key,
    timestamp  datetime(6) not null,
    latency    double      not null,
    service_id bigint      not null,
    constraint overwatch_networkser_service_id_d23d38ff_fk_overwatch
        foreign key (service_id) references overwatch_networkservice (id)
);

create index overwatch_networkservicelog_timestamp_859e9a4d
    on overwatch_networkservicelog (timestamp);

insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (307, '2023-02-06 19:45:01.369425', 212.719, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (308, '2023-02-06 19:45:03.387840', 13.023014, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (309, '2023-02-06 19:45:06.423044', 17.863, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (310, '2023-02-06 19:45:06.742231', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (311, '2023-02-06 19:46:02.166168', 157.93699999999998, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (312, '2023-02-06 19:46:04.190843', 13.754138, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (313, '2023-02-06 19:46:07.219727', 19.327, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (314, '2023-02-06 19:46:07.541313', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (315, '2023-02-06 19:47:02.512441', 146.966, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (316, '2023-02-06 19:47:04.533185', 13.103335, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (317, '2023-02-06 19:47:07.559732', 18.29, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (318, '2023-02-06 19:47:07.884876', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (319, '2023-02-06 19:48:02.906541', 161.159, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (320, '2023-02-06 19:48:04.928158', 12.935117, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (321, '2023-02-06 19:48:07.962795', 18.212, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (322, '2023-02-06 19:48:08.309730', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (323, '2023-02-06 19:49:02.324886', 156.752, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (324, '2023-02-06 19:49:04.344812', 13.6328, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (325, '2023-02-06 19:49:07.378305', 17.737, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (326, '2023-02-06 19:49:07.691256', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (327, '2023-02-06 19:50:02.673893', 147.168, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (328, '2023-02-06 19:50:04.693304', 12.749275, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (329, '2023-02-06 19:50:07.722070', 21.584, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (330, '2023-02-06 19:50:08.042841', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (331, '2023-02-06 19:51:02.035678', 170.626, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (332, '2023-02-06 19:51:04.062642', 12.637014, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (333, '2023-02-06 19:51:07.096312', 20.192, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (334, '2023-02-06 19:51:07.414403', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (335, '2023-02-06 19:52:02.476387', 149.551, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (336, '2023-02-06 19:52:04.502796', 12.781886, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (337, '2023-02-06 19:52:07.536750', 18.609, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (338, '2023-02-06 19:52:07.860251', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (339, '2023-02-06 19:53:02.850808', 164.202, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (340, '2023-02-06 19:53:04.872318', 12.878674, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (341, '2023-02-06 19:53:07.904183', 18.501, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (342, '2023-02-06 19:53:08.253701', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (343, '2023-02-06 19:54:02.270998', 159.139, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (344, '2023-02-06 19:54:04.299695', 14.371202, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (345, '2023-02-06 19:54:07.328378', 20.793, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (346, '2023-02-06 19:54:07.651853', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (347, '2023-02-06 19:55:02.673548', 148.367, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (348, '2023-02-06 19:55:04.696885', 15.84901, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (349, '2023-02-06 19:55:07.724633', 18.183, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (350, '2023-02-06 19:55:08.045576', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (351, '2023-02-06 19:56:02.010055', 139.817, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (352, '2023-02-06 19:56:04.029041', 13.167497, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (353, '2023-02-06 19:56:07.062631', 18.896, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (354, '2023-02-06 19:56:07.382871', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (355, '2023-02-06 19:57:02.366016', 161.005, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (356, '2023-02-06 19:57:04.392689', 14.715684, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (357, '2023-02-06 19:57:07.435209', 19.831, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (358, '2023-02-06 19:57:07.761424', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (359, '2023-02-06 19:58:02.740357', 151.018, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (360, '2023-02-06 19:58:04.766080', 12.426753, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (361, '2023-02-06 19:58:07.801664', 19.281, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (362, '2023-02-06 19:58:08.185418', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (363, '2023-02-06 19:59:02.131398', 136.27800000000002, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (364, '2023-02-06 19:59:04.152896', 15.295106, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (365, '2023-02-06 19:59:07.180784', 18.668, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (366, '2023-02-06 19:59:07.512253', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (367, '2023-02-06 20:00:02.501897', 148.16199999999998, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (368, '2023-02-06 20:00:04.530607', 13.607108, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (369, '2023-02-06 20:00:07.559885', 18.27, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (370, '2023-02-06 20:00:07.878306', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (371, '2023-02-06 20:01:02.821476', 140.934, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (372, '2023-02-06 20:01:04.848060', 12.14523, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (373, '2023-02-06 20:01:07.887137', 19.547, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (374, '2023-02-06 20:01:08.205643', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (375, '2023-02-06 20:02:02.208116', 163.148, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (376, '2023-02-06 20:02:04.235597', 13.382467, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (377, '2023-02-06 20:02:07.266615', 22.508, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (378, '2023-02-06 20:02:07.601539', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (379, '2023-02-06 20:03:03.382420', 940.25, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (380, '2023-02-06 20:03:05.413052', 21.024405, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (381, '2023-02-06 20:03:08.448277', 18.927, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (382, '2023-02-06 20:03:33.480770', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (383, '2023-02-06 20:04:02.496378', 159.31300000000002, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (384, '2023-02-06 20:04:04.522405', 12.359371, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (385, '2023-02-06 20:04:07.550931', 18.506, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (386, '2023-02-06 20:04:07.879924', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (387, '2023-02-06 20:05:02.880655', 165.25500000000002, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (388, '2023-02-06 20:05:04.908563', 13.710328, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (389, '2023-02-06 20:05:07.938273', 18.92, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (390, '2023-02-06 20:05:08.253532', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (391, '2023-02-06 20:06:02.236527', 141.259, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (392, '2023-02-06 20:06:04.256795', 13.002434, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (393, '2023-02-06 20:06:07.285608', 21.248, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (394, '2023-02-06 20:06:07.613173', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (395, '2023-02-06 20:07:02.661162', 198.789, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (396, '2023-02-06 20:07:04.686774', 11.972459, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (397, '2023-02-06 20:07:07.720998', 18.986, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (398, '2023-02-06 20:07:08.041318', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (399, '2023-02-06 20:08:01.973866', 132.646, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (400, '2023-02-06 20:08:03.994104', 13.075856, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (401, '2023-02-06 20:08:07.028761', 18.196, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (402, '2023-02-06 20:08:07.342993', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (403, '2023-02-06 20:09:02.345243', 146.767, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (404, '2023-02-06 20:09:04.376050', 22.399562, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (405, '2023-02-06 20:09:07.404904', 17.577, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (406, '2023-02-06 20:09:07.776322', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (407, '2023-02-06 20:10:02.774877', 162.75300000000001, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (408, '2023-02-06 20:10:04.800623', 12.18305, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (409, '2023-02-06 20:10:07.834683', 17.782, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (410, '2023-02-06 20:10:08.154013', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (411, '2023-02-06 20:11:02.137778', 153.209, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (412, '2023-02-06 20:11:04.159919', 14.356941, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (413, '2023-02-06 20:11:07.188546', 19.696, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (414, '2023-02-06 20:11:07.502570', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (415, '2023-02-06 20:12:02.468549', 130.996, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (416, '2023-02-06 20:12:04.488286', 13.263555, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (417, '2023-02-06 20:12:07.536226', 23.87, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (418, '2023-02-06 20:12:07.861578', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (419, '2023-02-06 20:13:02.824913', 141.37800000000001, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (420, '2023-02-06 20:13:04.845315', 13.600947, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (421, '2023-02-06 20:13:07.881188', 20.471, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (422, '2023-02-06 20:13:08.203212', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (423, '2023-02-06 20:14:02.225229', 162.232, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (424, '2023-02-06 20:14:04.249347', 16.588141, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (425, '2023-02-06 20:14:07.277367', 18.485, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (426, '2023-02-06 20:14:07.620575', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (427, '2023-02-06 20:15:02.905303', 414.666, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (428, '2023-02-06 20:15:04.936336', 23.556356, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (429, '2023-02-06 20:15:07.966265', 19.2, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (430, '2023-02-06 20:15:08.284878', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (431, '2023-02-06 20:16:02.526150', 403.357, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (432, '2023-02-06 20:16:04.551483', 12.06966, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (433, '2023-02-06 20:16:07.581183', 18.652, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (434, '2023-02-06 20:16:07.904025', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (435, '2023-02-06 20:17:02.900384', 145.751, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (436, '2023-02-06 20:17:04.922182', 14.357432, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (437, '2023-02-06 20:17:07.956764', 18.202, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (438, '2023-02-06 20:17:08.277567', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (439, '2023-02-06 20:18:02.268856', 153.60199999999998, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (440, '2023-02-06 20:18:04.297214', 15.480798, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (441, '2023-02-06 20:18:07.324292', 21.284, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (442, '2023-02-06 20:18:07.646975', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (443, '2023-02-06 20:19:02.628169', 131.309, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (444, '2023-02-06 20:19:04.655575', 13.841169, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (445, '2023-02-06 20:19:07.689747', 18.895, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (446, '2023-02-06 20:19:08.033034', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (447, '2023-02-06 20:20:01.989965', 144.211, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (448, '2023-02-06 20:20:04.015873', 12.389051, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (449, '2023-02-06 20:20:07.051048', 18.709, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (450, '2023-02-06 20:20:07.366493', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (451, '2023-02-06 20:21:02.401020', 174.811, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (452, '2023-02-06 20:21:04.431626', 23.743527, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (453, '2023-02-06 20:21:07.458606', 18.055, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (454, '2023-02-06 20:21:07.775990', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (455, '2023-02-06 20:22:02.776006', 170.488, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (456, '2023-02-06 20:22:04.804846', 15.282745, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (457, '2023-02-06 20:22:07.834069', 19.742, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (458, '2023-02-06 20:22:08.155710', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (459, '2023-02-06 20:23:02.126182', 163.02, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (460, '2023-02-06 20:23:04.149449', 15.759396, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (461, '2023-02-06 20:23:07.185610', 21.492, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (462, '2023-02-06 20:23:07.518037', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (463, '2023-02-06 20:24:02.515621', 182.5, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (464, '2023-02-06 20:24:04.537577', 14.018592, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (465, '2023-02-06 20:24:07.566459', 18.338, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (466, '2023-02-06 20:24:07.929294', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (467, '2023-02-06 20:25:02.905253', 142.157, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (468, '2023-02-06 20:25:04.942210', 22.772405, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (469, '2023-02-06 20:25:07.969656', 18.703, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (470, '2023-02-06 20:25:08.288949', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (471, '2023-02-06 20:26:02.267359', 166.382, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (472, '2023-02-06 20:26:04.295679', 14.583691, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (473, '2023-02-06 20:26:07.325310', 19.381, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (474, '2023-02-06 20:26:07.637886', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (475, '2023-02-06 20:27:02.568598', 143.14499999999998, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (476, '2023-02-06 20:27:04.591869', 14.847321, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (477, '2023-02-06 20:27:07.621411', 17.961, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (478, '2023-02-06 20:27:07.943612', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (479, '2023-02-06 20:28:01.934019', 171.85, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (480, '2023-02-06 20:28:03.958513', 11.88041, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (481, '2023-02-06 20:28:06.986661', 18.404, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (482, '2023-02-06 20:28:07.305878', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (483, '2023-02-06 20:29:02.268292', 150.311, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (484, '2023-02-06 20:29:04.296141', 14.332615, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (485, '2023-02-06 20:29:07.324512', 18.587, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (486, '2023-02-06 20:29:07.663016', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (487, '2023-02-06 20:30:02.661820', 135.88500000000002, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (488, '2023-02-06 20:30:04.683452', 12.719755, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (489, '2023-02-06 20:30:07.714065', 17.388, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (490, '2023-02-06 20:30:08.039417', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (491, '2023-02-06 20:31:02.000265', 144.62900000000002, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (492, '2023-02-06 20:31:04.028832', 13.554208, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (493, '2023-02-06 20:31:07.062408', 18.248, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (494, '2023-02-06 20:31:07.375438', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (495, '2023-02-06 20:32:02.379607', 170.421, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (496, '2023-02-06 20:32:04.409512', 13.598227, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (497, '2023-02-06 20:32:07.436478', 18.48, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (498, '2023-02-06 20:32:07.754881', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (499, '2023-02-06 20:33:02.706628', 147.99499999999998, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (500, '2023-02-06 20:33:04.725937', 12.849564, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (501, '2023-02-06 20:33:07.752631', 18.271, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (502, '2023-02-06 20:33:08.108140', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (503, '2023-02-06 20:34:02.062992', 143.407, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (504, '2023-02-06 20:34:04.084783', 13.453335, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (505, '2023-02-06 20:34:07.120243', 17.733, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (506, '2023-02-06 20:34:07.460622', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (507, '2023-02-06 20:35:02.418164', 125.67, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (508, '2023-02-06 20:35:04.444317', 12.631081, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (509, '2023-02-06 20:35:07.471862', 18.327, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (510, '2023-02-06 20:35:07.784375', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (511, '2023-02-06 20:36:02.714492', 144.897, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (512, '2023-02-06 20:36:04.736194', 12.613969, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (513, '2023-02-06 20:36:07.769143', 18.538, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (514, '2023-02-06 20:36:08.088012', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (515, '2023-02-06 20:37:02.054821', 143.62199999999999, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (516, '2023-02-06 20:37:04.080970', 12.327117, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (517, '2023-02-06 20:37:07.116014', 18.251, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (518, '2023-02-06 20:37:07.431742', 0, 20);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (519, '2023-02-06 20:38:02.409118', 151.134, 17);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (520, '2023-02-06 20:38:04.436076', 12.88433, 18);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (521, '2023-02-06 20:38:07.463551', 18.342, 19);
insert into NanoSiem.overwatch_networkservicelog (id, timestamp, latency, service_id) values (522, '2023-02-06 20:38:07.774322', 0, 20);
