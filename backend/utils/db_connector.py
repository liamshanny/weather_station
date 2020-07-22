import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.pool
from contextlib import contextmanager
import select


class DBConnector:
    def wait(self, conn):
        while 1:
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                break
            elif state == psycopg2.extensions.POLL_WRITE:
                select.select([], [conn.fileno()], [])
            elif state == psycopg2.extensions.POLL_READ:
                select.select([conn.fileno()], [], [])
            else:
                raise psycopg2.OperationalError("poll() returned %s" % state)

    def __init__(self):
        self.db_pool = psycopg2.pool.ThreadedConnectionPool(minconn=1, maxconn=30,
                                                            host='localhost',
                                                            dbname='weather_station',
                                                            user='postgres',
                                                            async_=True)

    def get_conn(self):
        try:
            dbconn = self.db_pool.getconn()
            self.wait(dbconn)
            if dbconn:
                return dbconn, dbconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        except Exception as e:
            raise e

    def put_conn(self, dbconn):
        self.db_pool.putconn(dbconn)

    @contextmanager
    def get_connection(self):
        conn, cur = self.get_conn()
        try:
            yield cur, conn
        except Exception:
            raise
        finally:
            try:
                print(' '.join(str(cur.query.decode('utf-8')).replace('\n', '').split()))
            except AttributeError:
                print(cur.query)
            self.wait(conn)
            self.put_conn(conn)


db = DBConnector()
