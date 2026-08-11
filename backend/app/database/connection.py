from neo4j import GraphDatabase

from app.config import settings
class Database:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.cognodb_uri,
            auth=(
                settings.cognodb_username,
                settings.cognodb_password
            )
        )

    def verify_connection(self):
        try:
            with self.driver.session() as session:
                result = session.run(
                    "RETURN 1 AS result"
                )

                record = result.single()

                return record["result"] == 1

        except Exception as error:
            print(f"Database connection failed: {error}")
            return False

    def close(self):
        self.driver.close()


database = Database()