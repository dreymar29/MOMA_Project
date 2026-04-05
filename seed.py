from MoMA import app
from models import db, Artist, Art, Visitor, InteractionLog

def isi_database():
    with app.app_context():
        data_karya = [
            {"artist": "Joan Snyder", "art": "My August"},
            {"artist": "Ian Cheng", "art": "3FACE"},
            {"artist": "Louis Fratino", "art": "Fanciullo"},
            {"artist": "Michael Armitage", "art": "Head of Koitalel"},
            {"artist": "Vaginal Davis", "art": "Xochiquetzal, The Precious Feather Flower Goddess of Beauty and Art"}
        ]

        for item in data_karya:
            artist = Artist.query.filter_by(name=item["artist"]).first()
            if not artist:
                artist = Artist(name=item["artist"])
                db.session.add(artist)
                db.session.commit()
            
            if not Art.query.filter_by(name=item["art"]).first():
                karya = Art(name=item["art"], artist_id=artist.id)
                db.session.add(karya)

        visitors = [
            {"name": "Dida", "gender": "Female", "job": "Student"},
            {"name": "Audrey", "gender": "Female", "job": "Student"},
            {"name": "Egi", "gender": "Female", "job": "Student"},
            {"name": "Jihan", "gender": "Female", "job": "Student"},
            {"name": "Tubagus", "gender": "Male", "job": "Student"}
        ]

        for v in visitors:
            if not Visitor.query.filter_by(name=v["name"]).first():
                new_v = Visitor(name=v["name"], gender=v["gender"], job=v["job"])
                db.session.add(new_v)

        db.session.commit()
        print("Semua data berhasil diinput!")

        db.session.commit() 
        interaksi = [
            {"visitor": "Dida", "art": "My August", "ar": "Scanned", "audio": "Played"},
            {"visitor": "Audrey", "art": "3FACE", "ar": "Scanned", "audio": "Played"},
            {"visitor": "Egi", "art": "Fanciullo", "ar": "Scanned", "audio": "Played"},
            {"visitor": "Jihan", "art": "Head of Koitalel", "ar": "Scanned", "audio": "Played"},
            {"visitor": "Tubagus", "art": "Xochiquetzal, The Precious Feather Flower Goddess of Beauty and Art", "ar": "Scanned", "audio": "Played"},
        ]

        for log in interaksi:
            v = Visitor.query.filter_by(name=log["visitor"]).first()
            a = Art.query.filter_by(name=log["art"]).first()

            if v and a:
                cek_log = InteractionLog.query.filter_by(visitor_id=v.id, art_id=a.id).first()
                
                if not cek_log:
                    new_log = InteractionLog(
                        visitor_id=v.id, 
                        art_id=a.id, 
                        ar_status=log["ar"], 
                        audio_status=log["audio"]
                    )
                    db.session.add(new_log)

        db.session.commit()
        print("Semua data (Visitor & Log) berhasil diinput!")

if __name__ == "__main__":
    isi_database()