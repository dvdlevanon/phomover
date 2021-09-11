import threading
import sqlite3

class Database:
	def __init__(self, db_file):
		self.db_file = db_file
		self.connection = threading.local()
		self.make_sure_table_exists()
	
	def get_connection(self):
		try:
			return self.connection.value
		except AttributeError as e:
			self.connection.value = sqlite3.connect(self.db_file)
			return self.connection.value

	def make_sure_table_exists(self):
		cur = self.get_connection().cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS photos (
				id TEXT NOT NULL PRIMARY KEY, 
				path TEXT, 
				x INTEGER, 
				y INTEGER, 
				fingerprint TEXT)
		""")
		self.get_connection().commit()
	
	def get_photos_count(self):
		cur = self.get_connection().cursor()
		cur.execute("SELECT COUNT(*) FROM photos")
		return int(cur.fetchone()[0])
	
	def save_new(self, photo):
		cur = self.get_connection().cursor()
		cur.execute("""
			INSERT OR IGNORE INTO photos (id, path) values (?, ?)
		""", (photo.get_id(), photo.file))
		self.get_connection().commit()
	
	def get_photos_without_fingerprint(self):
		cur = self.get_connection().cursor()
		cur.execute("SELECT path FROM photos WHERE fingerprint is NULL")
		return cur.fetchall()
	
	def update_photos(self, photos):
		cur = self.get_connection().cursor()
		
		for photo in photos:
			cur.execute("""
				UPDATE photos SET
					x=?,
					y=?,
					fingerprint=?
				WHERE
					id=?
			""", (photo.resolution_x, photo.resolution_y, photo.fingerprint, photo.get_id()))

		self.get_connection().commit()
