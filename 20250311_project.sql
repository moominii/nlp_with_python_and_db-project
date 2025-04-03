create database text_analysis;

use text_analysis;

create table stopwords (
	id int auto_increment primary key,
    word varchar(50) not null unique
);

create table extra_words (
	id int auto_increment primary key,
    word varchar(50) not null unique
);

INSERT INTO stopwords (word) VALUES
('그리고'), ('하지만'), ('것이다'), ('있다'), ('없다');

INSERT INTO extra_words (word) VALUES
('쌍꺼풀'), ('코성형'), ('턱라인'), ('눈매교정');

create database travel_analysis;

use travel_analysis;

create table stopwords_jeju (
	id int auto_increment primary key,
    word varchar(50) not null unique
);

INSERT INTO stopwords_jeju (word) VALUES
('추천'), ('검색'), ('코스'), ('숙소'), ('입장료'), ('가격'),
('이용'), ('도움'), ('위치'), ('첫째날'), ('둘째날'), ('할인'),
('렌트카'), ('소요'), ('항공사'), ('사진'), ('무료 체험');

create database tourism_analysis;

use tourism_analysis;

create table stopwords (
	id int auto_increment primary key,
    word varchar(255) unique not null
);

create table additional_words (
	id int auto_increment primary key,
    word varchar(255) unique not null
); 


create database speech_analysis;

use speech_analysis;

create table stopwords (
	id int auto_increment primary key,
    word varchar(255) unique not null
);

drop database text_analysis;



drop database travel_analysis;

drop database tourism_analysis;

drop database speech_analysis;

drop database test_index;

drop database us_stock;








