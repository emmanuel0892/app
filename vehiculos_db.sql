CREATE DATABASE autos_db;

USE autos_db;

CREATE TABLE vehiculos(
	id_patente varchar(50) primary key not null,
	chasis int,
	año date,
	marca varchar(50),
	modelo varchar(50),
	color varchar(50),
	TieneSeguro boolean
);
