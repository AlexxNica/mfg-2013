drop table glyph;
drop table glyphoutline;
drop table glyphparam;
drop table master;
drop table globalparam;
drop table localparam;
drop table groupparam;

CREATE TABLE glyph (
    idglyph INT AUTO_INCREMENT,
    glyphName varchar(3),
    width integer,
    unicode TEXT,
    primary key (idglyph)
);
CREATE TABLE glyphoutline (
    id INT ,
    glyphName VARCHAR(3),
    PointNr VARCHAR(4),
    x integer,
    y integer, 
    contrp integer default 0,
    idmaster INT,
    pip INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,id,glyphName)
);
CREATE TABLE glyphparam (
    id INT ,
    glyphName VARCHAR(3),
    PointName VARCHAR(5),
    groupname VARCHAR(10),
    startp INT,
    doubledash INT,
    tripledash INT,
    superleft float,
    superright float,
    leftp   INT,
    rightp  INT,
    downp   INT,
    upp     INT,
    dir     varchar(30),
    leftp2   INT,
    rightp2  INT,
    downp2   INT,
    upp2     INT,
    dir2     varchar(30),
    tension INT, 
    tensionand varchar(10),
    cycle     INT,
    penshifted varchar(30), 
    pointshifted varchar(30),
    angle varchar(30), 
    penwidth varchar(30),
    overx VARCHAR(10), 
    overbase VARCHAR(10),  
    overcap VARCHAR(10), 
    overasc VARCHAR(10), 
    overdesc VARCHAR(10), 
    stemcutter float,
    stemshift float,
    inktrap_l float,
    inktrap_r float,   
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,id,glyphName)
);
CREATE TABLE groupparam (
    groupname varchar(10), 
    startp INT,
    doubledash INT,
    tripledash INT,
    superleft float,
    superright float,
    leftp   INT,
    rightp  INT,
    downp   INT,
    upp     INT,
    dir     varchar(30),
    leftp2   INT,
    rightp2  INT,
    downp2   INT,
    upp2     INT,
    dir2     float,
    tension INT, 
    tensionand varchar(10),
    cycle     INT,
    penshifted varchar(30), 
    pointshifted varchar(30),
    superness INT, 
    angle varchar(30),
    penwidth float,
    overx VARCHAR(10), 
    overbase VARCHAR(10),  
    overcap VARCHAR(10), 
    overasc VARCHAR(10), 
    overdesc VARCHAR(10), 
    stemcutter float,
    stemshift float,
    inktrap_l float,
    inktrap_r float,   
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,groupname)
);
CREATE TABLE master (
    idmaster INT AUTO_INCREMENT,
    FontName TEXT,
    FontNameA varchar(30),
    FontNameB varchar(30),
    idglobal INT, 
    vdate    TIMESTAMP default now(),
    primary key (idmaster)
);
CREATE TABLE globalparam (
    idglobal INT ,
    metapolation float,
    unitwidth float,
    fontsize  integer default 10,
    mean      float default 5.0,
    cap       float default 8.0,
    ascl       float default 2.0,
    des       float default 2.0,
    box       float default 10,
    primary key (idglobal)
);
CREATE TABLE localparam (
    idlocal INT ,
    px        float default 0.1,
    width  float default 1,
	space  float default 0,
    xheight   float default 5.0,
    capital   float default 8.0,
    boxheight   float default 10.0,
    ascender   float default 8.0,
    descender  float default 2.0,
    inktrap    integer default 10,
    stemcut   integer default 20,
    skeleton  float default 0.0,
    superness float default 1.0,
	over float default 0.1,
    primary key (idlocal)
);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("Foxtail", "FoxtailA.ufo","FoxtailA.ufo",1);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("My First Metapolator Font", "GaramondSansA.ufo","GaramondSansB.ufo",2);
insert into globalparam (idglobal,metapolation,unitwidth,fontsize) Values (1, 0.5,1,10);
insert into globalparam (idglobal,metapolation,unitwidth,fontsize) Values (2, 0.5,1,10);
insert into localparam (idlocal) values (1);
insert into localparam (idlocal) values (2);
insert into localparam (idlocal) values (3);
insert into localparam (idlocal) values (4);
