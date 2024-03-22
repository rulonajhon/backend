-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 21, 2024 at 06:45 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crbs3`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `AdminID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`AdminID`, `Username`, `Password`) VALUES
(1, 'admin', 'adminpassword'),
(2, 'admin1', 'admin1pass'),
(3, 'admin2', 'admin2pass'),
(4, 'string', 'string');

-- --------------------------------------------------------

--
-- Table structure for table `bookinghistory`
--

CREATE TABLE `bookinghistory` (
  `HistoryID` int(11) NOT NULL,
  `BookingID` int(11) DEFAULT NULL,
  `StudentID` bigint(20) DEFAULT NULL,
  `RoomChoice` enum('room1','room2') DEFAULT NULL,
  `TimeIn` datetime NOT NULL,
  `TimeOut` datetime NOT NULL,
  `Companions` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookinghistory`
--

INSERT INTO `bookinghistory` (`HistoryID`, `BookingID`, `StudentID`, `RoomChoice`, `TimeIn`, `TimeOut`, `Companions`) VALUES
(2, 42, 234567890123, 'room2', '2024-03-21 09:00:00', '2024-03-21 11:00:00', 'Friend3, Friend4'),
(3, 45, 567890123456, 'room1', '2024-03-24 12:00:00', '2024-03-24 14:00:00', 'Friend8'),
(4, 47, 789012345678, 'room1', '2024-03-26 14:00:00', '2024-03-26 16:00:00', 'Friend10, Friend11');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `BookingID` int(11) NOT NULL,
  `StudentID` bigint(20) DEFAULT NULL,
  `RoomChoice` enum('Room1','Room2') NOT NULL,
  `TimeIn` datetime NOT NULL,
  `TimeOut` datetime NOT NULL,
  `Companions` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`BookingID`, `StudentID`, `RoomChoice`, `TimeIn`, `TimeOut`, `Companions`) VALUES
(41, 123456789012, 'Room1', '2024-03-20 08:00:00', '2024-03-20 10:00:00', 'Friend1, Friend2'),
(42, 234567890123, 'Room2', '2024-03-21 09:00:00', '2024-03-21 11:00:00', 'Friend3, Friend4'),
(43, 345678901234, 'Room1', '2024-03-22 10:00:00', '2024-03-22 12:00:00', 'Friend5'),
(44, 456789012345, 'Room2', '2024-03-23 11:00:00', '2024-03-23 13:00:00', 'Friend6, Friend7'),
(45, 567890123456, 'Room1', '2024-03-24 12:00:00', '2024-03-24 14:00:00', 'Friend8'),
(46, 678901234567, 'Room2', '2024-03-25 13:00:00', '2024-03-25 15:00:00', 'Friend9'),
(47, 789012345678, 'Room1', '2024-03-26 14:00:00', '2024-03-26 16:00:00', 'Friend10, Friend11'),
(48, 890123456789, 'Room2', '2024-03-27 15:00:00', '2024-03-27 17:00:00', 'Friend12'),
(49, 901234567890, 'Room1', '2024-03-28 16:00:00', '2024-03-28 18:00:00', 'Friend13, Friend14'),
(50, 123456789101, 'Room2', '2024-03-29 17:00:00', '2024-03-29 19:00:00', 'Friend15');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `StudentID` bigint(20) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`StudentID`, `Username`, `Password`, `Name`, `Email`) VALUES
(123456789012, 'student1', 'student1pass', 'John Doe', 'john@example.com'),
(123456789101, 'student10', 'student10pass', 'Andrew Taylor', 'andrew@example.com'),
(180000001856, 'rulonajhon', '12345rulona', 'Jhon Norban Rulona', 'jrulona_180000001856@uic.edu.ph'),
(220000001122, 'examplechuchu', '12345', 'Jade Doe', 'jadedoe@uic.edu.ph'),
(230000004455, 'example2', '123456', 'exam ple', 'example@uic.edu.ph'),
(234567890123, 'student2', 'student2pass', 'Jane Smith', 'jane@example.com'),
(345678901234, 'student3', 'student3pass', 'Alice Johnson', 'alice@example.com'),
(456789012345, 'student4', 'student4pass', 'Bob Williams', 'bob@example.com'),
(567890123456, 'student5', 'student5pass', 'Emily Brown', 'emily@example.com'),
(678901234567, 'student6', 'student6pass', 'Michael Davis', 'michael@example.com'),
(789012345678, 'student7', 'student7pass', 'Jessica Lee', 'jessica@example.com'),
(890123456789, 'student8', 'student8pass', 'David Martinez', 'david@example.com'),
(901234567890, 'student9', 'student9pass', 'Sophia Clark', 'sophia@example.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`AdminID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `bookinghistory`
--
ALTER TABLE `bookinghistory`
  ADD PRIMARY KEY (`HistoryID`),
  ADD KEY `BookingID` (`BookingID`),
  ADD KEY `StudentID` (`StudentID`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`BookingID`),
  ADD KEY `StudentID` (`StudentID`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`StudentID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `AdminID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `bookinghistory`
--
ALTER TABLE `bookinghistory`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `BookingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookinghistory`
--
ALTER TABLE `bookinghistory`
  ADD CONSTRAINT `bookinghistory_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`),
  ADD CONSTRAINT `bookinghistory_ibfk_2` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`);

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
