use test;
DROP TABLE IF EXISTS `user_table`;
CREATE TABLE `user_table`  (
  `id` int AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;
INSERT INTO `user_table` VALUES (1, 'admin', '123456', '管理员', '12306@qq.com', '15655556666');
INSERT INTO `user_table` VALUES (2, 'admin', '123456', '管理员', '23456@qq.com', '13552699852');
INSERT INTO `user_table` VALUES (3, 'admin', '124wedewrt', '管理员', 'xxsdfscs', '1542289294');

select count(*) from user_table;
SHOW FIELDS FROM maintenance_plan;

select password from user_table where username='admin';

DROP TABLE IF EXISTS `maintenance_plan`;
create table `test`.`maintenance_plan`(
    `number` varchar(60) not null,
    `position` varchar(100) not null,
    `imgset` varchar(100) not null,
    `left1-半月` varchar(100) not null,
    `left2-半年` varchar(100) not null,
    `left3-半月` varchar(100) not null,
    `left4-半月` varchar(100) not null,
    PRIMARY KEY (`number`,`position`,`imgset`,`left1-半月`,`left2-半年`,`left3-半月`,`left4-半月`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


insert into `test`.`maintenance_plan` (`number`,`position`,`imgset`,`left1-半月`,`left2-半年`,`left3-半月`,`left4-半月`) VALUES
('T46971', '11栋中-南','<a href="/static/image/T46971.png">T46971.png</a>', '11月1', '11月15', '11月29', 'NO'),
('T46968', '11栋中-北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月1', '11月15', '11月29', 'NO'),
('T46964', '11栋西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月1', '11月15', '11月29', 'NO'),
('T54967', 'A1楼西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月1', '11月15', '11月29', 'NO'),
('T54966', 'A1楼东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月1', '11月15', '11月29', 'NO'),
('T54965', 'A1楼北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月1', '11月15', '11月29', 'NO'),
('T54964', 'A3楼西南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月2', '11月16', '11月30', 'NO'),
('T54963', 'A3楼西北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月2', '11月16', '11月30', 'NO'),
('T54962', 'A3楼东南南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月2', '11月16', '11月30', 'NO'),
('T54961', 'A3楼东南北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月2', '11月16', '11月30', 'NO'),
('T54960', 'A3楼东北南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月2', '11月16', '11月30', 'NO'),
('T54959', 'A3楼东北北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月2', '11月16', '11月30', 'NO'),
('T46974', '1栋南东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月3', '11月17', '12月1', 'NO'),
('T46975', '1栋南中','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月3', '11月17', '12月1', 'NO'),
('T46976', '1栋南西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月3', '11月17', '12月1', 'NO'),
('T48294', '1栋北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月3', '11月17', '12月1', 'NO'),
('T46961', '2栋南东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月3', '11月17', '12月1', 'NO'),
('T46962', '2栋南西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月3', '11月17', '12月1', 'NO'),
('T48662', 'B2-5区（综合楼1）B楼','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月4', '11月18', '12月2', 'NO'),
('T48663', 'B2-5区（综合楼1）A楼北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月4', '11月18', '12月2', 'NO'),
('T48658', 'B2-5区（综合楼1）B楼1~2层北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月4', '11月18', '12月2', 'NO'),
('T48659', 'B2-5区（综合楼1）B楼1~2层南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月4', '11月18', '12月2', 'NO'),
('T48661', 'B2-5区（综合楼1）A楼南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月4', '11月18', '12月2', 'NO'),
('T48290', '5栋A座北东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月4', '11月18', '12月2', 'NO'),
('T47706', '5栋西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月4', '11月18', '12月2', 'NO'),
('T47716', '6幢西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47717', '6幢北客梯','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47718', '6幢南客梯','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47719', '6幢东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47713', '7幢南客梯','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47714', '7幢北客梯','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47715', '7幢东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月5', '11月19', '12月3', 'NO'),
('T47710', '8幢北客梯','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月6', '11月20', '12月4', 'NO'),
('T47711', '8幢南客梯','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月6', '11月20', '12月4', 'NO'),
('T47712', '8幢东','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月6', '11月20', '12月4', 'NO'),
('T46969', '9幢东(南)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月6', '11月20', '12月4', 'NO'),
('T46966', '9幢西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月6', '11月20', '12月4', 'NO'),
('T46972', '9幢东(北)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月6', '11月20', '12月4', 'NO'),
('T46977', '10幢(东)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月7', '11月21', '12月5', 'NO'),
('T46978', '10幢西(北)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月7', '11月21', '12月5', 'NO'),
('T46979', '10幢西(南)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月7', '11月21', '12月5', 'NO'),
('T46970', '11幢(东)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月7', '11月21', '12月5', 'NO'),
('T61050', '奥杰大厦','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月7', '11月21', '12月5', 'NO'),
('T47704', '5幢东(东)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月8', '11月22', '12月6', 'NO'),
('T47705', '5幢东(西)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月8', '11月22', '12月6', 'NO'),
('T47706', '5幢西', '<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月8', '11月22', '12月6', 'NO'),
('T47707', '4幢东', '<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月8', '11月22', '12月6', 'NO'),
('T47708', '4幢西(东)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月8', '11月22', '12月6', 'NO'),
('T47709', '4幢西(西)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月8', '11月22', '12月6', 'NO'),
('T46963', '2幢南（中）','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月9', '11月23', '12月7', 'NO'),
('T48293', '2幢北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月9', '11月23', '12月7', 'NO'),
('T46965', '3幢东(东)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月9', '11月23', '12月7', 'NO'),
('T48292', '3幢A座北(东)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月9', '11月23', '12月7', 'NO'),
('T46967', '3幢西','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月9', '11月23', '12月7', 'NO'),
('T46973', '3幢东(西)', '<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月9', '11月23', '12月7', 'NO'),
('T53494', 'B3区19幢(北)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月10', '11月24', '12月8', 'NO'),
('T53496', 'B3区19幢(南)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月10', '11月24', '12月8', 'NO'),
('T53509', 'B3区20幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月10', '11月24', '12月8', 'NO'),
('T53507', 'B3区21幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月10', '11月24', '12月8', 'NO'),
('T53504', 'B3区22幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月10', '11月24', '12月8', 'NO'),
('T53502', 'B3区23幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月10', '11月24', '12月8', 'NO'),
('T53501', 'B3区12幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月11', '11月25', '12月9', 'NO'),
('T53503', 'B3区15幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月11', '11月25', '12月9', 'NO'),
('T53506', 'B3区16幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月11', '11月25', '12月9', 'NO'),
('T53508', 'B3区17幢','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月11', '11月25', '12月9', 'NO'),
('T53495', 'B3区18幢(北)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月11', '11月25', '12月9', 'NO'),
('T53493', 'B3区18幢(南)','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月11', '11月25', '12月9', 'NO'),
('T53492', 'B3区综合楼2东南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>', '11月12', '11月26', '12月10', 'NO'),
('T53505', 'B3区综合楼2北', '<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月12', '11月26', '12月10', 'NO'),
('T53497', 'B3区综合楼2扶梯1F-2F南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月12', '11月26', '12月10', 'NO'),
('T53498', 'B3区综合楼2扶梯1F-2F北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月12', '11月26', '12月10', 'NO'),
('T53499', 'B3区综合楼2扶梯2F-3F南','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月12', '11月26', '12月10', 'NO'),
('T53500', 'B3区综合楼2扶梯2F-3F北','<a href="/static/image/1栋T46974.png">1栋T46974.png</a>','11月12', '11月26', '12月10', 'NO');

select * from `test`.`maintenance_plan` where `left1-半月`='11月12' or `left2-半月`='11月12' ;#order by `number` desc;
SELECT t.*
      FROM test.maintenance_plan t
      LIMIT 501;

select * from Maintenance_plan where left1='11月3-半';
# name: Super Admin

CREATE TABLE `test`.`city_today`(
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `confirm` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `suspect` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `heal` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `dead` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `severe` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `storeConfirm` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `lastUpdateTime`varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `province_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `uni` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
PRIMARY KEY (`id`,`name`,`confirm`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;


select * from city_today;

CREATE TABLE city_total(
    `id`int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `confirm`varchar(100) NOT NULL,
    `suspect`varchar(100) NOT NULL,
    `heal`varchar(100) NOT NULL,
    `dead`varchar(100) NOT NULL,
    `severe`varchar(100) NOT NULL,
    `lastUpdateTime`varchar(100) NOT NULL,
    `province_name`varchar(100) NOT NULL,
    `uni`varchar(100) NOT NULL,
PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;
create table province_today(
    `id`int NOT NULL AUTO_INCREMENT,
    `name`varchar(100) NOT NULL,
    `confirm`varchar(100) NOT NULL,
    `suspect`varchar(100) NOT NULL,
    `heal`varchar(100) NOT NULL,
    `dead`varchar(100) NOT NULL,
    `severe`varchar(100) NOT NULL,
    `storeConfirm`varchar(100) NOT NULL,
    `lastUpdateTime`varchar(100) NOT NULL,
    `uni`varchar(100) NOT NULL,
PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

create table province_total(
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `confirm` varchar(100) NOT NULL,
    `suspect` varchar(100) NOT NULL,
    `heal` varchar(100) NOT NULL,
    `dead` varchar(100) NOT NULL,
    `severe` varchar(100) NOT NULL,
    `input` varchar(100) NOT NULL,
    `lastUpdateTime` varchar(100) NOT NULL,
    `uni` varchar(100) NOT NULL,
    PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

create table country_today(
    `id` int NOT NULL AUTO_INCREMENT,
    `name`varchar(100) NOT NULL,
    `confirm`varchar(100) NOT NULL,
    `suspect`varchar(100) NOT NULL,
    `heal`varchar(100) NOT NULL,
    `dead`varchar(100) NOT NULL,
    `severe`varchar(100) NOT NULL,
    `storeConfirm`varchar(100) NOT NULL,
    `lastUpdateTime`varchar(100) NOT NULL,
    `uni`varchar(100) NOT NULL,
    PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;



create table country_total(
    `id` int NOT NULL AUTO_INCREMENT,
    `name`varchar(100) NOT NULL,
    `confirm`varchar(100) NOT NULL,
    `suspect`varchar(100) NOT NULL,
    `heal`varchar(100) NOT NULL,
    `dead`varchar(100) NOT NULL,
    `severe`varchar(100) NOT NULL,
    `input`varchar(100) NOT NULL,
    `lastUpdateTime`varchar(100) NOT NULL,
    `uni`varchar(100) NOT NULL,
PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;
select *from country_today;
select *from country_total;
