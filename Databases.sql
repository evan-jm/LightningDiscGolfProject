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
    ALTER TABLE User AUTO_INCREMENT=10001;
    
    insert into User Values (default,'test1','test','test','test@gmail.com','test');
   insert into User Values (default,'joes','test','test','test@gmail.com','test');

    create table Guest
    (
	ID int auto_increment,
    first_name varchar(10),
    last_name varchar(20),
    email varchar(20) not null,
    Use_Time datetime,
    constraint Guest_PK primary key(ID)
    );
    ALTER TABLE Guest AUTO_INCREMENT=20001;
    insert into Guest Values (default,'Mike','Deer','mdeer@gmail.com', current_timestamp() );
    
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
    
    insert into Admin Values (default,'admin','Matt','Myles','matt@gmail.com','pword');
    
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
Guest_ID int,
Address varchar(30),
Order_Total decimal not null,
Total_Quantity int not null,
constraint Orders_PK primary key(Order_ID),
constraint Orders_FK1 foreign key(User_ID) references User(ID),
constraint Orders_FK2 foreign key(Guest_ID) references Guest(ID)
);

insert into Orders Values(default,'2022-12-04',10001,NULL,'225 Street',40.00,2);
insert into Orders Values(default,'2022-12-04',NULL,20001,'225 Street',24.00,1);

create table Order_Line_Item
(
Order_ID int not null,
ItemID int,
Product_Quantity int not null,
Cost_Total decimal not null,
constraint Order_Line_FK1 foreign key(Order_ID) references Orders(Order_ID),
constraint Order_Line_FK2 foreign key(ItemID) references Item(ItemID),
constraint Order_Line_PK primary key(Order_ID,ItemID)
);

insert into Order_Line_Item Values(1,2,1,20);
insert into Order_Line_Item Values(1,3,1,20);
insert into Order_Line_Item Values(2,2,1,20);



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
(3, 'Infinite');

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

UPDATE Item SET Description = "Nothing throws off your game quite like the wind. We're not figuratively talking, though: wind alters where your shot goes, adding an extra variable and increasing unpredictability out on the course.

After playing in the strong Kansas winds in our hometown of Emporia, Dynamic Discs knew we had to develop a disc golf disc specifically for this challenge. Enter the Felon, a fairway driver that feels great in your hand and comes out easy.

This wind-fighting fairway driver will continue to sail, without turning over, despite the headwind that is challenging your confidence. When the wind is down, it has an incredibly predictable hyzer finish. When you are facing a low ceiling shot where you need good glide and a strong finish the Felon is your answer. You asked, and Dynamic Discs has delivered.

Speed: 9 Glide: 3 Turn: 0.5 Fade: 4
Max Weight: 176g" WHERE ItemID = 1;
UPDATE Item SET Description = "One word can summarize the Escape, glide. The description cannot stop there, however. The Escape is a fantastic disc for all levels of skill, power, and distance. It has such an easy release and the glide will keep this disc going even when less power is applied. It can fly on all angles and is even extremely useful as a roller. Break away from your expectations and escape your high scores of the past. Throw with confidence. Throw the Escape.

Speed: 9 Glide: 5 Turn: -1 Fade: 2
Max Weight: 175g" WHERE ItemID = 2;
UPDATE Item SET Description = "Walt Whitman said, 'Whatever satisfies the soul is truth.' The EMAC Truth is here to bring satisfaction to your golf game. The Truth had lost its way and wasn't as stable as we wanted it to be. The EMAC Truth sets the record straight. The beautifully neutral and versatile flight of this disc will remind you of the core of disc golf; to throw a disc where you want it to go. Let the EMAC Truth take you back to this satisfying feeling. May the Truth be with you. Signature disc for 2010 World Champion, Eric McCabe

Speed: 5 Glide: 5 Turn: 0 Fade: 2
Max Weight: 180g" WHERE ItemID = 3;
UPDATE Item SET Description = "Why was the Judge named the 2013 Disc of the Year in the Player's Choice Awards? It is incredibly predictable in flying and hitting the chains. It is a fantastic throwing putter that will fly straight and glide for amazing distances. It comes in 7 different plastics so that your preferred feel is available in this disc. Come see why this disc has become so popular and judged other, more well-known discs, to be insufficient.

Speed: 2 Glide: 4 Turn: 0 Fade: 1
Max Weight: 176g" WHERE ItemID = 4;
UPDATE Item SET Description = "The Culprit is a great upshot and approach disc. It can handle any arm speed and holds up well in a headwind. It has a very low profile and small diameter, making it perfect for players with smaller hands who want some beef on their approaches. We suspect you will realize the Culprit is responsible for your improved scores.

Speed: 4 Glide: 2 Turn: 0 Fade: 3.5
Max Weight: 176g" WHERE ItemID = 5;
UPDATE Item SET Description = "The Harp is our most reliable approach disc. Designed to withstand any type of condition. It will hold in the wind. For professional players, this could be their only approach disc they will need to carry as it can hold anyone's arm speed and still hyzer. For slower arm speeds, it will be your most overstable approach disc.

Speed: 4 Glide: 3 Turn: 0 Fade: 3" WHERE ItemID = 6;
UPDATE Item SET Description = "'Bad company corrupts good morals' has been proven true through the ages. However, Dynamic Discs is bringing you a Criminal that you are going to want to get to know. With more glide than the Felon and more stability than the Convict, this Criminal is exactly what you need to assault your high scores. The fairway driver that will be able to trust to cover the ground necessary without giving up the stability you need for confident throws. Befriend this Criminal and you will start to do some bad things to your course. 

Speed: 10 Glide: 3 Turn: 1 Fade: 4 
Max Weight: 176g" WHERE ItemID = 7;
UPDATE Item SET Description = "The Trespass is the high-speed driver for the masses. It is very neutral in its flight, not being too stable or flipping over. The wide rim is able to take all the power that you can throw at it and just keep gliding to new distances. The Trespass will allow you to break through all obstacles and explore new territory in your distance drives.

Speed: 12 Glide: 5 Turn: -0.5 Fade: 3" WHERE ItemID = 8;
UPDATE Item SET Description = "The Raider is sure to steal its spot in bags of all skill levels. The Raider sits comfortably between the Trespass and Enforcer in stability, and it excels at finishing forward instead of diving at the end of its flight. Players with slower arm speeds will find a dependable, overstable driver that will gain them distance over the Enforcer or Defender, while faster arms will love the Raider as a workhorse driver that is perfect for carrying multiples to cover a variety of shots. Get ready to put some power on your distance shots, and watch the Raider destroy your previous best drives.

Speed: 13 Glide: 5 Turn: -0.5 Fade: 3" WHERE ItemID = 9;



insert into Brands values
(1, 'Discmania'),
(2, 'Innova'),
(3, 'Infinite'),
(4, 'Dynamic Discs');

insert into DiscTypes values
(1, 'Fairway Driver');
