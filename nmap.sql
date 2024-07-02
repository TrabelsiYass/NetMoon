-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : sam. 25 mai 2024 à 12:36
-- Version du serveur : 8.3.0
-- Version de PHP : 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `nmap`
--

-- --------------------------------------------------------

--
-- Structure de la table `area`
--

DROP TABLE IF EXISTS `area`;
CREATE TABLE IF NOT EXISTS `area` (
  `id_area` int NOT NULL,
  `id_user` int NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id_area`),
  KEY `id_user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `area`
--

INSERT INTO `area` (`id_area`, `id_user`, `date`) VALUES
(1, 1, '2024-05-06'),
(2, 1, '2024-05-06'),
(3, 1, '2024-05-05'),
(4, 1, '2024-05-05'),
(8, 1, '2024-05-15'),
(16, 1, '2024-05-18');

-- --------------------------------------------------------

--
-- Structure de la table `devices`
--

DROP TABLE IF EXISTS `devices`;
CREATE TABLE IF NOT EXISTS `devices` (
  `id_routeer` varchar(16) NOT NULL,
  `id_device` varchar(100) NOT NULL,
  `ip_adress_router` varchar(16) NOT NULL,
  `ip_adress` varchar(16) NOT NULL,
  `mac_adress` varchar(100) NOT NULL,
  `services` json NOT NULL,
  PRIMARY KEY (`id_device`),
  KEY `ip_adress_router` (`ip_adress_router`),
  KEY `id_routeer` (`id_routeer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `devices`
--

INSERT INTO `devices` (`id_routeer`, `id_device`, `ip_adress_router`, `ip_adress`, `mac_adress`, `services`) VALUES
('1', '1', '192.168.1.1', '192.168.1.10', 'fe80::bb78:973:58:2ecb%5', '\"tcp\"'),
('1', '2', '192.168.1.1', '192.168.1.18', 'fe80::bb78:973:58:2ecb%6', '\"tcp\"'),
('3', '3', '172.20.10.1', '172.20.10.15', 'fe80::bb78:973:58:2ecb%7', '\"telnet\"'),
('4', '4', '172.30.10.1', '172.30.10.19', 'fe80::bb78:973:58:2ecb%8', '\"http\"'),
('7', '7', '192.168.1.1', '192.168.1.16', 'fe80::bb78:973:58:2ecb%10', '\"tcp\"'),
('8', '8', '172.20.10.1', '172.20.10.3', 'd0:39:57:05:54:f5', '{\"tcp\": {\"80\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"http\", \"state\": \"open\", \"reason\": \"syn-ack\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}, \"135\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"msrpc\", \"state\": \"open\", \"reason\": \"syn-ack\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}, \"137\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"netbios-ns\", \"state\": \"filtered\", \"reason\": \"no-response\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}, \"139\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"netbios-ssn\", \"state\": \"open\", \"reason\": \"syn-ack\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}, \"445\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"microsoft-ds\", \"state\": \"open\", \"reason\": \"syn-ack\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}}, \"status\": {\"state\": \"up\", \"reason\": \"localhost-response\"}, \"uptime\": {\"seconds\": \"324973\", \"lastboot\": \"Tue May 14 17:36:59 2024\"}, \"vendor\": {}, \"osmatch\": [{\"line\": \"69748\", \"name\": \"Microsoft Windows 10 1607\", \"osclass\": [{\"cpe\": [\"cpe:/o:microsoft:windows_10:1607\"], \"type\": \"general purpose\", \"osgen\": \"10\", \"vendor\": \"Microsoft\", \"accuracy\": \"100\", \"osfamily\": \"Windows\"}], \"accuracy\": \"100\"}], \"portused\": [{\"proto\": \"tcp\", \"state\": \"open\", \"portid\": \"80\"}, {\"proto\": \"tcp\", \"state\": \"closed\", \"portid\": \"1\"}, {\"proto\": \"udp\", \"state\": \"closed\", \"portid\": \"36817\"}], \"addresses\": {\"ipv4\": \"172.20.10.3\"}, \"hostnames\": [{\"name\": \"\", \"type\": \"\"}]}'),
('8', '9', '172.20.10.1', '172.20.10.1', '7a:02:8b:4c:a3:64', '{\"tcp\": {\"21\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"ftp\", \"state\": \"open\", \"reason\": \"syn-ack\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}, \"53\": {\"cpe\": \"\", \"conf\": \"3\", \"name\": \"domain\", \"state\": \"open\", \"reason\": \"syn-ack\", \"product\": \"\", \"version\": \"\", \"extrainfo\": \"\"}}, \"status\": {\"state\": \"up\", \"reason\": \"arp-response\"}, \"vendor\": {}, \"osmatch\": [{\"line\": \"4225\", \"name\": \"Apple iOS 8.0 - 8.1 (Darwin 14.0.0)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:8\"], \"type\": \"phone\", \"osgen\": \"8.X\", \"vendor\": \"Apple\", \"accuracy\": \"94\", \"osfamily\": \"iOS\"}], \"accuracy\": \"94\"}, {\"line\": \"4243\", \"name\": \"Apple iOS 8.1.2 (Darwin 14.0.0)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:8.1.2\"], \"type\": \"phone\", \"osgen\": \"8.X\", \"vendor\": \"Apple\", \"accuracy\": \"94\", \"osfamily\": \"iOS\"}], \"accuracy\": \"94\"}, {\"line\": \"4297\", \"name\": \"Apple iOS 8.3 (Darwin 14.0.0)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:8.3\"], \"type\": \"phone\", \"osgen\": \"8.X\", \"vendor\": \"Apple\", \"accuracy\": \"94\", \"osfamily\": \"iOS\"}], \"accuracy\": \"94\"}, {\"line\": \"7574\", \"name\": \"Apple OS X 10.11.2 (El Capitan) (Darwin 15.2.0)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:mac_os_x:10.11.2\"], \"type\": \"general purpose\", \"osgen\": \"10.11.X\", \"vendor\": \"Apple\", \"accuracy\": \"94\", \"osfamily\": \"OS X\"}], \"accuracy\": \"94\"}, {\"line\": \"4361\", \"name\": \"Apple iOS 9 (Darwin 15.0.0)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:9\"], \"type\": \"phone\", \"osgen\": \"9.X\", \"vendor\": \"Apple\", \"accuracy\": \"94\", \"osfamily\": \"iOS\"}], \"accuracy\": \"94\"}, {\"line\": \"4010\", \"name\": \"Apple iOS 5.1.1\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:5.1.1\"], \"type\": \"media device\", \"osgen\": \"5.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"iOS\"}], \"accuracy\": \"91\"}, {\"line\": \"4029\", \"name\": \"Apple iOS 5.1.1 - 6.1\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:5\"], \"type\": \"media device\", \"osgen\": \"5.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"iOS\"}, {\"cpe\": [\"cpe:/o:apple:iphone_os:5\"], \"type\": \"phone\", \"osgen\": \"5.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"iOS\"}, {\"cpe\": [\"cpe:/o:apple:iphone_os:6\"], \"type\": \"media device\", \"osgen\": \"6.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"iOS\"}, {\"cpe\": [\"cpe:/o:apple:iphone_os:6\"], \"type\": \"phone\", \"osgen\": \"6.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"iOS\"}], \"accuracy\": \"91\"}, {\"line\": \"4206\", \"name\": \"Apple iOS 7.1.1\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:iphone_os:7.1.1\"], \"type\": \"phone\", \"osgen\": \"7.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"iOS\"}], \"accuracy\": \"91\"}, {\"line\": \"6863\", \"name\": \"Apple Mac OS X 10.7.4 (Lion) (Darwin 11.4.2)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:mac_os_x:10.7.4\"], \"type\": \"general purpose\", \"osgen\": \"10.7.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"Mac OS X\"}], \"accuracy\": \"91\"}, {\"line\": \"7610\", \"name\": \"Apple OS X 10.8 (Mountain Lion) (Darwin 12.4.0)\", \"osclass\": [{\"cpe\": [\"cpe:/o:apple:mac_os_x:10.8\"], \"type\": \"general purpose\", \"osgen\": \"10.8.X\", \"vendor\": \"Apple\", \"accuracy\": \"91\", \"osfamily\": \"OS X\"}], \"accuracy\": \"91\"}], \"portused\": [{\"proto\": \"tcp\", \"state\": \"open\", \"portid\": \"21\"}, {\"proto\": \"tcp\", \"state\": \"closed\", \"portid\": \"1\"}, {\"proto\": \"udp\", \"state\": \"closed\", \"portid\": \"38602\"}], \"addresses\": {\"mac\": \"7A:02:8B:4C:A3:64\", \"ipv4\": \"172.20.10.1\"}, \"hostnames\": [{\"name\": \"\", \"type\": \"\"}]}');

-- --------------------------------------------------------

--
-- Structure de la table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
  `id_user` int NOT NULL,
  `msg` varchar(255) NOT NULL,
  KEY `id_user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `feedback`
--

INSERT INTO `feedback` (`id_user`, `msg`) VALUES
(3, 'Application bent qahba !! '),
(3, 'C\'est mieux In Black'),
(3, 'Welcome babay'),
(3, 'taw tetsaker !');

-- --------------------------------------------------------

--
-- Structure de la table `routers`
--

DROP TABLE IF EXISTS `routers`;
CREATE TABLE IF NOT EXISTS `routers` (
  `id_router` varchar(100) NOT NULL,
  `Id_scan` int NOT NULL,
  `ip_adress` varchar(16) NOT NULL,
  PRIMARY KEY (`id_router`) USING BTREE,
  KEY `Id_scan` (`Id_scan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `routers`
--

INSERT INTO `routers` (`id_router`, `Id_scan`, `ip_adress`) VALUES
('1', 1, '192.168.1.1'),
('2', 1, '192.168.1.0'),
('3', 2, '172.20.10.1'),
('4', 2, '172.30.10.1'),
('7', 3, '192.168.1.1'),
('8', 6, '172.20.10.1');

-- --------------------------------------------------------

--
-- Structure de la table `scan`
--

DROP TABLE IF EXISTS `scan`;
CREATE TABLE IF NOT EXISTS `scan` (
  `id_area` int NOT NULL,
  `Id_Scan` int NOT NULL,
  `date_scan` datetime NOT NULL,
  PRIMARY KEY (`Id_Scan`),
  KEY `id_area` (`id_area`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `scan`
--

INSERT INTO `scan` (`id_area`, `Id_Scan`, `date_scan`) VALUES
(1, 1, '2024-05-06 13:40:15'),
(1, 2, '2024-05-02 20:50:03'),
(3, 3, '2024-05-07 14:30:05'),
(3, 4, '2024-05-07 15:30:05'),
(8, 5, '2024-05-15 05:43:54'),
(16, 6, '2024-05-18 11:53:07');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `Id_user` int NOT NULL,
  `Username` varchar(20) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `Password` varchar(20) NOT NULL,
  PRIMARY KEY (`Id_user`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`Id_user`, `Username`, `email`, `Password`) VALUES
(1, 'user', NULL, 'user'),
(2, 'sino06', 'yassinos20435121@gmail.com', 'abcd'),
(3, 'bounjeh', 'bounjeh@gmail.com', '1920'),
(4, 'rahim06', 'rahim@gmail.com', '1234');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `area`
--
ALTER TABLE `area`
  ADD CONSTRAINT `area_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`Id_user`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`id_routeer`) REFERENCES `routers` (`id_router`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`Id_user`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `routers`
--
ALTER TABLE `routers`
  ADD CONSTRAINT `routers_ibfk_1` FOREIGN KEY (`Id_scan`) REFERENCES `scan` (`Id_Scan`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `scan`
--
ALTER TABLE `scan`
  ADD CONSTRAINT `scan_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `area` (`id_area`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
