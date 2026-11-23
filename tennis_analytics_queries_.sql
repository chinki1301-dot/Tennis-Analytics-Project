CREATE DATABASE tennis_analytics;
USE tennis_analytics;
CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(150) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(50),
    gender VARCHAR(20),
    category_id VARCHAR(50),
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
CREATE TABLE complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id)
        REFERENCES complexes(complex_id)
);
CREATE TABLE competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    country_code VARCHAR(10),
    abbreviation VARCHAR(20)
);
CREATE TABLE competitor_rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    `rank` INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id)
        REFERENCES competitors(competitor_id)
);

USE tennis_analytics;

CREATE USER IF NOT EXISTS 'tennis_user'@'localhost'
IDENTIFIED BY 'Gopesh@5715';

GRANT ALL PRIVILEGES ON tennis_analytics.*
TO 'tennis_user'@'localhost';

SHOW GRANTS FOR 'tennis_user'@'localhost';

USE tennis_analytics;

SELECT COUNT(*) AS total_players
FROM competitors;

SELECT COUNT(*) AS total_rankings
FROM competitor_rankings;

SELECT *
FROM competitors
LIMIT 10;
USE tennis_analytics;

SELECT
    c.name AS player_name,
    c.country,
    cr.`rank`,
    cr.points,
    cr.movement
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
ORDER BY cr.`rank` ASC
LIMIT 10;

SELECT
    c.country,
    COUNT(*) AS total_players,
    ROUND(AVG(cr.points), 2) AS average_points
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
GROUP BY c.country
ORDER BY total_players DESC;

SELECT
    c.name AS player_name,
    c.country,
    cr.points,
    cr.`rank`
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
ORDER BY cr.points DESC
LIMIT 10;

SELECT
    c.name AS player_name,
    c.country,
    cr.`rank`,
    cr.movement,
    cr.points
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE cr.movement > 0
ORDER BY cr.movement DESC
LIMIT 10;

USE tennis_analytics;

ALTER TABLE competitor_rankings
ADD COLUMN tour VARCHAR(10),
ADD COLUMN gender VARCHAR(20),
ADD COLUMN ranking_year INT,
ADD COLUMN ranking_week INT;

USE tennis_analytics;

DESCRIBE competitors;

DESCRIBE competitor_rankings;

USE tennis_analytics;

SELECT
    c.competitor_id,
    c.name AS player_name,
    c.country,
    c.country_code,
    cr.`rank`,
    cr.movement,
    cr.points,
    cr.competitions_played,
    cr.tour,
    cr.gender,
    cr.ranking_year,
    cr.ranking_week
FROM competitors c
INNER JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
LIMIT 10;

SELECT COUNT(*) AS total_competitors
FROM competitors;

SELECT COUNT(*) AS total_rankings
FROM competitor_rankings;

SELECT
    tour,
    COUNT(*) AS total_records
FROM competitor_rankings
GROUP BY tour;

USE tennis_analytics;

DELETE FROM competitor_rankings;

USE tennis_analytics;

SELECT COUNT(*) AS total_competitors
FROM competitors;

SELECT COUNT(*) AS total_rankings
FROM competitor_rankings;

SELECT tour, COUNT(*) AS total_records
FROM competitor_rankings
GROUP BY tour;

USE tennis_analytics;
SHOW TABLES;

DESCRIBE categories;
DESCRIBE competitions;
DESCRIBE complexes;
DESCRIBE venues;
DESCRIBE competitors;
DESCRIBE competitor_rankings;

USE tennis_analytics;

SELECT COUNT(*) AS total_competitions FROM competitions;

SELECT COUNT(*) AS total_venues FROM venues;


USE tennis_analytics;

-- =========================================
-- PART 1: COMPETITION ANALYSIS (7 QUERIES)
-- =========================================

-- 1. All competitions with category name
SELECT c.competition_name, cat.category_name
FROM competitions c
LEFT JOIN categories cat ON c.category_id = cat.category_id;

-- 2. Count competitions in each category
SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions
FROM categories cat
LEFT JOIN competitions c ON cat.category_id = c.category_id
GROUP BY cat.category_name;

-- 3. Find doubles competitions
SELECT *
FROM competitions
WHERE LOWER(type) = 'doubles';

-- 4. Competitions belonging to ITF Men category
SELECT c.*
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

-- 5. Parent competitions and sub-competitions
SELECT p.competition_name AS parent_competition,
       c.competition_name AS sub_competition
FROM competitions c
LEFT JOIN competitions p ON c.parent_id = p.competition_id
WHERE c.parent_id IS NOT NULL;

-- 6. Competition type distribution by category
SELECT cat.category_name, c.type, COUNT(*) AS total
FROM competitions c
LEFT JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type;

-- 7. Top-level competitions
SELECT *
FROM competitions
WHERE parent_id IS NULL;


-- =========================================
-- PART 2: VENUE ANALYSIS (7 QUERIES)
-- =========================================

-- 8. All venues with associated complex name
SELECT v.venue_name, v.city_name, x.complex_name
FROM venues v
JOIN complexes x ON v.complex_id = x.complex_id;

-- 9. Count venues in each complex
SELECT x.complex_name, COUNT(v.venue_id) AS total_venues
FROM complexes x
LEFT JOIN venues v ON x.complex_id = v.complex_id
GROUP BY x.complex_name;

-- 10. Venues in Chile
SELECT *
FROM venues
WHERE country_name = 'Chile';

-- 11. Venues and their timezones
SELECT venue_name, city_name, timezone
FROM venues;

-- 12. Complexes with more than one venue
SELECT x.complex_name, COUNT(v.venue_id) AS total_venues
FROM complexes x
JOIN venues v ON x.complex_id = v.complex_id
GROUP BY x.complex_id, x.complex_name
HAVING COUNT(v.venue_id) > 1;

-- 13. Venues grouped by country
SELECT country_name, COUNT(*) AS total_venues
FROM venues
GROUP BY country_name
ORDER BY total_venues DESC;

-- 14. Venues for a specific complex (Nacional)
SELECT v.*
FROM venues v
JOIN complexes x ON v.complex_id = x.complex_id
WHERE x.complex_name LIKE '%Nacional%';


-- =========================================
-- PART 3: DOUBLES RANKING ANALYSIS (6 QUERIES)
-- =========================================

-- 15. Competitors with rank and points
SELECT c.name, c.country, r.`rank`, r.points
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id;

-- 16. Top 5 competitors
SELECT c.name, c.country, r.`rank`, r.points
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
ORDER BY r.`rank` ASC
LIMIT 5;

-- 17. Competitors with stable ranking
SELECT c.name, r.`rank`, r.movement
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
WHERE r.movement = 0;

-- 18. Total points of competitors from Croatia
SELECT SUM(r.points) AS total_points
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
WHERE c.country = 'Croatia';

-- 19. Count competitors per country
SELECT c.country, COUNT(DISTINCT c.competitor_id) AS total_competitors
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY total_competitors DESC;

-- 20. Competitors with highest points in latest available week
SELECT c.name, c.country, r.points, r.`rank`
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
WHERE (r.ranking_year, r.ranking_week) = (
    SELECT ranking_year, ranking_week
    FROM competitor_rankings
    ORDER BY ranking_year DESC, ranking_week DESC
    LIMIT 1
)
ORDER BY r.points DESC;


SELECT tour, COUNT(*) AS total_rankings
FROM competitor_rankings
GROUP BY tour;