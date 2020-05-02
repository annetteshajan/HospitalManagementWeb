-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: hospmgmt
-- ------------------------------------------------------
-- Server version	5.7.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ADMIN`
--

DROP TABLE IF EXISTS `ADMIN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ADMIN` (
  `ADMIN_ID` varchar(5) NOT NULL,
  `FN` varchar(10) DEFAULT NULL,
  `LN` varchar(10) DEFAULT NULL,
  `USERNAME` varchar(10) DEFAULT NULL,
  `PASSWORD` varchar(20) DEFAULT NULL,
  `PHONE` decimal(10,0) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ADMIN_ID`),
  UNIQUE KEY `USERNAME` (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ADMIN`
--

LOCK TABLES `ADMIN` WRITE;
/*!40000 ALTER TABLE `ADMIN` DISABLE KEYS */;
INSERT INTO `ADMIN` VALUES ('A0','ANNETTE','SHAJAN','admin','password',9632553962,'a@b.com'),('A1','aneesh','sidharth','aneesh','merc1288',9686446858,'an@.g');
/*!40000 ALTER TABLE `ADMIN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `APPOINTMENT`
--

DROP TABLE IF EXISTS `APPOINTMENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `APPOINTMENT` (
  `DOC_ID` varchar(5) DEFAULT NULL,
  `PAT_ID` varchar(5) DEFAULT NULL,
  KEY `DOC_ID` (`DOC_ID`),
  KEY `PAT_ID` (`PAT_ID`),
  CONSTRAINT `APPOINTMENT_ibfk_1` FOREIGN KEY (`DOC_ID`) REFERENCES `DOCTOR` (`DOCTOR_ID`),
  CONSTRAINT `APPOINTMENT_ibfk_2` FOREIGN KEY (`PAT_ID`) REFERENCES `PATIENT` (`PATIENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APPOINTMENT`
--

LOCK TABLES `APPOINTMENT` WRITE;
/*!40000 ALTER TABLE `APPOINTMENT` DISABLE KEYS */;
INSERT INTO `APPOINTMENT` VALUES ('D6','P1'),('D5','P2'),('D0','P1'),('D1','P1'),('D4','P1'),('D0','P5');
/*!40000 ALTER TABLE `APPOINTMENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BILL`
--

DROP TABLE IF EXISTS `BILL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BILL` (
  `BILL_ID` varchar(5) NOT NULL,
  `PATIENT_ID` varchar(5) DEFAULT NULL,
  `DOCTOR_ID` varchar(5) DEFAULT NULL,
  `CONSULTFEE` decimal(10,0) DEFAULT NULL,
  `EXTRA` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`BILL_ID`),
  KEY `PATIENT_ID` (`PATIENT_ID`),
  KEY `DOCTOR_ID` (`DOCTOR_ID`),
  CONSTRAINT `BILL_ibfk_1` FOREIGN KEY (`PATIENT_ID`) REFERENCES `PATIENT` (`PATIENT_ID`),
  CONSTRAINT `BILL_ibfk_2` FOREIGN KEY (`DOCTOR_ID`) REFERENCES `DOCTOR` (`DOCTOR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BILL`
--

LOCK TABLES `BILL` WRITE;
/*!40000 ALTER TABLE `BILL` DISABLE KEYS */;
INSERT INTO `BILL` VALUES ('B0','P1','D6',500,200),('B1','P2','D5',1000,300);
/*!40000 ALTER TABLE `BILL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DEPARTMENT`
--

DROP TABLE IF EXISTS `DEPARTMENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DEPARTMENT` (
  `DEP_ID` varchar(5) NOT NULL,
  `NAME` varchar(15) DEFAULT NULL,
  `RATING` decimal(3,0) DEFAULT NULL,
  PRIMARY KEY (`DEP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DEPARTMENT`
--

LOCK TABLES `DEPARTMENT` WRITE;
/*!40000 ALTER TABLE `DEPARTMENT` DISABLE KEYS */;
INSERT INTO `DEPARTMENT` VALUES ('D01','GENERAL MED',5),('D02','SURGERY',5),('D03','DENTAL',5),('D04','ORTHOPAEDICS',5),('D05','CARDIOLOGY',5);
/*!40000 ALTER TABLE `DEPARTMENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DOCTOR`
--

DROP TABLE IF EXISTS `DOCTOR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DOCTOR` (
  `DOCTOR_ID` varchar(5) NOT NULL,
  `FN` varchar(10) DEFAULT NULL,
  `LN` varchar(10) DEFAULT NULL,
  `DEP_ID` varchar(5) DEFAULT NULL,
  `QUAL1` varchar(10) DEFAULT NULL,
  `QUAL2` varchar(10) DEFAULT NULL,
  `QUAL3` varchar(10) DEFAULT NULL,
  `CONSULT` time DEFAULT NULL,
  `PHONE` decimal(10,0) DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `ADDRESS` varchar(50) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `USERNAME` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(30) DEFAULT NULL,
  `CONSULT_TILL` time DEFAULT NULL,
  `RATING` decimal(3,0) DEFAULT '5',
  `DORMANT` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`DOCTOR_ID`),
  UNIQUE KEY `USERNAME` (`USERNAME`),
  KEY `DEP_ID` (`DEP_ID`),
  CONSTRAINT `DOCTOR_ibfk_1` FOREIGN KEY (`DEP_ID`) REFERENCES `DEPARTMENT` (`DEP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DOCTOR`
--

LOCK TABLES `DOCTOR` WRITE;
/*!40000 ALTER TABLE `DOCTOR` DISABLE KEYS */;
INSERT INTO `DOCTOR` VALUES ('D0','Abcdef','Ggsdg','D01','MBBS','MD','','02:00:00',232564,'m','Indiranagar','a@gmail.com','a','pass2','10:00:00',5,0),('D1','ABC','DEF','D03','MBBS','MD','','03:00:00',2347882,'m','Whitefield','ab@g.co','dr1','pass2','08:00:00',8,0),('D2','Pqr','Fgh','D05','MBBS','MD','','02:00:00',232453,'f','Indiranagar','pqr@gmail.com','dr2','pass1','10:00:00',5,0),('D3','JAGDISH','CHINNAPPA','D04','MBBS','MD','','02:00:00',9611128073,'m','koramangla','Chin@.com','dr3','pass2','05:00:00',5,0),('D4','AKSHITA','KOTHARI','D01','MBBS','MD','','04:00:00',8971877551,'f','whitefield','AK@.COM','dr4','pass4','08:00:00',5,0),('D5','sumita','jha','D04','MBBS','','','10:00:00',9980544600,'f','HSR','sumita@.com','dr5','pass5','01:00:00',7,0),('D6','vidhaan','mishra','D02','MBBS','MS','','04:00:00',9686446857,'m','indiranagar','vd@.com','dr6','pass6','07:00:00',6,0);
/*!40000 ALTER TABLE `DOCTOR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEDRECORD`
--

DROP TABLE IF EXISTS `MEDRECORD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MEDRECORD` (
  `RECORD_ID` varchar(5) NOT NULL,
  `PATIENT_ID` varchar(5) NOT NULL,
  `CONSULT` date DEFAULT NULL,
  `CASEHIST` varchar(30) DEFAULT NULL,
  `DIAGNOSIS` varchar(30) DEFAULT NULL,
  `PRESC` varchar(30) DEFAULT NULL,
  `DOC_ID` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`RECORD_ID`,`PATIENT_ID`),
  KEY `PATIENT_ID` (`PATIENT_ID`),
  KEY `DOC_ID` (`DOC_ID`),
  CONSTRAINT `MEDRECORD_ibfk_1` FOREIGN KEY (`PATIENT_ID`) REFERENCES `PATIENT` (`PATIENT_ID`),
  CONSTRAINT `MEDRECORD_ibfk_2` FOREIGN KEY (`DOC_ID`) REFERENCES `DOCTOR` (`DOCTOR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEDRECORD`
--

LOCK TABLES `MEDRECORD` WRITE;
/*!40000 ALTER TABLE `MEDRECORD` DISABLE KEYS */;
INSERT INTO `MEDRECORD` VALUES ('R2','P1','2019-11-05','cyst','laparoscopy','med2,med3','D6'),('R2','P2','2019-03-23','hairline fracture','graft','dolo','D5');
/*!40000 ALTER TABLE `MEDRECORD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PATIENT`
--

DROP TABLE IF EXISTS `PATIENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PATIENT` (
  `PATIENT_ID` varchar(5) NOT NULL,
  `FN` varchar(10) DEFAULT NULL,
  `LN` varchar(10) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `HEIGHT` decimal(5,0) DEFAULT NULL,
  `WEIGHT` decimal(5,0) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `HISTORY` varchar(500) DEFAULT NULL,
  `PHONE` decimal(10,0) DEFAULT NULL,
  `ADDRESS` varchar(50) DEFAULT NULL,
  `USERNAME` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(30) DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `BP` varchar(10) DEFAULT NULL,
  `EMERGENCY` varchar(10) DEFAULT NULL,
  `DORMANT` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`PATIENT_ID`),
  UNIQUE KEY `USERNAME` (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PATIENT`
--

LOCK TABLES `PATIENT` WRITE;
/*!40000 ALTER TABLE `PATIENT` DISABLE KEYS */;
INSERT INTO `PATIENT` VALUES ('P0','Michelle','Shajan','mS@g.com',190,3,'2004-04-05','Dust',92843792,'here','michelle','pass1','m','120/20','92348792',0),('P1','Aaa','Bbb','aaa@bbb.com',180,50,'1990-05-03','Pollen',8875658,'Sarjapur','pat1','pass2','f','140/10','763874628',0),('P2','Bbb','Ccc','bb@cc.com',200,40,'1998-07-06','',34344534,'Kengeri','pat2','pass1','m','130/20','43634634',0),('P3','Ccc','Ddd','cc@gmail.com',140,50,'2000-12-08','Lactose',4534325,'Mysore','pat3','pass1','o','120/30','5645733',0),('P4','Annette','','a@g.com',180,20,'1999-08-28','',34351312,'','annette','pass','m','324','434534',0),('P5','ak','jn','alll@.com',123,50,'1998-08-12','lk',0,'209lkn','akshita','merc8020','f','80/120','8888888888',0);
/*!40000 ALTER TABLE `PATIENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ROOM`
--

DROP TABLE IF EXISTS `ROOM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ROOM` (
  `ROOM_NO` int(11) NOT NULL,
  `PATIENT_ID` varchar(5) DEFAULT NULL,
  `ADMITDATE` date DEFAULT NULL,
  `DISCHARGE` date DEFAULT NULL,
  `DOC_ID` varchar(5) DEFAULT NULL,
  `STAFF_ID` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`ROOM_NO`),
  KEY `PATIENT_ID` (`PATIENT_ID`),
  KEY `DOC_ID` (`DOC_ID`),
  KEY `STAFF_ID` (`STAFF_ID`),
  CONSTRAINT `ROOM_ibfk_1` FOREIGN KEY (`PATIENT_ID`) REFERENCES `PATIENT` (`PATIENT_ID`),
  CONSTRAINT `ROOM_ibfk_2` FOREIGN KEY (`DOC_ID`) REFERENCES `DOCTOR` (`DOCTOR_ID`),
  CONSTRAINT `ROOM_ibfk_3` FOREIGN KEY (`STAFF_ID`) REFERENCES `STAFF` (`STAFF_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ROOM`
--

LOCK TABLES `ROOM` WRITE;
/*!40000 ALTER TABLE `ROOM` DISABLE KEYS */;
INSERT INTO `ROOM` VALUES (5,'P1','2019-10-07','2019-10-10','D6','S3');
/*!40000 ALTER TABLE `ROOM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `STAFF`
--

DROP TABLE IF EXISTS `STAFF`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `STAFF` (
  `STAFF_ID` varchar(5) NOT NULL,
  `FN` varchar(10) DEFAULT NULL,
  `LN` varchar(10) DEFAULT NULL,
  `DEP_ID` varchar(5) DEFAULT NULL,
  `PHONE` decimal(10,0) DEFAULT NULL,
  `DORMANT` tinyint(1) DEFAULT '0',
  `EMAIL` varchar(100) DEFAULT NULL,
  `USERNAME` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`STAFF_ID`),
  KEY `DEP_ID` (`DEP_ID`),
  CONSTRAINT `STAFF_ibfk_1` FOREIGN KEY (`DEP_ID`) REFERENCES `DEPARTMENT` (`DEP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `STAFF`
--

LOCK TABLES `STAFF` WRITE;
/*!40000 ALTER TABLE `STAFF` DISABLE KEYS */;
INSERT INTO `STAFF` VALUES ('S0','Ann','shajan','D03',83924972,0,'abc@g.com','annette','pass'),('S1','Donald','Trump','D01',72348763,0,'dt@gmail.com','staff1','p1'),('S2','ankita','kothari','D01',8971877551,0,'an@.com','st1','merc100'),('S3','pooja','chowdary','D02',7777777777,0,'pc@.com','st2','merc200'),('S4','leeannah','aleaxander','D03',888888888,0,'la@.com','st3','merc300'),('S5','lakshita','kothari','D04',999999999,0,'lk@.com','st5','merc500');
/*!40000 ALTER TABLE `STAFF` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-24  9:20:06
