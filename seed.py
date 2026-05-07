from MoMA import app
from models import db, Artist, Art, Visitor, InteractionLog, Staff

def isi_database():
    with app.app_context():
        data_art = [
            {"id": "118200001", "artist": "Joan Snyder", "art": "My August"},
            {"id": "118200002", "artist": "Ian Cheng", "art": "3FACE"},
            {"id": "118200003", "artist": "Louis Fratino", "art": "Fanciullo"},
            {"id": "118200004", "artist": "Michael Armitage", "art": "Head of Koitalel"},
            {"id": "118200005", "artist": "Vaginal Davis", "art": "Xochiquetzal, The Precious Feather Flower Goddess of Beauty and Art"}
        ]

        for item in data_art:
            artist = Artist.query.filter_by(name=item["artist"]).first()
            if not artist:
                artist = Artist(name=item["artist"])
                db.session.add(artist)
                db.session.commit()
            
            if not Art.query.get(item["id"]):
                new_art = Art(id=item["id"], name=item["art"], artist_id=artist.id)
                db.session.add(new_art)

        visitors = [
            {"id": "2219200001", "name": "Dida", "gender": "Female", "job": "Student", "pw": "didadidada"},
            {"id": "2219200002", "name": "Audrey", "gender": "Female", "job": "Student", "pw": "odeyodeydey"},
            {"id": "2219200003", "name": "Egi", "gender": "Female", "job": "Student", "pw": "egiegigi"},
            {"id": "2219200004", "name": "Jihan", "gender": "Female", "job": "Student", "pw": "jihanjiji"},
            {"id": "2219200005", "name": "Tubagus", "gender": "Male", "job": "Student", "pw": "tuthegus"}
        ]

        for v in visitors:
            if not Visitor.query.get(v["id"]):
                new_v = Visitor(
                    id=v["id"], 
                    name=v["name"], 
                    gender=v["gender"], 
                    password=v["pw"]
                )
                db.session.add(new_v)

        staff_data = [
            {"name": "admin", "password": "123"},
            {"name": "staff_moma", "password": "123"}
        ]

        for s in staff_data:
            if not Staff.query.filter_by(name=s["name"]).first():
                new_s = Staff(name=s["name"], password=s["password"])
                db.session.add(new_s)

        db.session.commit()
        print("Data Artis, Art, Visitor, dan Staff berhasil dicek/ditambah!")

        interaction = [
            {"visitor_name": "Dida", 
             "art_name": "My August", 
             "artreview": "Luar biasa indahnya!",
             "museumreview": "Museumnya bersih, tapi AC-nya dingin banget.",
             "rating": "5"
             },
            
            {"visitor_name": "Audrey", 
             "art_name": "3FACE", 
             "artreview": "Konsepnya sangat modern dan unik.",
             "museumreview": "Suka banget sama tata letak cahayanya.",
             "rating": "4"
             },
        ]

        for log in interaction:
            v = Visitor.query.filter_by(name=log["visitor_name"]).first()
            a = Art.query.filter_by(name=log["art_name"]).first()

            if v and a:
                check_log = InteractionLog.query.filter_by(visitor_id=v.id, art_id=a.id).first()
                if not check_log:
                    new_log = InteractionLog(
                        visitor_id=v.id, 
                        art_id=a.id, 
                        review_art=log.get("artreview"),
                        review_museum=log.get("museumreview"),
                        rating=log.get("rating")
                    )
                    db.session.add(new_log)

        db.session.commit()
        print("Semua proses seed selesai dengan sukses!")

if __name__ == "__main__":
    isi_database()