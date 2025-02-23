-- a script that creates a function SafeDiv that divides
DELIMITER //
DROP FUNCTION IF EXISTS `SafeDiv`;
CREATE FUNCTION SafeDiv(
	a INTEGER,
        b INTEGER
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE res FLOAT;
    IF b = 0 THEN
        SET res = 0;
    ELSE
        SET res = (a * 1.0) / b;
    END IF;
	RETURN (res);
END //
DELIMITER;
