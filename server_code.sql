CREATE TABLE `endreason` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `description` VARCHAR(255) NOT NULL
);

CREATE TABLE `networknode` (
  `ip` VARCHAR(255) NOT NULL,
  `port` INTEGER NOT NULL,
  PRIMARY KEY (`ip`, `port`)
);

CREATE TABLE `protocol` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `flow` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `end_reason` INTEGER,
  `category` VARCHAR(255) NOT NULL,
  `application_protocol` VARCHAR(255) NOT NULL,
  `web_service` VARCHAR(255) NOT NULL,
  `src_node_ip` VARCHAR(255) NOT NULL,
  `src_node_port` INTEGER NOT NULL,
  `dest_node_ip` VARCHAR(255) NOT NULL,
  `dest_node_port` INTEGER NOT NULL,
  `protocol_id` INTEGER,
  `end_reason_id` INTEGER
);

CREATE INDEX `idx_flow__dest_node_ip_dest_node_port` ON `flow` (`dest_node_ip`, `dest_node_port`);

CREATE INDEX `idx_flow__end_reason_id` ON `flow` (`end_reason_id`);

CREATE INDEX `idx_flow__protocol_id` ON `flow` (`protocol_id`);

CREATE INDEX `idx_flow__src_node_ip_src_node_port` ON `flow` (`src_node_ip`, `src_node_port`);

ALTER TABLE `flow` ADD CONSTRAINT `fk_flow__dest_node_ip__dest_node_port` FOREIGN KEY (`dest_node_ip`, `dest_node_port`) REFERENCES `networknode` (`ip`, `port`) ON DELETE CASCADE;

ALTER TABLE `flow` ADD CONSTRAINT `fk_flow__end_reason_id` FOREIGN KEY (`end_reason_id`) REFERENCES `endreason` (`id`) ON DELETE SET NULL;

ALTER TABLE `flow` ADD CONSTRAINT `fk_flow__protocol_id` FOREIGN KEY (`protocol_id`) REFERENCES `protocol` (`id`) ON DELETE SET NULL;

ALTER TABLE `flow` ADD CONSTRAINT `fk_flow__src_node_ip__src_node_port` FOREIGN KEY (`src_node_ip`, `src_node_port`) REFERENCES `networknode` (`ip`, `port`) ON DELETE CASCADE;

CREATE TABLE `packetinfo` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `flow_id` INTEGER NOT NULL,
  `packet_total_count` INTEGER,
  `octet_total_count` INTEGER,
  `min_pkt_size` DOUBLE,
  `max_pkt_size` DOUBLE,
  `avg_pkt_size` DOUBLE,
  `stdev_pkt_size` DOUBLE
);

CREATE INDEX `idx_packetinfo__flow_id` ON `packetinfo` (`flow_id`);

ALTER TABLE `packetinfo` ADD CONSTRAINT `fk_packetinfo__flow_id` FOREIGN KEY (`flow_id`) REFERENCES `flow` (`id`)
