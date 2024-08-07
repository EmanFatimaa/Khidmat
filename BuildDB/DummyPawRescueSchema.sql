USE [master]
GO
/****** Object:  Database [DummyPawRescue]    Script Date: 7/30/2024 8:16:08 PM ******/
CREATE DATABASE [DummyPawRescue]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'DummyPawRescue', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.FONTAINE\MSSQL\DATA\DummyPawRescue.mdf' , SIZE = 73728KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'DummyPawRescue_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.FONTAINE\MSSQL\DATA\DummyPawRescue_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [DummyPawRescue] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [DummyPawRescue].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [DummyPawRescue] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [DummyPawRescue] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [DummyPawRescue] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [DummyPawRescue] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [DummyPawRescue] SET ARITHABORT OFF 
GO
ALTER DATABASE [DummyPawRescue] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [DummyPawRescue] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [DummyPawRescue] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [DummyPawRescue] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [DummyPawRescue] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [DummyPawRescue] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [DummyPawRescue] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [DummyPawRescue] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [DummyPawRescue] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [DummyPawRescue] SET  DISABLE_BROKER 
GO
ALTER DATABASE [DummyPawRescue] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [DummyPawRescue] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [DummyPawRescue] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [DummyPawRescue] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [DummyPawRescue] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [DummyPawRescue] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [DummyPawRescue] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [DummyPawRescue] SET RECOVERY FULL 
GO
ALTER DATABASE [DummyPawRescue] SET  MULTI_USER 
GO
ALTER DATABASE [DummyPawRescue] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [DummyPawRescue] SET DB_CHAINING OFF 
GO
ALTER DATABASE [DummyPawRescue] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [DummyPawRescue] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [DummyPawRescue] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [DummyPawRescue] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'DummyPawRescue', N'ON'
GO
ALTER DATABASE [DummyPawRescue] SET QUERY_STORE = ON
GO
ALTER DATABASE [DummyPawRescue] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [DummyPawRescue]
GO
/****** Object:  Table [dbo].[Cage]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cage](
	[cageID] [int] NOT NULL,
	[wardID] [int] NULL,
	[cageStatusID] [int] NULL,
	[date] [date] NULL,
	[cageNo] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[cageID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[cageID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[cageStatus]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[cageStatus](
	[cageStatusID] [int] NOT NULL,
	[cageStatus] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[cageStatusID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[cageStatusID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Cats]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cats](
	[catID] [int] NOT NULL,
	[catName] [nvarchar](max) NULL,
	[age] [decimal](3, 2) NULL,
	[genderID] [int] NULL,
	[typeID] [int] NULL,
	[cageID] [int] NULL,
	[externalID] [int] NULL,
	[statusID] [int] NULL,
	[admittedOn] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[catID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[catID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CatStatus]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CatStatus](
	[StatusID] [int] NOT NULL,
	[statusType] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[StatusID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Donations]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Donations](
	[donationID] [int] NOT NULL,
	[donorID] [int] NULL,
	[modeID] [int] NULL,
	[amount] [int] NULL,
	[date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[donationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[donationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Externals]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Externals](
	[externalID] [int] NOT NULL,
	[name] [nvarchar](max) NOT NULL,
	[contactNum] [nvarchar](max) NOT NULL,
	[address] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[externalID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[externalID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Gender]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Gender](
	[genderID] [int] NOT NULL,
	[gender] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[genderID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[genderID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[InternalRole]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[InternalRole](
	[internalRoleID] [int] NOT NULL,
	[roleDesc] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[internalRoleID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[internalRoleID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Mode]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Mode](
	[modeID] [int] NOT NULL,
	[mode] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[modeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[modeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Revenue]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Revenue](
	[revenueID] [int] NOT NULL,
	[buyerID] [int] NULL,
	[modeID] [int] NULL,
	[date] [date] NULL,
	[amount] [int] NULL,
	[remarks] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[revenueID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[revenueID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Transactions]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Transactions](
	[transactionID] [int] NOT NULL,
	[modeID] [int] NULL,
	[amount] [int] NULL,
	[billFor] [nvarchar](max) NULL,
	[date] [date] NULL,
	[remarks] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[transactionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[transactionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Treatment]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Treatment](
	[treatmentID] [int] NOT NULL,
	[catID] [int] NULL,
	[userID] [int] NULL,
	[dateTime] [datetime] NULL,
	[temperature] [nvarchar](max) NULL,
	[treatment] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[treatmentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[treatmentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Type]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Type](
	[typeID] [int] NOT NULL,
	[type] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[typeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[typeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[userID] [int] NOT NULL,
	[userName] [nvarchar](max) NULL,
	[email] [nvarchar](max) NULL,
	[password] [nvarchar](max) NULL,
	[picture] [varbinary](max) NULL,
	[internalRoleID] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[userID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[userID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Ward]    Script Date: 7/30/2024 8:16:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ward](
	[wardID] [int] NOT NULL,
	[name] [nvarchar](max) NULL,
	[code] [nvarchar](max) NULL,
	[capacityCages] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[wardID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[wardID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[Cage]  WITH CHECK ADD  CONSTRAINT [Cage_fk1] FOREIGN KEY([wardID])
REFERENCES [dbo].[Ward] ([wardID])
GO
ALTER TABLE [dbo].[Cage] CHECK CONSTRAINT [Cage_fk1]
GO
ALTER TABLE [dbo].[Cage]  WITH CHECK ADD  CONSTRAINT [Cage_fk2] FOREIGN KEY([cageStatusID])
REFERENCES [dbo].[cageStatus] ([cageStatusID])
GO
ALTER TABLE [dbo].[Cage] CHECK CONSTRAINT [Cage_fk2]
GO
ALTER TABLE [dbo].[Cats]  WITH CHECK ADD  CONSTRAINT [Cats_fk3] FOREIGN KEY([genderID])
REFERENCES [dbo].[Gender] ([genderID])
GO
ALTER TABLE [dbo].[Cats] CHECK CONSTRAINT [Cats_fk3]
GO
ALTER TABLE [dbo].[Cats]  WITH CHECK ADD  CONSTRAINT [Cats_fk4] FOREIGN KEY([typeID])
REFERENCES [dbo].[Type] ([typeID])
GO
ALTER TABLE [dbo].[Cats] CHECK CONSTRAINT [Cats_fk4]
GO
ALTER TABLE [dbo].[Cats]  WITH CHECK ADD  CONSTRAINT [Cats_fk5] FOREIGN KEY([cageID])
REFERENCES [dbo].[Cage] ([cageID])
GO
ALTER TABLE [dbo].[Cats] CHECK CONSTRAINT [Cats_fk5]
GO
ALTER TABLE [dbo].[Cats]  WITH CHECK ADD  CONSTRAINT [Cats_fk6] FOREIGN KEY([externalID])
REFERENCES [dbo].[Externals] ([externalID])
GO
ALTER TABLE [dbo].[Cats] CHECK CONSTRAINT [Cats_fk6]
GO
ALTER TABLE [dbo].[Cats]  WITH CHECK ADD  CONSTRAINT [Cats_fk7] FOREIGN KEY([statusID])
REFERENCES [dbo].[CatStatus] ([StatusID])
GO
ALTER TABLE [dbo].[Cats] CHECK CONSTRAINT [Cats_fk7]
GO
ALTER TABLE [dbo].[Donations]  WITH CHECK ADD  CONSTRAINT [Donations_fk1] FOREIGN KEY([donorID])
REFERENCES [dbo].[Externals] ([externalID])
GO
ALTER TABLE [dbo].[Donations] CHECK CONSTRAINT [Donations_fk1]
GO
ALTER TABLE [dbo].[Donations]  WITH CHECK ADD  CONSTRAINT [Donations_fk2] FOREIGN KEY([modeID])
REFERENCES [dbo].[Mode] ([modeID])
GO
ALTER TABLE [dbo].[Donations] CHECK CONSTRAINT [Donations_fk2]
GO
ALTER TABLE [dbo].[Revenue]  WITH CHECK ADD  CONSTRAINT [Revenue_fk1] FOREIGN KEY([buyerID])
REFERENCES [dbo].[Externals] ([externalID])
GO
ALTER TABLE [dbo].[Revenue] CHECK CONSTRAINT [Revenue_fk1]
GO
ALTER TABLE [dbo].[Revenue]  WITH CHECK ADD  CONSTRAINT [Revenue_fk2] FOREIGN KEY([modeID])
REFERENCES [dbo].[Mode] ([modeID])
GO
ALTER TABLE [dbo].[Revenue] CHECK CONSTRAINT [Revenue_fk2]
GO
ALTER TABLE [dbo].[Transactions]  WITH CHECK ADD  CONSTRAINT [Transactions_fk1] FOREIGN KEY([modeID])
REFERENCES [dbo].[Mode] ([modeID])
GO
ALTER TABLE [dbo].[Transactions] CHECK CONSTRAINT [Transactions_fk1]
GO
ALTER TABLE [dbo].[Treatment]  WITH CHECK ADD  CONSTRAINT [Treatment_fk1] FOREIGN KEY([catID])
REFERENCES [dbo].[Cats] ([catID])
GO
ALTER TABLE [dbo].[Treatment] CHECK CONSTRAINT [Treatment_fk1]
GO
ALTER TABLE [dbo].[Treatment]  WITH CHECK ADD  CONSTRAINT [Treatment_fk2] FOREIGN KEY([userID])
REFERENCES [dbo].[Users] ([userID])
GO
ALTER TABLE [dbo].[Treatment] CHECK CONSTRAINT [Treatment_fk2]
GO
ALTER TABLE [dbo].[Users]  WITH CHECK ADD  CONSTRAINT [Users_fk5] FOREIGN KEY([internalRoleID])
REFERENCES [dbo].[InternalRole] ([internalRoleID])
GO
ALTER TABLE [dbo].[Users] CHECK CONSTRAINT [Users_fk5]
GO
USE [master]
GO
ALTER DATABASE [DummyPawRescue] SET  READ_WRITE 
GO
