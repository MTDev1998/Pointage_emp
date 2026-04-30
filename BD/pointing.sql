-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 26 fév. 2025 à 22:34
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `pointing`
--

-- --------------------------------------------------------

--
-- Structure de la table `emp`
--

CREATE TABLE `emp` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `emp`
--

INSERT INTO `emp` (`id`, `name`, `email`, `phone`, `address`) VALUES
(1, 'tarek', 'Tarek moussaoui 1', '1', 'Permie d\'étude'),
(2, 'TAREK', 'MOUSSAOUI', '1', 'MOUSSAOUI TAREK STRITE'),
(4, 'tarek', 'Tarek moussaoui ', '1', 'tarek.moussaoui@univ-constantine2.dz'),
(5, 'tarek', 'tarek.moussaoui227@gmail.com', '1', 'Vvhhbvf'),
(6, 'tarek', 'T', '1', 'T'),
(7, 'tarek', 'Lala', '1', 'Kolala'),
(8, 'tarek', 'Salut', '1', 'Tata'),
(9, 'tarek', 'T', '1', 'T'),
(10, 'tarek', 'Y', '1', 'Y'),
(11, 'tarek', 'Brahim', '1', 'Khali'),
(12, 'tarek', 'Ghania Amarouche', '1', 'Amarouche');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `emp`
--
ALTER TABLE `emp`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `emp`
--
ALTER TABLE `emp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
