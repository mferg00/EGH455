USE sensors;
SELECT * FROM Labels;
SELECT Dangerous, Corrosive, Aruco FROM Labels ORDER BY Time DESC LIMIT 1;
SELECT * FROM UAVSensors;
INSERT INTO Labels (Time, Dangerous, Corrosive,Aruco) VALUES (3.6,0,1,'[0,999]');
DELETE FROM Labels WHERE Dangerous = 0;
DROP TABLE UAVSensors;
DROP TABLE Labels;
CREATE TABLE Labels (Id int(11) AUTO_INCREMENT, Time decimal(16,8), Dangerous int(11), Corrosive int(11), Aruco varchar(200),PRIMARY KEY(Id));
CREATE TABLE UAVSensors (Id int(11) AUTO_INCREMENT, Time decimal(16,8) NOT NULL, Pressure decimal(16,8) NOT NULL, Humidity decimal(16,8) NOT NULL,  Light decimal(16,8) NOT NULL, Temperature decimal(16,8) NOT NULL, Noise_1 decimal(16,8) NOT NULL, Noise_2 decimal(16,8) NOT NULL, Noise_3 decimal(16,8) NOT NULL, Ox_Threshold decimal(16,8) NOT NULL, Red_Threshold decimal(16,8) NOT NULL, Nh3_Threshold decimal(16,8) NOT NULL, Ox decimal(16,8) NOT NULL, Red decimal(16,8) NOT NULL, Nh3 decimal(16,8) NOT NULL,PRIMARY KEY(Id));

