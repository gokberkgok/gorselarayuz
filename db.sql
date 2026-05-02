-- phpMyAdmin SQL Dump
-- version 5.2.1
-- Host: localhost
-- Generation Time: May 02, 2026
-- Server version: 10.4.28-MariaDB (Typical XAMPP)
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rezervasyon_db`
--
CREATE DATABASE IF NOT EXISTS `rezervasyon_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `rezervasyon_db`;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
-- (Password is hashed 'admin123' using bcrypt)
--
INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'Admin', 'admin@admin.com', '$2b$12$L7R2Qo190mE4Ew64O9zP3e9L9q9o9u9t9s9e9c9r9e9t9k9e9y9h9', 'admin', current_timestamp());

-- --------------------------------------------------------

--
-- Table structure for table `types`
--
CREATE TABLE `types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_types_name` (`name`),
  KEY `ix_types_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `types`
--
INSERT INTO `types` (`id`, `name`) VALUES
(1, 'Hotel'),
(2, 'Restaurant'),
(3, 'Room'),
(4, 'Cafe'),
(5, 'Spa');

-- --------------------------------------------------------

--
-- Table structure for table `places`
--
CREATE TABLE `places` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `type_id` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `image_url` varchar(500) DEFAULT '',
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_by` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_places_id` (`id`),
  KEY `type_id` (`type_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `places_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`),
  CONSTRAINT `places_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `places`
--
INSERT INTO `places` (`id`, `name`, `type_id`, `description`, `image_url`, `is_active`, `created_by`, `created_at`) VALUES
(1, 'Grand Palace Hotel', 1, 'Luxury 5-star hotel with panoramic city views, indoor pool, and world-class dining.', '', 1, 1, current_timestamp()),
(2, 'Seaside Resort & Spa', 1, 'Beachfront resort offering premium suites, private beach access, and full spa services.', '', 1, 1, current_timestamp()),
(3, 'La Bella Cucina', 2, 'Authentic Italian fine dining with handmade pasta, wood-fired pizza, and curated wine list.', '', 1, 1, current_timestamp()),
(4, 'Sakura Sushi Bar', 2, 'Premium Japanese cuisine with fresh sashimi, omakase menu, and sake bar.', '', 1, 1, current_timestamp()),
(5, 'The Grill House', 2, 'Upscale steakhouse featuring dry-aged cuts, craft cocktails, and live jazz.', '', 1, 1, current_timestamp()),
(6, 'Executive Meeting Room A', 3, 'Modern meeting room for up to 20 people with projector, whiteboard, and video conferencing.', '', 1, 1, current_timestamp()),
(7, 'Creative Studio B', 3, 'Bright co-working space with flexible seating, high-speed Wi-Fi, and coffee bar.', '', 1, 1, current_timestamp()),
(8, 'Artisan Coffee Lab', 4, 'Specialty coffee roastery with single-origin beans, pastries, and cozy reading nooks.', '', 1, 1, current_timestamp()),
(9, 'Garden Tea House', 4, 'Tranquil tea house with over 50 premium teas, outdoor garden seating, and live acoustic music.', '', 1, 1, current_timestamp()),
(10, 'Serenity Wellness Center', 5, 'Full-service spa offering massage therapy, hot stone treatments, and aromatherapy sessions.', '', 1, 1, current_timestamp());

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--
CREATE TABLE `reservations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `place_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `status` enum('pending','approved','cancelled','rejected') NOT NULL DEFAULT 'pending',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_reservations_id` (`id`),
  KEY `user_id` (`user_id`),
  KEY `place_id` (`place_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
