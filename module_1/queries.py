# All queries used
SELECT_ALL = 'SELECT character_id, name FROM charactercreator_character;'

AVG_ITEM_WEIGHT_PER_CHARACTER = '''
SELECT cc_char.name, AVG(ai.weight) AS avg_item_weight
FROM charactercreator_character AS cc_char
JOIN charactercreator_character_inventory AS cc_inv
ON cc_char.character_id == cc_inv.character_id
JOIN armory_item AS ai
ON ai.item_id = cc_inv.item_id
GROUP BY cc_char.character_id;
'''

# Part 1

TOTAL_CHARACTERS = '''
SELECT COUNT(*) AS TOTAL_CHARACTERS
FROM charactercreator_character;
'''

TOTAL_SUBCLASS = '''
SELECT COUNT(*) AS TOTAL_SUBCLASS
FROM charactercreator_necromancer;
'''

TOTAL_ITEMS = '''
SELECT COUNT(*) AS TOTAL_ITEMS
FROM armory_item;
'''

WEAPONS = '''
SELECT COUNT(*) AS WEAPONS
FROM armory_weapon;
'''

NON_WEAPONS = '''
SELECT COUNT(*) AS NON_WEAPON
FROM armory_item
LEFT JOIN armory_weapon
ON armory_item.item_id = armory_weapon.item_ptr_id
WHERE armory_weapon.item_ptr_id IS NULL;
'''

CHARACTER_ITEMS = '''
SELECT COUNT(*) AS CHARACTER_ITEMS
FROM charactercreator_character AS cc_c
JOIN charactercreator_character_inventory AS cc_c_i
ON cc_c.character_id = cc_c_i.character_id
GROUP BY cc_c.character_id
LIMIT 20;
'''

CHARACTER_WEAPONS = '''
SELECT COUNT(*) AS CHARACTER_WEAPONS
FROM charactercreator_character as cc_c
JOIN charactercreator_character_inventory as cc_c_i
ON cc_c.character_id = cc_c_i.character_id
JOIN armory_weapon as a_w
ON cc_c_i.item_id = a_w.item_ptr_id
GROUP BY cc_c.character_id
LIMIT 20;
'''

AVG_CHARACTER_ITEMS = '''
SELECT AVG(CHARACTER_ITEMS) AS AVG_CHARACTER_ITEMS
FROM (
    SELECT COUNT(*) AS CHARACTER_ITEMS
    FROM charactercreator_character AS cc_c
    JOIN charactercreator_character_inventory AS cc_c_i
    ON cc_c.character_id = cc_c_i.character_id
    GROUP BY cc_c.character_id;
    );
'''

AVG_CHARACTER_WEAPONS = '''
SELECT AVG(CHARACTER_WEAPONS) AS AVG_CHARACTER_WEAPONS
FROM (
    SELECT COUNT(*) AS CHARACTER_WEAPONS
    FROM charactercreator_character as cc_c
    JOIN charactercreator_character_inventory as cc_c_i
    ON cc_c.character_id = cc_c_i.character_id
    JOIN armory_weapon as a_w
    ON cc_c_i.item_id = a_w.item_ptr_id
    GROUP BY cc_c.character_id;
    );
'''

# Part 2

COUNT = '''
SELECT COUNT(*) AS COUNT
FROM BuddyMove;
'''

COUNT_NATURE_SHOPPING_100 = '''
SELECT COUNT(*)
FROM BuddyMove
WHERE Nature >= 100 AND Shopping >= 100;
'''

AVG_CATEGORIES = '''
SELECT AVG(Sports), AVG(Religious), AVG(Nature),
AVG(Theatre), AVG(Shopping), AVG(Picnic)
FROM BuddyMove;
'''
