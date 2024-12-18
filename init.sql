-- Create Players table with additional fields for market price and position
CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    nationality VARCHAR(50),
    main_position VARCHAR(50),
    estimated_market_price DECIMAL(15, 2)
);

-- Index on last_name
CREATE INDEX IF NOT EXISTS idx_last_name ON players (last_name);


-- Contracts table with trigger for total salary calculation
CREATE TABLE IF NOT EXISTS contracts (
    player_id INT PRIMARY KEY REFERENCES players(player_id) ON DELETE CASCADE,
    sign_date DATE,
    end_date DATE,
    monthly_salary DECIMAL(15, 2)
);



-- Updated Statistics table, including performance metrics and normalization by total play time
CREATE TABLE IF NOT EXISTS statistics (
    player_id INT PRIMARY KEY REFERENCES players(player_id) ON DELETE CASCADE,
    matches_played INT DEFAULT 0,
    total_play_time INT DEFAULT 0, -- Total play time in minutes
    goals INT DEFAULT 0,
    assists INT DEFAULT 0,
    tackles INT DEFAULT 0,
    saves INT DEFAULT 0,
    yellow_cards INT DEFAULT 0,
    red_cards INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS avg_performance (
    player_id INT PRIMARY KEY REFERENCES players(player_id) ON DELETE CASCADE,
    avg_performance DECIMAL(10, 5) DEFAULT 0
);

CREATE OR REPLACE PROCEDURE delete_by_id(p_player_id INT)
AS $$
BEGIN
    DELETE FROM players WHERE player_id = p_player_id;
END;
$$ LANGUAGE plpgsql;

-- Procedure to update player statistics
CREATE OR REPLACE PROCEDURE update_statistics(
    p_player_id INTEGER,
    p_matches_played INT,
    p_total_play_time INT,
    p_goals INT,
    p_assists INT,
    p_tackles INT,
    p_saves INT,
    p_yellow_cards INT,
    p_red_cards INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if a record exists for the given player_id
    IF EXISTS (SELECT 1 FROM statistics WHERE player_id = p_player_id) THEN
        -- Update current statistics by adding new data
        UPDATE statistics
        SET matches_played = matches_played + p_matches_played,
            total_play_time = total_play_time + p_total_play_time,
            goals = goals + p_goals,
            assists = assists + p_assists,
            tackles = tackles + p_tackles,
            saves = saves + p_saves,
            yellow_cards = yellow_cards + p_yellow_cards,
            red_cards = red_cards + p_red_cards
        WHERE player_id = p_player_id;
    ELSE
        -- Insert a new record if no data exists for the player
        INSERT INTO statistics (
            player_id, matches_played, total_play_time, goals, assists, tackles, saves, yellow_cards, red_cards
        ) VALUES (
            p_player_id, p_matches_played, p_total_play_time, p_goals, p_assists, p_tackles, p_saves, p_yellow_cards, p_red_cards
        );
    END IF;


END;
$$;

CREATE OR REPLACE PROCEDURE update_contract(
    p_player_id INTEGER,
    p_sign_date DATE,
    p_end_date DATE,
    p_monthly_salary DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if a record exists for the given player_id
    IF EXISTS (SELECT 1 FROM contracts WHERE player_id = p_player_id) THEN
        -- Update the existing record
        UPDATE contracts
        SET sign_date = p_sign_date,
            end_date = p_end_date,
            monthly_salary = p_monthly_salary
        WHERE player_id = p_player_id;
    ELSE
        -- Insert a new record
        INSERT INTO contracts (
            player_id, sign_date, end_date, monthly_salary
        ) VALUES (
            p_player_id, p_sign_date, p_end_date, p_monthly_salary
        );
    END IF;
END;
$$;

-- Function to update avg_performance in the avg_performance table
CREATE OR REPLACE FUNCTION update_avg_performance()
RETURNS TRIGGER AS $$
DECLARE
    total_time INT;
    goals_column INT;
    assists_column INT;
    tackles_column INT;
    saves_column INT;
    yellow_cards_column INT;
    red_cards_column INT;
    new_avg_performance DECIMAL(10, 5);
BEGIN

    SELECT s.total_play_time, s.goals, s.assists, s.tackles, s.saves, s.yellow_cards, s.red_cards
    INTO total_time, goals_column, assists_column, tackles_column, saves_column, yellow_cards_column, red_cards_column
    FROM statistics s
    WHERE s.player_id = NEW.player_id;


    IF total_time > 0 THEN
        new_avg_performance :=
            10 * ((goals_column::DECIMAL * 4) + (assists_column::DECIMAL * 3) + (tackles_column::DECIMAL * 2) + (saves_column::DECIMAL * 15) -
                  (yellow_cards_column::DECIMAL * 1) - (red_cards_column::DECIMAL * 2)) / total_time::DECIMAL;
    ELSE
        new_avg_performance := 0;
    END IF;


    INSERT INTO avg_performance (player_id, avg_performance)
    VALUES (NEW.player_id, new_avg_performance)
    ON CONFLICT (player_id)
    DO UPDATE SET avg_performance = EXCLUDED.avg_performance;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



-- Trigger to update avg_performance after INSERT or UPDATE on statistics
CREATE TRIGGER trg_update_avg_performance
AFTER INSERT OR UPDATE ON statistics
FOR EACH ROW EXECUTE FUNCTION update_avg_performance();


-- Function to display the contents of the Players table
CREATE OR REPLACE FUNCTION display_players_contents()
RETURNS TABLE(player_id INT, first_name VARCHAR, last_name VARCHAR, date_of_birth DATE, nationality VARCHAR, main_position VARCHAR, estimated_market_price DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.player_id, p.first_name, p.last_name, p.date_of_birth, p.nationality, p.main_position, p.estimated_market_price
    FROM players p;
END;
$$;

CREATE OR REPLACE FUNCTION display_avg_performance_contents()
RETURNS TABLE(player_id INT, first_name VARCHAR, last_name VARCHAR, avg_performance DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.player_id, p.first_name, p.last_name, a.avg_performance
    FROM avg_performance a
    JOIN players p USING (player_id)
    ORDER BY avg_performance DESC;
END;
$$;


-- Function to display the contents of the Contracts table
CREATE OR REPLACE FUNCTION display_contracts_contents()
RETURNS TABLE(player_id INT, first_name VARCHAR, last_name VARCHAR, sign_date DATE, end_date DATE, monthly_salary DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.player_id, p.first_name, p.last_name, c.sign_date, c.end_date, c.monthly_salary
    FROM contracts c
    JOIN players p USING (player_id);
END;
$$;

-- Function to display the contents of the Statistics table
CREATE OR REPLACE FUNCTION display_statistics_contents()
RETURNS TABLE(player_id INT, first_name VARCHAR, last_name VARCHAR, matches_played INT, total_play_time INT, goals INT, assists INT, tackles INT, saves INT, yellow_cards INT, red_cards INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.player_id, p.first_name, p.last_name, s.matches_played, s.total_play_time, s.goals, s.assists, s.tackles, s.saves, s.yellow_cards, s.red_cards
    FROM statistics s
    JOIN players p USING (player_id);
END;
$$;

-- Procedure to add a new player
CREATE OR REPLACE PROCEDURE add_player(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_date_of_birth DATE,
    p_nationality VARCHAR,
    p_main_position VARCHAR,
    p_estimated_market_price DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO players (first_name, last_name, date_of_birth, nationality, main_position, estimated_market_price)
    VALUES (p_first_name, p_last_name, p_date_of_birth, p_nationality, p_main_position, p_estimated_market_price);
END;
$$;


---- Procedure to clean the contents of any table by truncating and resetting the identity
CREATE OR REPLACE PROCEDURE clean_table(table_name TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('TRUNCATE TABLE %I RESTART IDENTITY CASCADE', table_name);
END;
$$;

-- Procedure to clean all the relevant tables in the schema
CREATE OR REPLACE PROCEDURE clean_all_tables()
LANGUAGE plpgsql
AS $$
BEGIN
    CALL clean_table('players');
    CALL clean_table('avg_performance');
    CALL clean_table('contracts');
    CALL clean_table('statistics');
END;
$$;

-- Procedure to search players by nationality
CREATE OR REPLACE FUNCTION search_by_last_name(last_name_query TEXT)
RETURNS TABLE(player_id INT, first_name VARCHAR, last_name VARCHAR, date_of_birth DATE, nationality VARCHAR, main_position VARCHAR, estimated_market_price DECIMAL,
              matches_played INT, total_play_time INT,  goals INT, assists INT, tackles INT, saves INT, yellow_cards INT, red_cards INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.*, s.matches_played, s.total_play_time, s.goals, s.assists, s.tackles, s.saves, s.yellow_cards, s.red_cards
    FROM players p JOIN statistics s USING (player_id)
    WHERE p.last_name = last_name_query;
END;
$$;

-- Procedure to update player information
CREATE OR REPLACE PROCEDURE update_player(
    p_player_id INTEGER,
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_date_of_birth DATE,
    p_nationality VARCHAR,
    p_main_position VARCHAR,
    p_estimated_market_price DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE players
    SET first_name = p_first_name,
        last_name = p_last_name,
        date_of_birth = p_date_of_birth,
        nationality = p_nationality,
        main_position = p_main_position,
        estimated_market_price = p_estimated_market_price
    WHERE player_id = p_player_id;
END;
$$;

-- Procedure to delete a player by ID
CREATE OR REPLACE PROCEDURE delete_player(p_last_name VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM players WHERE last_name = p_last_name;
END;
$$;

-- Creating a non-root user with privileges
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'team_manager') THEN
        DROP USER team_manager;
    END IF;
END $$;

-- Create the user
CREATE USER team_manager WITH PASSWORD 'password';

-- Grant connect privilege on the database
GRANT CONNECT ON DATABASE football_management TO team_manager;

-- Allow access to the schema
GRANT USAGE ON SCHEMA public TO team_manager;

-- Grant privileges on specific tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO team_manager;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO team_manager;
GRANT TRUNCATE ON ALL TABLES IN SCHEMA public TO team_manager;
ALTER TABLE players OWNER TO team_manager;
ALTER TABLE avg_performance OWNER TO team_manager;
ALTER TABLE contracts OWNER TO team_manager;
ALTER TABLE statistics OWNER TO team_manager;
ALTER SEQUENCE players_player_id_seq OWNER TO team_manager;