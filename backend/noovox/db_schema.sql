CREATE DATABASE IF NOT EXISTS `noovox`; USE `noovox`; CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); CREATE TABLE IF NOT EXISTS `chats` (
    `chat_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
); CREATE TABLE IF NOT EXISTS `chat_messages` (
    `message_id` INT AUTO_INCREMENT PRIMARY KEY,
    `chat_id` INT,
    `user_id` INT,
    `sender_type` ENUM('user', 'system', 'assistant') NOT NULL,
    `message_text` TEXT NOT NULL,
    `sent_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`chat_id`) REFERENCES `chats`(`chat_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
); CREATE TABLE IF NOT EXISTS `content_tracking` (
    `tracking_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT,
    `content_type` ENUM('view', 'like', 'analysis') NOT NULL,
    `content_id` INT NOT NULL,
    `tracked_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
);