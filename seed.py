from MoMA import app
from models import db, Artist, Art, Visitor, InteractionLog, Staff

def isi_database():
    with app.app_context():
        data_art = [
            {"artist": "Joan Snyder", "art": "My August"},
            {"artist": "Ian Cheng", "art": "3FACE"},
            {"artist": "Louis Fratino", "art": "Fanciullo"},
            {"artist": "Michael Armitage", "art": "Head of Koitalel"},
            {"artist": "Vaginal Davis", "art": "Xochiquetzal, The Precious Feather Flower Goddess of Beauty and Art"}
        ]

        for item in data_art:
            artist = Artist.query.filter_by(name=item["artist"]).first()
            if not artist:
                artist = Artist(name=item["artist"])
                db.session.add(artist)
                db.session.commit()
            
            if not Art.query.filter_by(name=item["art"]).first():
                arts = Art(name=item["art"], artist_id=artist.id)
                db.session.add(arts)

        visitors = [
            {"name": "Dida", "gender": "Female", "job": "Student", "pw": "didadidada"},
            {"name": "Audrey", "gender": "Female", "job": "Student", "pw": "odeyodeydey"},
            {"name": "Egi", "gender": "Female", "job": "Student", "pw": "egiegigi"},
            {"name": "Jihan", "gender": "Female", "job": "Student", "pw": "jihanjiji"},
            {"name": "Tubagus", "gender": "Male", "job": "Student", "pw": "tuthegus"}
        ]

        for v in visitors:
            if not Visitor.query.filter_by(name=v["name"]).first():
                new_v = Visitor(name=v["name"], gender=v["gender"], job=v["job"], password=v["pw"])
                db.session.add(new_v)

        db.session.commit()
        print("Semua data berhasil diinput!")
        
        staff_data = [
            {"username": "admin", "password": "123"},
            {"username": "staff_moma", "password": "123"}
        ]

        for s in staff_data:
            if not Staff.query.filter_by(username=s["username"]).first():
                new_s = Staff(username=s["username"], password=s["password"])
                db.session.add(new_s)

        db.session.commit()
        print("Database berhasil diisi ulang!")

        db.session.commit() 
        interaction = [
            {"visitor": "Dida", "art": "My August", "or": "Scanned", "audio": "Played"},
            {"visitor": "Audrey", "art": "3FACE", "or": "Scanned", "audio": "Played"},
            {"visitor": "Egi", "art": "Fanciullo", "or": "Scanned", "audio": "Played"},
            {"visitor": "Jihan", "art": "Head of Koitalel", "or": "Scanned", "audio": "Played"},
            {"visitor": "Tubagus", "art": "Xochiquetzal, The Precious Feather Flower Goddess of Beauty and Art", "or": "Scanned", "audio": "Played"},
        ]

        for log in interaction:
            v = Visitor.query.filter_by(name=log["visitor"]).first()
            a = Art.query.filter_by(name=log["art"]).first()

            if v and a:
                check_log = InteractionLog.query.filter_by(visitor_id=v.id, art_id=a.id).first()
                
                if not check_log:
                    new_log = InteractionLog(
                        visitor_id=v.id, 
                        art_id=a.id, 
                        or_status=log["or"], 
                        audio_status=log["audio"]
                    )
                    db.session.add(new_log)

        db.session.commit()
        print("Semua data (Visitor & Log) berhasil diinput!")

if __name__ == "__main__":
    isi_database()