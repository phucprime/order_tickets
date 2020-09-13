-- Tai khoan dang nhap Admin Page:
-- Tai khoan: admin
-- Mat khau: admin
-- Script SqlAlchemy


DROP TABLE IF EXISTS `flight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight` (
  `id` int NOT NULL AUTO_INCREMENT,
  `airfield` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `airfield_land_off` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `time_duration` int NOT NULL,
  `available_chair` int DEFAULT NULL,
  `unavailable_chair` int DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight`
--

LOCK TABLES `flight` WRITE;
/*!40000 ALTER TABLE `flight` DISABLE KEYS */;
INSERT INTO `flight` VALUES (1,'Tân Sơn Nhất','Nội Bài','2020-09-18 00:00:00',50,110,30,560000),(2,'Đà Nẵng','Hải Phòng','2020-09-22 00:00:00',70,200,30,350000),(3,'Cần Thơ','Đà Nẵng','2020-09-22 00:00:00',120,40,10,400000),(4,'Tân Sơn Nhất','Bangkok','2020-09-14 00:00:00',480,300,50,890000),(5,'Nội Bài','Seoul','2020-09-13 00:00:00',550,330,40,650000),(6,'Đà Nẵng','Bắc Kinh','2020-09-18 00:00:00',240,130,60,750000),(7,'Nội Bài','Phú Quốc','2020-09-21 00:00:00',60,90,40,350000),(8,'Vinh','Sydney','2020-09-22 00:00:00',600,330,30,12000000),(9,'Cần Thơ','New York','2020-09-20 00:00:00',500,400,150,950000),(10,'Tân Sơn Nhất','Tokyo','2020-09-14 00:00:00',300,40,10,550000);
/*!40000 ALTER TABLE `flight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flightschedule`
--

DROP TABLE IF EXISTS `flightschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flightschedule` (
  `flight_id` int NOT NULL,
  `chair_type_1` int NOT NULL,
  `chair_type_2` int NOT NULL,
  `mid_airfield` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mid_airfield_time` int DEFAULT NULL,
  `mid_airfield_note` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mid_airfield_2` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mid_airfield_time_2` int DEFAULT NULL,
  `mid_airfield_note_2` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`flight_id`),
  CONSTRAINT `flightschedule_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flightschedule`
--

LOCK TABLES `flightschedule` WRITE;
/*!40000 ALTER TABLE `flightschedule` DISABLE KEYS */;
INSERT INTO `flightschedule` VALUES (1,10,20,'Đà Nẵng',10,'Ăn uống',NULL,NULL,NULL);
/*!40000 ALTER TABLE `flightschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `flight_id` int NOT NULL,
  `bill` int NOT NULL AUTO_INCREMENT,
  `identity_number` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `ticket_type` int NOT NULL,
  `passengers` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`bill`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flightschedule` (`flight_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,1,'341909090',1,'Nguyen Hoang Phuc','0945069017','phuc@phuc.phuc',560000);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rules`
--

DROP TABLE IF EXISTS `rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `max_airfield` int NOT NULL,
  `min_time_duration` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rules`
--

LOCK TABLES `rules` WRITE;
/*!40000 ALTER TABLE `rules` DISABLE KEYS */;
INSERT INTO `rules` VALUES (1,10,30);
/*!40000 ALTER TABLE `rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `username` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'phuc',NULL,'admin','21232f297a57a5a743894a0e4a801fc3');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-11 17:20:45
