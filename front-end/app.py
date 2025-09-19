from flask import Flask, render_template, request, redirect, url_for, flash
from utils.api_calls import check_user
app = Flask(__name__)

mock_games = [
    {
        "id": 1,
        "title": "Catan",
        "author": "Klaus Teuber",
        "players": "3-4",
        "playtime": 60,
        "short_description": "Buduj osady, handluj surowcami i rywalizuj o dominację na wyspie Catan.",
        "description": "Catan to strategiczna gra ekonomiczna, w której gracze kolonizują nową wyspę, budując drogi i miasta. Surowce pozyskiwane są w zależności od rzutów kostką, a kluczowym elementem jest handel między graczami.",
        "rules_short": "Rzucasz kostkami, zbierasz surowce, wymieniasz się i budujesz.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/2/2d/Catan-2015-boxart.jpg"
    },
    {
        "id": 2,
        "title": "Carcassonne",
        "author": "Klaus-Jürgen Wrede",
        "players": "2-5",
        "playtime": 35,
        "short_description": "Układaj kafelki i buduj średniowieczne miasto Carcassonne.",
        "description": "Carcassonne to gra kafelkowa, w której gracze dokładają płytki, tworząc krajobraz średniowiecznej Francji. Rozmieszczają swoich meepli, aby zdobywać punkty za miasta, drogi i klasztory.",
        "rules_short": "Dobierasz płytkę, dokładasz do planszy, opcjonalnie stawiasz meepla i punktujesz.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/4/46/Carcassonne-game.jpg"
    },
    {
        "id": 3,
        "title": "Dixit",
        "author": "Jean-Louis Roubira",
        "players": "3-6",
        "playtime": 30,
        "short_description": "Gra skojarzeń i wyobraźni z pięknymi ilustracjami.",
        "description": "Dixit to gra, w której gracze starają się odgadnąć, która z kart została opisana przez narratora. Karty zawierają surrealistyczne ilustracje, które można interpretować na wiele sposobów.",
        "rules_short": "Narrator wybiera kartę i hasło, reszta graczy podkłada swoje karty i głosuje.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/7/7d/Dixit_gameplay.jpg"
    },
    {
        "id": 4,
        "title": "Ticket to Ride",
        "author": "Alan R. Moon",
        "players": "2-5",
        "playtime": 45,
        "short_description": "Buduj linie kolejowe i rywalizuj o trasy przez Amerykę.",
        "description": "Gracze kolekcjonują karty wagonów, by budować połączenia kolejowe pomiędzy miastami. Celem jest realizacja tajnych tras oraz zdobywanie punktów za długie linie kolejowe.",
        "rules_short": "Dobierasz karty wagonów, budujesz trasy, realizujesz bilety.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/5/5b/Ticket_to_Ride_Board_Game_Box_EN.jpg"
    },
    {
        "id": 5,
        "title": "7 Cudów Świata",
        "author": "Antoine Bauza",
        "players": "3-7",
        "playtime": 40,
        "short_description": "Rozwijaj cywilizację i buduj cud świata w grze karcianej.",
        "description": "Gracze prowadzą swoje cywilizacje przez trzy epoki, wybierając karty reprezentujące budynki, naukę, wojsko i handel. Każdy rozwija własne miasto, a jednocześnie buduje swój cud świata.",
        "rules_short": "Draftujesz karty, budujesz struktury, punktujesz na koniec gry.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/7/7f/7_Wonders_%28board_game%29_box_cover.jpg"
    }
]



@app.route("/game/<int:game_id>")
def game_detail(game_id):
    game = next((g for g in mock_games if g["id"] == game_id), None)
    return render_template("game_detail.html", game=game)


@app.route("/game/add", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        new_game = {
            "id": len(mock_games) + 1,
            "title": request.form["title"],
            "owner": request.form.get("owner", ""),
            "players": request.form.get("players", ""),
            "playtime": request.form.get("playtime", ""),
            "short_description": request.form.get("short_description", ""),
            "description": request.form.get("description", ""),
            "rules_short": request.form.get("rules_short", ""),
            "image_url": request.form.get("image_url", "")
        }
        mock_games.append(new_game)
        return redirect(url_for("index"))
    return render_template("add_game.html")


@app.route("/")
def index():
    games = mock_games
    return render_template('index.html', games=games)


@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        pwd = data['password']
        repeated_pwd = data['repeated-pwd']
        if pwd != repeated_pwd:
            flash("Hasła nie sa takie same", "error")
        elif check_user(username, pwd):
            flash("Udało się zarejestrować", "success")
            return render_template("login.html")
        else:
            flash("Błedne dane logownia", "error")



    return render_template('register.html')


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        password = data['password']
        if check_user(username, password):
            flash("Udało się zalogować", "success")
            return render_template("index.html")
        else:
            flash("Błedne dane logownia", "error")

    return render_template('login.html')
