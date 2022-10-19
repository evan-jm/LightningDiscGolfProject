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

insert into Admin values (1,'mattm','matt','myles','matt@gmail.com','pword');