from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.api_calls import check_user, fetch_post, fetch_posts, NewPost, add_post, add_user, add_comment
from pydantic import ValidationError

app = Flask(__name__)
app.secret_key = "asdsadsadkj"
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
        "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202209/2812/ev8VaiyRc42X3QgRwHIJ2b5r.jpg"
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


@app.context_processor
def inject_user_info():
    if session.get("login", None):
        print("cokolwiek")
        return dict(curr_user=session['login'])

    return dict(curr_user=None)



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

@app.route("/forum")
def forum():
    posts = fetch_posts()
    game_id = request.args.get("game_id", type=int)
    games = mock_games
    use_filter = request.args.get("use_filter") == "on"
    if use_filter and game_id:
        posts = [p for p in posts if p.game and p.game.id == game_id]

    return render_template(
        "forum.html",
        posts=posts,
        games=games,
        selected_game=game_id,
        use_filter=use_filter
    )

@app.route("/forum/<int:post_id>")
def post_detail(post_id):
    post = fetch_post(post_id)
    return render_template("post_detail.html", post=post)

@app.route("/forum/<int:post_id>/", methods=["POST"])
def post_comment(post_id):
    data = request.form.to_dict()
    add_comment(post_id, data['body'], session['login'])
    return redirect(url_for("post_detail", post_id=post_id))



@app.route("/forum/new", methods=["POST", "GET"])
def new_post():
    games = mock_games

    if request.method == "POST":
            form_data = request.form.to_dict()
            try:
                post_data = NewPost(**form_data)
                add_post(post_data)
            except ValidationError as e:
                flash("❌ Błąd walidacji: " + str(e), "error")
                return render_template("post_form.html", form=form_data)

            return redirect(url_for("forum"))

    return render_template("post_form.html", games=games)


@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form.to_dict()
        username = data['username']
        pwd = data['pwd']
        repeated_pwd = data['repeated-pwd']
        if pwd != repeated_pwd:
            flash("Hasła nie sa takie same", "error")
            return
        elif not check_user(username, pwd):
            add_user(username, pwd)
            print("cos")
            flash("Udało się zarejestrować", "success")
            return redirect(url_for("login"))
        else:
            flash("Użytkownik istnieje lool", "error")


    return render_template('register.html')


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form.to_dict()
        username = data['username']
        password = data['password']
        if check_user(username, password):
            flash("Udało się zalogować", "success")
            session['login'] = username
            return redirect("/")
        else:
            flash("Błedne dane logownia", "error")
    return render_template('login.html')

@app.route("/auth/logout")
def logout():
    session.pop("login", None)
    flash("Wylogowano", "success")
    return redirect("/")