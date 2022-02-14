CREATE TABLE `data` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`timestamp` VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	`cur_speed` FLOAT(20) NOT NULL,
	`set_speed` INT(20) NOT NULL,
	`throttle` FLOAT(20) NOT NULL,
	PRIMARY KEY (`id`)
);