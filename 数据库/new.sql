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
INSERT INTO `user_table` VALUES (1, 'admin', '123456', '����Ա', '12306@qq.com', '15655556666');
INSERT INTO `user_table` VALUES (2, 'admin', '123456', '����Ա', '23456@qq.com', '13552699852');
INSERT INTO `user_table` VALUES (3, 'admin', '124wedewrt', '����Ա', 'xxsdfscs', '1542289294');

select count(*) from user_table;
SHOW FIELDS FROM maintenance_plan;

select password from user_table where username='admin';

DROP TABLE IF EXISTS `maintenance_plan`;
create table `test`.`maintenance_plan`(
    `number` varchar(60) not null,
    `position` varchar(100) not null,
    `imgset` varchar(100) not null,
    `left1-����` varchar(100) not null,
    `left2-����` varchar(100) not null,
    `left3-����` varchar(100) not null,
    `left4-����` varchar(100) not null,
    PRIMARY KEY (`number`,`position`,`imgset`,`left1-����`,`left2-����`,`left3-����`,`left4-����`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


insert into `test`.`maintenance_plan` (`number`,`position`,`imgset`,`left1-����`,`left2-����`,`left3-����`,`left4-����`) VALUES
('T46971', '11����-��','<a href="/static/image/T46971.png">T46971.png</a>', '11��1', '11��15', '11��29', 'NO'),
('T46968', '11����-��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��1', '11��15', '11��29', 'NO'),
('T46964', '11����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��1', '11��15', '11��29', 'NO'),
('T54967', 'A1¥��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��1', '11��15', '11��29', 'NO'),
('T54966', 'A1¥��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��1', '11��15', '11��29', 'NO'),
('T54965', 'A1¥��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��1', '11��15', '11��29', 'NO'),
('T54964', 'A3¥����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��2', '11��16', '11��30', 'NO'),
('T54963', 'A3¥����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��2', '11��16', '11��30', 'NO'),
('T54962', 'A3¥������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��2', '11��16', '11��30', 'NO'),
('T54961', 'A3¥���ϱ�','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��2', '11��16', '11��30', 'NO'),
('T54960', 'A3¥������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��2', '11��16', '11��30', 'NO'),
('T54959', 'A3¥������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��2', '11��16', '11��30', 'NO'),
('T46974', '1���϶�','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��3', '11��17', '12��1', 'NO'),
('T46975', '1������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��3', '11��17', '12��1', 'NO'),
('T46976', '1������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��3', '11��17', '12��1', 'NO'),
('T48294', '1����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��3', '11��17', '12��1', 'NO'),
('T46961', '2���϶�','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��3', '11��17', '12��1', 'NO'),
('T46962', '2������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��3', '11��17', '12��1', 'NO'),
('T48662', 'B2-5�����ۺ�¥1��B¥','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��4', '11��18', '12��2', 'NO'),
('T48663', 'B2-5�����ۺ�¥1��A¥��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��4', '11��18', '12��2', 'NO'),
('T48658', 'B2-5�����ۺ�¥1��B¥1~2�㱱','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��4', '11��18', '12��2', 'NO'),
('T48659', 'B2-5�����ۺ�¥1��B¥1~2����','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��4', '11��18', '12��2', 'NO'),
('T48661', 'B2-5�����ۺ�¥1��A¥��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��4', '11��18', '12��2', 'NO'),
('T48290', '5��A������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��4', '11��18', '12��2', 'NO'),
('T47706', '5����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��4', '11��18', '12��2', 'NO'),
('T47716', '6����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47717', '6��������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47718', '6���Ͽ���','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47719', '6����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47713', '7���Ͽ���','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47714', '7��������','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47715', '7����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��5', '11��19', '12��3', 'NO'),
('T47710', '8��������','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��6', '11��20', '12��4', 'NO'),
('T47711', '8���Ͽ���','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��6', '11��20', '12��4', 'NO'),
('T47712', '8����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��6', '11��20', '12��4', 'NO'),
('T46969', '9����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��6', '11��20', '12��4', 'NO'),
('T46966', '9����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��6', '11��20', '12��4', 'NO'),
('T46972', '9����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��6', '11��20', '12��4', 'NO'),
('T46977', '10��(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��7', '11��21', '12��5', 'NO'),
('T46978', '10����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��7', '11��21', '12��5', 'NO'),
('T46979', '10����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��7', '11��21', '12��5', 'NO'),
('T46970', '11��(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��7', '11��21', '12��5', 'NO'),
('T61050', '�½ܴ���','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��7', '11��21', '12��5', 'NO'),
('T47704', '5����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��8', '11��22', '12��6', 'NO'),
('T47705', '5����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��8', '11��22', '12��6', 'NO'),
('T47706', '5����', '<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��8', '11��22', '12��6', 'NO'),
('T47707', '4����', '<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��8', '11��22', '12��6', 'NO'),
('T47708', '4����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��8', '11��22', '12��6', 'NO'),
('T47709', '4����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��8', '11��22', '12��6', 'NO'),
('T46963', '2���ϣ��У�','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��9', '11��23', '12��7', 'NO'),
('T48293', '2����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��9', '11��23', '12��7', 'NO'),
('T46965', '3����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��9', '11��23', '12��7', 'NO'),
('T48292', '3��A����(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��9', '11��23', '12��7', 'NO'),
('T46967', '3����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��9', '11��23', '12��7', 'NO'),
('T46973', '3����(��)', '<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��9', '11��23', '12��7', 'NO'),
('T53494', 'B3��19��(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��10', '11��24', '12��8', 'NO'),
('T53496', 'B3��19��(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��10', '11��24', '12��8', 'NO'),
('T53509', 'B3��20��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��10', '11��24', '12��8', 'NO'),
('T53507', 'B3��21��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��10', '11��24', '12��8', 'NO'),
('T53504', 'B3��22��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��10', '11��24', '12��8', 'NO'),
('T53502', 'B3��23��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��10', '11��24', '12��8', 'NO'),
('T53501', 'B3��12��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��11', '11��25', '12��9', 'NO'),
('T53503', 'B3��15��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��11', '11��25', '12��9', 'NO'),
('T53506', 'B3��16��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��11', '11��25', '12��9', 'NO'),
('T53508', 'B3��17��','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��11', '11��25', '12��9', 'NO'),
('T53495', 'B3��18��(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��11', '11��25', '12��9', 'NO'),
('T53493', 'B3��18��(��)','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��11', '11��25', '12��9', 'NO'),
('T53492', 'B3���ۺ�¥2����','<a href="/static/image/1��T46974.png">1��T46974.png</a>', '11��12', '11��26', '12��10', 'NO'),
('T53505', 'B3���ۺ�¥2��', '<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��12', '11��26', '12��10', 'NO'),
('T53497', 'B3���ۺ�¥2����1F-2F��','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��12', '11��26', '12��10', 'NO'),
('T53498', 'B3���ۺ�¥2����1F-2F��','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��12', '11��26', '12��10', 'NO'),
('T53499', 'B3���ۺ�¥2����2F-3F��','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��12', '11��26', '12��10', 'NO'),
('T53500', 'B3���ۺ�¥2����2F-3F��','<a href="/static/image/1��T46974.png">1��T46974.png</a>','11��12', '11��26', '12��10', 'NO');

select * from `test`.`maintenance_plan` where `left1-����`='11��12' or `left2-����`='11��12' ;#order by `number` desc;
SELECT t.*
      FROM test.maintenance_plan t
      LIMIT 501;

select * from Maintenance_plan where left1='11��3-��';
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
