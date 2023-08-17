import sqlite3

# Disini dummy semua sih, buat bukti kalo bisa integrasi ke db aja
def connect_db(dbname: str):
    conn = sqlite3.connect(dbname)
    return conn

def close_db(conn: sqlite3.Connection):
    conn.commit()
    conn.close()

def init_db(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS istri(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    desc TEXT)''')
    
    #Bikin dummy data
    c.execute('SELECT * FROM istri')
    entries = c.fetchone()
    if entries == None:
        c.execute('INSERT INTO istri (name, desc) VALUES (?, ?)', ("Mori Calliope", "Mori Calliope is a captivating VTuber with a unique and engaging personality. As the reaper-themed talent of the group, she often brings a touch of dark humor and a sense of mystery to her content. Calliope is renowned for her deep, resonant voice, which she skillfully uses in various ways, including rap battles and singing performances. She has an undeniable passion for music and often shares her musical talents through karaoke streams and collaborations. Beyond her musical endeavors, Mori Calliope is a friendly and relatable presence, frequently interacting with her fans in a playful and endearing manner."))
        c.execute('INSERT INTO istri (name, desc) VALUES (?, ?)', ("Takahashi Kiara", "Takanashi Kiara, the phoenix-inspired VTuber, is a whirlwind of energy and positivity. Fluent in both English and Japanese, she effortlessly bridges cultural gaps and connects with fans from around the world. Kiara is a skilled singer who often delights her audience with powerful and melodic performances. Her streams are a mix of gaming, language learning, and delightful conversations. With her infectious laughter and bubbly demeanor, Takanashi Kiara brings a ray of sunshine to every interaction, making her a beloved member of the Hololive EN family."))
        c.execute('INSERT INTO istri (name, desc) VALUES (?, ?)', ("Ninomae Ina'nis", "Ninomae Ina'nis exudes a tranquil and artistic aura as the Cthulhu-themed VTuber. With a soothing voice and a penchant for creativity, she frequently hosts drawing and painting sessions, captivating her audience as she brings her visions to life on-screen. Ina'nis is known for her gentle and welcoming presence, making her streams a serene and enjoyable experience. Her content reflects a genuine love for art and an affinity for expressing herself through visual mediums. Through her calm demeanor and artistic pursuits, Ninomae Ina'nis offers a serene escape for her fans."))
        c.execute('INSERT INTO istri (name, desc) VALUES (?, ?)', ("Gawr Gura", "Gawr Gura, the lovable shark-inspired VTuber, has taken the Hololive community by storm with her boundless enthusiasm and adorable charm. Her gaming streams are filled with humor, excitement, and a genuine love for interacting with her fans. Gura's infectious laughter and playful banter create an atmosphere of pure enjoyment, making her streams an irresistible delight. Her endearing personality, combined with her impressive gaming skills and memorable karaoke performances, has earned her a devoted following and a special place in the hearts of viewers worldwide."))
        c.execute('INSERT INTO istri (name, desc) VALUES (?, ?)', ("Amelia Watson", "Watson Amelia is a dynamic VTuber who brings a clever and inquisitive spirit to her detective-themed persona. Her streams are a blend of gaming, interactive mystery-solving, and engaging conversations. With her quick wit and comedic timing, Amelia keeps her audience entertained and engaged. She fearlessly dives into a variety of games and challenges, showcasing her versatile skills and creating memorable content. Watson Amelia's charismatic and entertaining presence makes her streams a captivating experience for fans who are eager to accompany her on her virtual adventures."))
        print("Dummy data inserted")


# bikin dummy data kalo belom ada

