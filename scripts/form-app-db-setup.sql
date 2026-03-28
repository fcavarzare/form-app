-- =============================================================
-- form-app: Script de criação de banco, usuários e schema
-- SQL Server (100.100.100.104)
-- Ambientes: dev, qa, prod
-- Executar como SA ou sysadmin
-- =============================================================

-- -----------------------------------------------
-- DEV
-- -----------------------------------------------
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'appdb_dev')
BEGIN
    CREATE DATABASE appdb_dev;
    PRINT 'Database appdb_dev criado.';
END
GO

USE appdb_dev;
GO

IF NOT EXISTS (SELECT name FROM sys.tables WHERE name = 'FormData')
BEGIN
    CREATE TABLE FormData (
        Id       INT           IDENTITY(1,1) PRIMARY KEY,
        Nome     NVARCHAR(150) NOT NULL,
        Email    NVARCHAR(255) NOT NULL,
        Mensagem NVARCHAR(MAX) NOT NULL
    );
    PRINT 'Tabela FormData criada em appdb_dev.';
END
GO

IF NOT EXISTS (SELECT name FROM sys.server_principals WHERE name = 'formapp_dev')
BEGIN
    CREATE LOGIN formapp_dev WITH PASSWORD = 'SenhaDev@123';
    PRINT 'Login formapp_dev criado.';
END
GO

IF NOT EXISTS (SELECT name FROM sys.database_principals WHERE name = 'formapp_dev')
BEGIN
    CREATE USER formapp_dev FOR LOGIN formapp_dev;
    ALTER ROLE db_datareader ADD MEMBER formapp_dev;
    ALTER ROLE db_datawriter ADD MEMBER formapp_dev;
    PRINT 'User formapp_dev criado e permissões concedidas em appdb_dev.';
END
GO

-- -----------------------------------------------
-- QA
-- -----------------------------------------------
USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'appdb_qa')
BEGIN
    CREATE DATABASE appdb_qa;
    PRINT 'Database appdb_qa criado.';
END
GO

USE appdb_qa;
GO

IF NOT EXISTS (SELECT name FROM sys.tables WHERE name = 'FormData')
BEGIN
    CREATE TABLE FormData (
        Id       INT           IDENTITY(1,1) PRIMARY KEY,
        Nome     NVARCHAR(150) NOT NULL,
        Email    NVARCHAR(255) NOT NULL,
        Mensagem NVARCHAR(MAX) NOT NULL
    );
    PRINT 'Tabela FormData criada em appdb_qa.';
END
GO

IF NOT EXISTS (SELECT name FROM sys.server_principals WHERE name = 'formapp_qa')
BEGIN
    CREATE LOGIN formapp_qa WITH PASSWORD = 'SenhaQa@123';
    PRINT 'Login formapp_qa criado.';
END
GO

IF NOT EXISTS (SELECT name FROM sys.database_principals WHERE name = 'formapp_qa')
BEGIN
    CREATE USER formapp_qa FOR LOGIN formapp_qa;
    ALTER ROLE db_datareader ADD MEMBER formapp_qa;
    ALTER ROLE db_datawriter ADD MEMBER formapp_qa;
    PRINT 'User formapp_qa criado e permissões concedidas em appdb_qa.';
END
GO

-- -----------------------------------------------
-- PROD
-- -----------------------------------------------
USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'appdb_prod')
BEGIN
    CREATE DATABASE appdb_prod;
    PRINT 'Database appdb_prod criado.';
END
GO

USE appdb_prod;
GO

IF NOT EXISTS (SELECT name FROM sys.tables WHERE name = 'FormData')
BEGIN
    CREATE TABLE FormData (
        Id       INT           IDENTITY(1,1) PRIMARY KEY,
        Nome     NVARCHAR(150) NOT NULL,
        Email    NVARCHAR(255) NOT NULL,
        Mensagem NVARCHAR(MAX) NOT NULL
    );
    PRINT 'Tabela FormData criada em appdb_prod.';
END
GO

IF NOT EXISTS (SELECT name FROM sys.server_principals WHERE name = 'formapp_prod')
BEGIN
    CREATE LOGIN formapp_prod WITH PASSWORD = 'SenhaProd@123';
    PRINT 'Login formapp_prod criado.';
END
GO

IF NOT EXISTS (SELECT name FROM sys.database_principals WHERE name = 'formapp_prod')
BEGIN
    CREATE USER formapp_prod FOR LOGIN formapp_prod;
    ALTER ROLE db_datareader ADD MEMBER formapp_prod;
    ALTER ROLE db_datawriter ADD MEMBER formapp_prod;
    PRINT 'User formapp_prod criado e permissões concedidas em appdb_prod.';
END
GO

PRINT '=== Setup concluído para dev, qa e prod ===';
