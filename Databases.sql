create table User
(
ID int not null auto_increment,
username varchar(20) not null default '',
first_name varchar(10),
last_name varchar(20),
email varchar(20) not null,
password varchar(20) not null,
    constraint User_PK primary key(ID)
);

create table Admin
(
ID int not null auto_increment,
username varchar(20) not null default '',
first_name varchar(10),
last_name varchar(20),
email varchar(20) not null,
password varchar(20) not null,
constraint User_PK primary key(ID)
);

create table Item
(
Brand varchar(15) not null,
Name varchar(15) not null,
Release_Date date not null,
Disc_Number int not null,
Abbreviation varchar(15) not null,
Cost decimal(10,2) not null,
constraint Item_PK primary key(Name)
);

create table Order
(
Order_ID int not null auto_increment,
Order_Date date not null,
Customer_ID int,
constraint Order_PK primary key(Order_ID),
constraint Order_FK foreign key(Customer_ID) references User(ID)
);

create table Order_Line
(
Order_ID int not null,
Product_Name varchar(15) not null,
Product_Quantity int(2) not null,
constraint Order_Line_FK foreign key(Order_ID) references Order(Order_ID)
);