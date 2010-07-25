-- Table structure for table `clantags`
--

CREATE TABLE IF NOT EXISTS `clantags` (
  `clan` varchar(256) NOT NULL COMMENT 'Clan Name, presentable format',
  `tag regex` varchar(256) NOT NULL,
  `contact` varchar(256) NOT NULL COMMENT 'How to reach the clan',
  KEY `tag regex` (`tag regex`)
);

--
-- sample data for table `clantags`
--

INSERT INTO `clantags` (`clan`, `tag regex`, `contact`) VALUES
('Mapping Hell', '/\\[MH.?\\](.*)/', 'MappingHell.net');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user` varchar(256) NOT NULL,
  `key` varchar(256) NOT NULL DEFAULT 'privileges',
  `value` varchar(256) NOT NULL DEFAULT 'trusted',
  KEY `user` (`user`,`key`)
);

--
-- add first user in table `users`
--

INSERT INTO `users` (`user`, `key`, `value`) VALUES
('firstuser', 'privileges', 'admin'),
('firstuser', 'password', '25dcea7702a33590fbc3b77fca5c7e4185bf695016c6aac206732f2f');
