-- MySQL Script generated by MySQL Workbench
-- Tue Jul 23 15:46:09 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema db_mysite
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db_mysite
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_mysite` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `db_mysite` ;

-- -----------------------------------------------------
-- Table `db_mysite`.`auth_group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`auth_group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`django_content_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`django_content_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label` ASC, `model` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`auth_permission`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`auth_permission` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `content_type_id` INT NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id` ASC, `codename` ASC) VISIBLE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `db_mysite`.`django_content_type` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 81
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`auth_group_permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`auth_group_permissions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `group_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id` ASC, `permission_id` ASC) VISIBLE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id` ASC) VISIBLE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `db_mysite`.`auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `db_mysite`.`auth_group` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`auth_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`auth_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME(6) NULL DEFAULT NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`auth_user_groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`auth_user_groups` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id` ASC, `group_id` ASC) VISIBLE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id` ASC) VISIBLE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `db_mysite`.`auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `db_mysite`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`auth_user_user_permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`auth_user_user_permissions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id` ASC, `permission_id` ASC) VISIBLE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id` ASC) VISIBLE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `db_mysite`.`auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `db_mysite`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`django_admin_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`django_admin_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `action_time` DATETIME(6) NOT NULL,
  `object_id` LONGTEXT NULL DEFAULT NULL,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` SMALLINT UNSIGNED NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  `content_type_id` INT NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id` ASC) VISIBLE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `db_mysite`.`django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `db_mysite`.`auth_user` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`django_migrations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`django_migrations` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 54
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`django_session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  INDEX `django_session_expire_date_a5c62663` (`expire_date` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`polls_question`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`polls_question` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `question_text` VARCHAR(200) NOT NULL,
  `pub_date` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`polls_choice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`polls_choice` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `choice_text` VARCHAR(200) NOT NULL,
  `votes` INT NOT NULL,
  `question_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `polls_choice_question_id_c5b4b260_fk_polls_question_id` (`question_id` ASC) VISIBLE,
  CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id`
    FOREIGN KEY (`question_id`)
    REFERENCES `db_mysite`.`polls_question` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`polls_cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`polls_cliente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `cnpj` VARCHAR(14) NOT NULL,
  `senha` VARCHAR(128) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `polls_cliente_email_87df1e56_uniq` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `db_mysite`.`polls_login`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_mysite`.`polls_login` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `cliente_id` INT NOT NULL,
  `data_time` DATETIME(6) NOT NULL,
  `descricao` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `polls_login_cliente_id_807511c7_fk_polls_cliente_id` (`cliente_id` ASC) VISIBLE,
  CONSTRAINT `polls_login_cliente_id_807511c7_fk_polls_cliente_id`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `db_mysite`.`polls_cliente` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;