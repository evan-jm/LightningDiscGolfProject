create table User
(
ID int auto_increment,
username varchar(20) not null default '',
first_name varchar(10),
last_name varchar(20),
email varchar(20) not null,
password varchar(20) not null,
    constraint User_PK primary key(ID)
);

insert into User Values (1,'test1','test','test','test@gmail.com','test');

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

insert into Admin values (1,'mattm','matt','myles','matt@gmail.com','pword');

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
    Cost varchar(20) not null,
    constraint Item_PK primary key(ItemID)
    );
    
create table Orders
(
Order_ID int not null auto_increment,
Order_Date date not null,
User_ID int,
constraint Orders_PK primary key(Order_ID),
constraint Orders_FK foreign key(User_ID) references User(ID)
);

create table Order_Line_Item
(
Order_ID int not null,
ItemID int,
Product_Quantity int not null,
constraint Order_Line_FK1 foreign key(Order_ID) references Orders(Order_ID),
constraint Order_Line_FK2 foreign key(ItemID) references Item(ItemID),
constraint Order_Line_PK primary key(Order_ID,ItemID)
);

create table Brands
(
Brand_ID int not null auto_increment,
BrandName varchar(15),
constraint Brands_PK primary key(Brand_ID)
);

create table DiscTypes
(
Type_ID int not null auto_increment,
TypeName varchar(20),
constraint DiscTypes_PK primary key(Type_ID)
);

insert into Brands values
(1, 'Discmania'),
(2, 'Innova'),
(3, 'Infinite'),
(4, 'Dynamic Discs');

insert into DiscTypes values
(1, 'Fairway Driver');

insert into Item values 
(1,'Felon1.JPG','Dynamic Discs','Fuzion','Fairway Driver', 'Item Description','2022-11-10','DDDistFusion',20.00),
(2,'Escape1.JPG','Dynamic Discs','Escape','Fairway Driver', 'Item Description','2022-10-15','DDDistEscape',20.00),
(3,'Truth1.JPG','Dynamic Discs','Truth','Fairway Driver', 'Item Description','2022-09-07','DDDistTruth',20.00),
(4,'Judge1.JPG','Dynamic Discs','Judge','Fairway Driver', 'Item Description','2022-10-07','DDDistJudge',20.00),
(5,'Culprit1.JPG','Dynamic Discs','Culprit','Fairway Driver', 'Item Description','2022-08-07','DDDistCulprit',20.00),
(6,'Harp1.JPG','Dynamic Discs','Harp','Fairway Driver', 'Item Description','2022-11-15','DDDistHarp',20.00),
(7,'Criminal1.JPG','Dynamic Discs','Criminal','Fairway Driver', 'Item Description','2022-09-07','DDDistCriminal',20.00),
(8,'Trespass1.JPG','Dynamic Discs','Tresspass','Fairway Driver', 'Item Description','2022-09-07','DDDistTrespass',20.00),
(9,'Raider1.JPG','Dynamic Discs','Raider','Fairway Driver', 'Item Description','2022-09-07','DDDistRaider',20.00);