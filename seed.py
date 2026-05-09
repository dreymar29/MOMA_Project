from MoMA import app
from models import db, Artist, Art, Visitor, InteractionLog, Staff

def isi_database():
    with app.app_context():
        data_artist = [
            {
                "id_artist": "919200001", 
                "name": "Joan Snyder",
                "art": [
                    {"id": "118200001", 
                     "name": "My August",
                     "audio": "0238140001.mp3"}
                ]
            }
        ]

        for item in data_artist:
            artist = Artist.query.get(item["id_artist"])
            if not artist:
                artist = Artist(
                    id=item["id_artist"], 
                    name=item["name"], 
                    biography=item.get("biography", "")
                )
                db.session.add(artist)
                db.session.commit() 

            for art in item["arts"]:
                if not Art.query.get(art["id"]):
                    new_art = Art(
                        id=art["id"], 
                        name=art["name"], 
                        artist_id=artist.id, 
                        description=art["description"],
                        audio_path=art["audio"] 
                    )
                    db.session.add(new_art)
        
        db.session.commit()

        visitors = [
            {"id": "2219200001", "name": "Audrey", "gender": "Female", "pw": "odeyodeyi"}
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
            {"name": "MengAdmin", "password": "123"},
        ]

        for s in staff_data:
            if not Staff.query.filter_by(name=s["name"]).first():
                new_s = Staff(name=s["name"], password=s["password"])
                db.session.add(new_s)

        db.session.commit()

        interaction = [            
            {
                "visitor_name": "Audrey", 
                "art_name": "My August", 
                "artreview": "Karya luar biasa!",
                "museumreview": "Modern dan mudah diakses",
                "rating": 4,
                "audio": True,
                "scan": True
            }
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
                        rating=log.get("rating"),
                        audio_played=log.get("audio"),
                        scanned=log.get("scan")
                    )
                    db.session.add(new_log)

        db.session.commit()
        print("Semua data berhasil di-seed tanpa error!")

if __name__ == "__main__":
    isi_database()