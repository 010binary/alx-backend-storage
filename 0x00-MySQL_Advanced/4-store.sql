-- A script that creates a trigger that decreases the quantity of an items in store
CREATE TRIGGER decrement
AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE NAME = NEW.item_name;
