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
ItemID int not null auto_increment,
Image varchar(255) not null,
Brand varchar(15) not null,
Name varchar(15) not null,
DiscType varchar(20),
Description text,
Release_Date date,
ItemCode varchar(15) not null,
Cost decimal(10,2) not null,
constraint Item_PK primary key(ItemID)
);

insert into Item values 
(1,'1.PNG','Discmania','Cloudbreaker','Distance', 'Item Description', null,'DMCB',50.00),
(2,'1.PNG','Discmania','Full Tilt','Fairway', 'Item Description', null,'DMFT',20.00),
(3,'1.PNG','Discmania','Breaker','Putter', 'Item Description', null,'DMBR',30.00);



create table Orders
(
Order_ID int not null auto_increment,
Order_Date date not null,
User_ID int,
constraint Order_PK primary key(Order_ID),
constraint Order_FK foreign key(Customer_ID) references User(ID)
);

create table Order_Line_Item
(
Order_ID int not null,
ItemID int not null,
Product_Quantity int not null,
constraint Order_Line_FK1 foreign key(Order_ID) references Orders(Order_ID),
constraint Order_Line_FK2 foreign key(ItemID) references Item(ItemID),
constraint Order_Line_PK primary key(Order_ID,Item_ID)
);