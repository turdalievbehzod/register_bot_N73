users = """
CREATE TABLE IF NOT EXISTS users
        (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            phone_number BIGINT NOT NULL,
            age BIGINT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
"""