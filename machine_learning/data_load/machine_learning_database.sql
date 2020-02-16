USE [master]
GO
/****** Object:  Database [machine_learning_pr]    Script Date: 2/16/2020 6:20:22 PM ******/
CREATE DATABASE [machine_learning_pr]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'machine_learning_pr', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS\MSSQL\DATA\machine_learning_pr.mdf' , SIZE = 729088KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'machine_learning_pr_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS\MSSQL\DATA\machine_learning_pr_log.ldf' , SIZE = 1056768KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO
ALTER DATABASE [machine_learning_pr] SET COMPATIBILITY_LEVEL = 140
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [machine_learning_pr].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [machine_learning_pr] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [machine_learning_pr] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [machine_learning_pr] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [machine_learning_pr] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [machine_learning_pr] SET ARITHABORT OFF 
GO
ALTER DATABASE [machine_learning_pr] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [machine_learning_pr] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [machine_learning_pr] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [machine_learning_pr] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [machine_learning_pr] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [machine_learning_pr] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [machine_learning_pr] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [machine_learning_pr] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [machine_learning_pr] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [machine_learning_pr] SET  DISABLE_BROKER 
GO
ALTER DATABASE [machine_learning_pr] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [machine_learning_pr] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [machine_learning_pr] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [machine_learning_pr] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [machine_learning_pr] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [machine_learning_pr] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [machine_learning_pr] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [machine_learning_pr] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [machine_learning_pr] SET  MULTI_USER 
GO
ALTER DATABASE [machine_learning_pr] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [machine_learning_pr] SET DB_CHAINING OFF 
GO
ALTER DATABASE [machine_learning_pr] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [machine_learning_pr] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [machine_learning_pr] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [machine_learning_pr] SET QUERY_STORE = OFF
GO
USE [machine_learning_pr]
GO
/****** Object:  Table [dbo].[precipitation_data]    Script Date: 2/16/2020 6:20:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[precipitation_data](
	[site_id] [varchar](50) NULL,
	[source] [varchar](50) NULL,
	[date_time] [datetime2](7) NULL,
	[review_stage] [varchar](50) NULL,
	[atmospheric_temperature] [decimal](5, 2) NULL,
	[atmospheric_temperature_flag] [varchar](50) NULL,
	[relative_humidity] [decimal](5, 2) NULL,
	[relative_humidity_flag] [varchar](50) NULL,
	[barometric_pressure] [decimal](6, 2) NULL,
	[barometric_pressure_flag] [varchar](50) NULL,
	[wind_speed] [decimal](5, 2) NULL,
	[wind_speed_flag] [varchar](50) NULL,
	[total_PAR] [decimal](9, 2) NULL,
	[total_PAR_flag] [varchar](50) NULL,
	[total_precipitation] [decimal](5, 2) NULL,
	[total_precipitation_flag] [varchar](50) NULL,
	[total_solar_radiation] [decimal](9, 2) NULL,
	[total_solar_radiation_flag] [varchar](50) NULL,
	[timezone] [varchar](50) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[site]    Script Date: 2/16/2020 6:20:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[site](
	[site_id] [varchar](50) NOT NULL,
	[site_name] [varchar](50) NULL,
	[site_type] [varchar](50) NULL,
	[location] [varchar](50) NULL,
	[latitude] [decimal](12, 9) NULL,
	[longitude] [decimal](12, 9) NULL,
	[source] [varchar](50) NULL,
	[datum] [varchar](50) NULL,
	[vertical_datum] [varchar](50) NULL,
	[gage_altitude] [decimal](6, 2) NULL,
	[hole_depth] [decimal](6, 2) NULL,
	[well_depth] [decimal](6, 2) NULL,
	[hydrologic_unit] [varchar](50) NULL,
	[local_aquifer] [varchar](50) NULL,
	[aquifer_type] [varchar](50) NULL,
	[description] [text] NULL,
 CONSTRAINT [PK_site] PRIMARY KEY CLUSTERED 
(
	[site_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[water_nutrient_data]    Script Date: 2/16/2020 6:20:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[water_nutrient_data](
	[site_id] [varchar](50) NULL,
	[date_time] [datetime2](7) NULL,
	[review_stage] [varchar](50) NULL,
	[source] [varchar](50) NULL,
	[timezone] [varchar](50) NULL,
	[orthophosphate] [decimal](8, 4) NULL,
	[orthophosphate_flag] [varchar](50) NULL,
	[ammonium] [decimal](8, 4) NULL,
	[ammonium_flag] [varchar](50) NULL,
	[nitrite] [decimal](8, 4) NULL,
	[nitrite_flag] [varchar](50) NULL,
	[nitrate] [decimal](8, 4) NULL,
	[nitrate_flag] [varchar](50) NULL,
	[nitrite_nitrate] [decimal](8, 4) NULL,
	[nitrite_nitrate_flag] [varchar](50) NULL,
	[chlorophyll] [decimal](6, 2) NULL,
	[chlorophyll_flag] [varchar](50) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[water_quality_data]    Script Date: 2/16/2020 6:20:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[water_quality_data](
	[site_id] [varchar](50) NULL,
	[date_time] [datetime2](7) NULL,
	[timezone] [varchar](50) NULL,
	[review_stage] [varchar](50) NULL,
	[source] [varchar](50) NULL,
	[temperature] [decimal](5, 2) NULL,
	[temperature_flag] [varchar](50) NULL,
	[specific_conductivity] [decimal](5, 2) NULL,
	[specific_conductivity_flag] [varchar](50) NULL,
	[salinity] [decimal](5, 2) NULL,
	[salinity_flag] [varchar](50) NULL,
	[dissolved_oxygen_percent] [decimal](5, 2) NULL,
	[dissolved_oxygen_percent_flag] [varchar](50) NULL,
	[dissolved_oxygen] [decimal](5, 2) NULL,
	[dissolved_oxygen_flag] [varchar](50) NULL,
	[depth] [decimal](5, 2) NULL,
	[depth_flag] [varchar](50) NULL,
	[pH] [decimal](5, 2) NULL,
	[pH_flag] [varchar](50) NULL,
	[turbidity] [decimal](9, 2) NULL,
	[turbidity_flag] [varchar](50) NULL,
	[chlorophyll_fluorescence] [decimal](6, 2) NULL,
	[chlorophyll_fluorescence_flag] [varchar](50) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[well_data]    Script Date: 2/16/2020 6:20:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[well_data](
	[site_id] [varchar](50) NULL,
	[date_time] [datetime2](7) NULL,
	[timezone] [varchar](50) NULL,
	[review_stage] [varchar](50) NULL,
	[source] [varchar](50) NULL,
	[water_level_depth] [decimal](6, 2) NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[precipitation_data]  WITH CHECK ADD  CONSTRAINT [FK_precipitation_data_site] FOREIGN KEY([site_id])
REFERENCES [dbo].[site] ([site_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[precipitation_data] CHECK CONSTRAINT [FK_precipitation_data_site]
GO
ALTER TABLE [dbo].[water_nutrient_data]  WITH CHECK ADD  CONSTRAINT [FK_water_nutrient_data_site] FOREIGN KEY([site_id])
REFERENCES [dbo].[site] ([site_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[water_nutrient_data] CHECK CONSTRAINT [FK_water_nutrient_data_site]
GO
ALTER TABLE [dbo].[water_quality_data]  WITH CHECK ADD  CONSTRAINT [FK_water_quality_data_site] FOREIGN KEY([site_id])
REFERENCES [dbo].[site] ([site_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[water_quality_data] CHECK CONSTRAINT [FK_water_quality_data_site]
GO
ALTER TABLE [dbo].[well_data]  WITH CHECK ADD  CONSTRAINT [FK_well_data_site] FOREIGN KEY([site_id])
REFERENCES [dbo].[site] ([site_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[well_data] CHECK CONSTRAINT [FK_well_data_site]
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Site to time series relation' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'precipitation_data', @level2type=N'CONSTRAINT',@level2name=N'FK_precipitation_data_site'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Site to time series relation' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'water_nutrient_data', @level2type=N'CONSTRAINT',@level2name=N'FK_water_nutrient_data_site'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Site to time series relation' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'water_quality_data', @level2type=N'CONSTRAINT',@level2name=N'FK_water_quality_data_site'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Site to time series relation' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'well_data', @level2type=N'CONSTRAINT',@level2name=N'FK_well_data_site'
GO
USE [master]
GO
ALTER DATABASE [machine_learning_pr] SET  READ_WRITE 
GO
