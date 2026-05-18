from MoMA import app
from models import db, Artist, Art, Visitor, InteractionLog, Staff

def isi_database():
    with app.app_context():
        # Membuat ulang semua tabel berdasarkan model terbaru
        db.create_all()
        
        data_artist = [
            {
                "id_artist": "919200001", 
                "name": "Joan Snyder",
                "biography": "Born April 16, 1940 in Highland Park, NJ, Joan Snyder received her AB from Douglass College in 1962 and her MFA from Rutgers University in 1966. Snyder has been the recipient of several awards and distinctions, including a National Endowment for the Arts Fellowship in 1974, a John Simon Guggenheim Memorial Fellowship in 1983, a MacArthur Fellowship in 2007 and elected to the American Academy of Arts and Letters in 2026.",
                "photo": "919200001.jpg",
                "art": [
                    {"id": "118200001", 
                     "name": "My August",
                     "description": "2023, Oil and acrylic paint, papier-mâché, straw, flower stems, rosebuds, ink, and paper on linen ; 52 x 72",
                     "audio": "0238140001.mp3",
                     "image": "118200001.jpg"}
                ]
            }
        ]

        for item in data_artist:
            artist = Artist.query.get(item["id_artist"])
            if not artist:
                artist = Artist(
                    id=item["id_artist"], 
                    name=item["name"], 
                    biography=item.get("biography", ""),
                    photo_path=item.get("photo")
                )
                db.session.add(artist)
                db.session.commit() 

            for art in item["art"]:
                if not db.session.get(Art, art["id"]):
                    new_art = Art(
                        id=art["id"], 
                        name=art["name"], 
                        artist_id=artist.id, 
                        description=art["description"],
                        audio_path=art["audio"],
                        image_path=art["image"]
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