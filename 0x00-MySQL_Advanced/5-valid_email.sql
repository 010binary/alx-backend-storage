-- Doing Email validation without REGEx
-- A script that creates a trigger that resets the attribute valid_email only.
DELIMITER //
CREATE TRIGGER reset
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
	IF NEW.email != OLD.email THEN
	SET NEW.valid_email = 0;
END IF;
END; //
