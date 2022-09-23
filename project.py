import sys
from PIL import Image
from fpdf import FPDF
import requests
from random import uniform
from time import sleep
import datetime
from bs4 import BeautifulSoup
import re


def main():

    x, y = get_country(input("Country: ").strip().lower())
    global team
    team = get_name(input("Team: ").strip().title())
    global year
    year = get_year(input("Year: ").strip())

    # Set the headers
    global headers
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    # Championship Urls
    global URLS
    URLS = [f"https://www.transfermarkt.com/serie-a/startseite/wettbewerb/{x}", f"https://www.transfermarkt.com/serie-a/startseite/wettbewerb/{y}"]

    squad, logo = get_squad(get_team(team, year))

    get_pdf(squad, logo)
    print("Done!")



def get_team(team, year):


    # Create two lists, one for the team names and the other one for the links
    team_names_list = []
    team_links_list = []

    print("Loading...")

    # Make the first request to the server
    for URL in URLS:
        x = uniform(2, 4)
        sleep(x)
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        team_names = soup.find_all("td", {"class": "hauptlink no-border-links"})
        for team_name in range(len(team_names)):
            team_names_list.append(str(team_names[team_name]).split('title="',1)[1].split('">',1)[0])
        team_links = soup.find_all("td", {"class": "hauptlink no-border-links"})
        for team_link in range(len(team_links)):
            team_links_list.append("https://www.transfermarkt.co.uk"+(str(team_links[team_link]).split('href="',1)[1].split('2022',1)[0])+year+"/")


    # Search for simplified team name in official team names list

    for _ in team_names_list:
        if team in _:
            team = _


    if team not in team_names_list:
        sys.exit("Can't find the team.")

    index = team_names_list.index(team)


    if team in team_names_list:
        URL2 = team_links_list[index]

        print("Compiling data...")
        x = uniform(1,3)
        sleep(x)

        if team == "Brighton &amp; Hove Albion":
            team = "Brighton & Hove Albion"

        return URL2

def get_squad(url):

    # Make the second request to the server
    response2 = requests.get(url, headers=headers)

    soup = BeautifulSoup(response2.content, 'html.parser')

    players_list = []
    positions_list = []

    # Parse the html to obtain the names of the players and their role
    logo = soup.find("div", {"class": "dataBild"})
    players = soup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})
    positions = soup.find_all("td", {"class": ["zentriert rueckennummer bg_Torwart", "zentriert rueckennummer bg_Abwehr", "zentriert rueckennummer bg_Mittelfeld", "zentriert rueckennummer bg_Sturm"]

    } )

    # Clean some things up
    for player in range(len(players)):
        players_list.append(str(players[player]).split('" class',1)[0].split('<img alt="',1)[1])

    for position in range(len(positions)):
        positions_list.append(str(positions[position]).split('title="',1)[1].split('"><',1)[0].capitalize())


    if len(players_list) == 0:
        sys.exit("Sorry, can't find any data")

    team_logo = (str(logo).split('src="',1)[1].split('?lm=',1)[0])

    squad_ = list(zip(players_list, positions_list))

    return squad_, team_logo


def get_country(country):

    countries_allowed = ["italy", "spain", "england", "france", "germany"]
    if country not in countries_allowed:
        sys.exit("Invalid country")

    if country == "spain":
        return "ES1", "ES2"
    elif country == "italy":
        return "IT1", "IT2"
    elif country == "germany":
        return "L1", "L2"
    elif country == "england":
        return "GB1", "GB2"
    elif country == "france":
        return "FR1", "FR2"


def get_name(name):

    matches = re.search(r"^1?\.? ?[0-9a-zA-Z ]+$", name)
    if matches:
        names = name.split()

        # French championships exceptions

        if name.title() in ["Psg", "Paris Saint Germain", "Paris", "Paris Sg"]:
            return f"Paris Saint-Germain"
        elif name.title() in ["Olympique Lyonnais", "Lyon", "Ol"]:
            return "Olympique Lyon"
        elif name.title() in ["Saint Etienne", "As Saint Etienne", "Saint-Etienne", "A.S.S.E."]:
            return "AS Saint-Étienne"
        elif name.title() in ["Sochaux Montbeliard", "Fc Sochaux Montbeliard", "Sochaux"]:
            return "FC Sochaux-Montbéliard"
        elif name.title() in ["Nimes", "Nimes Olympique"]:
            return "Nîmes Olympique"
        elif name.title() in ["Olympique de Marseille", "Om", "Marseille"]:
            return "Olympique Marseille"
        elif name.title() in ["Quevilly", "Us Quevilly", "Us Quevilly-Rouen", "Qrm", "Quevilly-Rouen"]:
            return "Quevilly Rouen Métropole"
        elif name.title() in ["Pau", "Pau Fc"]:
            return "Pau FC"

        # Italian championships exceptions

        elif name.title() == "Spal":
            return name.upper()
        elif name.title() == "Milan":
            return "AC Milan"

        # Spanish championships exceptions

        elif name.title() in ["Atletico", "Atletico De Madrid", "Atletico Madrid", "Atleti"]:
            return "Atlético de Madrid"
        elif name.title() == "Real":
            return "Real Madrid"
        elif name.title() in ["Barcelona", "Barça"]:
            return "FC Barcelona"
        elif name.title() in ["Espanyol", "Espanyol Barcellona", "Español", "Espanyol Barcelona"]:
            return "RCD Espanyol Barcellona"
        elif name.title() in ["Betis", "Real Betis", "Real Betis Balompie"]:
            return "Real Betis Balompié"
        elif name.title() in ["Celta Vigo", "Celta"]:
            return "Celta de Vigo"
        elif name.title() in ["Cadiz", "Cadiz Cf", "Càdiz"]:
            return "Cádiz CF"
        elif name.title() in ["Almeria", "Ud Almeria"]:
            return "UD Almería"
        elif name.title() in ["Sporting Gijon", "Sporting Gijòn", "Gijon", "Gijòn"]:
            return "Sporting Gijón"
        elif name.title() in ["Alaves", "Alavès", "Deportivo Alavès", "Deportivo Alaves"]:
            return "Deportivo Alavés"
        elif name.title() in ["Leganes", "Leganès", "Cd Leganes", "Cd Leganès"]:
            return "CD Leganés"
        elif name.title() in ["Malaga", "Màlaga", "Malaga Cf", "Màlaga Cf"]:
            return "Málaga CF"
        elif name.title() in ["Mirandes", "Mirandès", "Cd Mirandes", "Cd Mirandès"]:
            return "CD Mirandés"
        elif name.title() in ["Albacete", "Albacete Balompie", "Albacete Balompiè"]:
            return "Albacete Balompié"

        # German championships exceptions

        elif name.title() in ["Bayer Leverkusen", "Leverkusen"]:
            return "Bayer 04 Leverkusen"
        elif name.title() in ["Fc Bayern", "Bayern", "Bayern München", "Bayern Munchen"]:
            return "Bayern Munich"
        elif name.title() in ["Koln", "Fc Koln", "1. Fc Koln"]:
            return "1. FC Köln"
        elif name.title() in ["Bvb", "Dortmund", "Borussia"]:
            return "Borussia Dortmund"
        elif name.title() in ["Gladbach", "Mönchengladbach", "Monchengladbach", "Borussia Monchengladbach"]:
            return "Borussia Mönchengladbach"
        elif name.title() == "Werder Bremen":
            return "SV Werder Bremen"
        elif name.title() in ["Greuther Fürth", "Greuther Furth", "Spvgg Greuther Fürth"]:
            return "SpVgg Greuther Fürth"
        elif name.title() in ["Fortuna Dusseldorf", "Dusseldorf"]:
            return "Fortuna Düsseldorf"

        # English championships exceptions

        elif name.title() == "West Ham":
            return "West Ham United"
        elif name.title() in ["Man United", "United"]:
            return "Manchester United"
        elif name.title() in ["Man City", "City"]:
            return "Manchester City"
        elif name.title() in ["Brighton & Hove", "Brighton & Hove Albion"]:
            return "Brighton &amp; Hove Albion"

        # General function


        if len(names) < 1:
            sys.exit("Insert a team")
        if len(names) == 1:
            if len(names[0]) <= 3 or name[0].isdigit() == True:
                sys.exit("Invalid team")
            else:
                return name.title()
        elif len(names) >= 2:
            if len(names[0]) < 2 or len(names[1]) < 1:
                sys.exit("Invalid team")
            if len(names[0]) >= 2 and len(names[0]) <= 3:
                names[0] = names[0].upper()
                if names[0] == "VFB":
                    names[0] = "VfB"
                elif names[0] == "VFL":
                    names[0] = "VfL"
            elif "1." in names[0]:
                        names[0] = names[0].upper()
            elif len(names[0]) > 3:
                if names[0].title() == "Losc" or names[0].title() == "Estac":
                    names[0] = names[0].upper()
                else:
                    names[0] = names[0].title()
            names[1] = names[1].title()
            if len(names[1]) <= 3:
                names[1] = names[1].upper()
            try:
                if len(names) >= 3:
                    if "1." in names[0]:
                        names[0] = names[0].upper()
                    if len(names[1]) >= 3:
                        names[1] = names[1].title()
                    if len(names[1]) <= 2:
                        names[1] = names[1].upper()
                        if names[1] == "DE":
                            names[1] = "de"
                        elif names[1] == "LE":
                            names[1] = "Le"
                if names[2]:
                    if len(names[2]) >= 3:
                        names[2] = names[2].title()
                    elif len(names[2]) <= 2:
                        names[2] = names[2].upper()
                if names[3]:
                    names[3] = names[3].title()
            except:
                pass

            return " ".join(names)

    else:
        sys.exit("Invalid team")

def get_year(year):

    x = datetime.datetime.now()
    current_year = x.year

    if year.isnumeric() == False:
        sys.exit("invalid year")
    elif len(year) <= 3 or int(year) > int(current_year) or int(year) < 1900:
        sys.exit("Invalid year")

    else:
        return year


def get_pdf(squad, logo):

    # Extract dominant color from team logo
    im = Image.open(requests.get(logo, stream=True).raw)
    im = im.convert('RGB')
    colors = im.getcolors(im.size[0]*im.size[1])


    dominant_color = min(colors)
    other_color = max(colors)


    value, RGB_values = dominant_color
    r, g, b = RGB_values

    # Create PDF
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Helvetica")
    pdf.set_font_size(5)
    pdf.set_y(3)
    pdf.cell(0, 10, f"Data from: Transfermarkt.co.uk", align="R")
    pdf.ln(7)

    if logo in ["https://tmssl.akamaized.net/images/wappen/head/1160.png", "https://tmssl.akamaized.net/images/wappen/head/276.png"]:
        pdf.set_fill_color(r=255, g=255, b=255)
        pdf.rect(20, 22, 10, 275, style="F")
        pdf.set_fill_color(r=255, g=255, b=255)
        pdf.rect(20, 15, 210, 10, style="F")

        pdf.image(logo, 10, 1, 30)

        pdf.set_text_color(r=0, g=0, b=0)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 21, f"{team} - {year}", border=0, align="C")
        pdf.ln(20)

    else:
        pdf.set_fill_color(r=r, g=g, b=b)
        pdf.rect(20, 22, 10, 275, style="F")
        pdf.set_fill_color(r=r, g=g, b=b)
        pdf.rect(20, 15, 210, 10, style="F")

        pdf.image(logo, 10, 1, 30)

        pdf.set_text_color(r=255, g=255, b=255)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 21, f"{team} - {year}", border=0, align="C")
        pdf.ln(20)

    line_height = pdf.font_size * 1.5
    col_width = pdf.epw / 3.5

    pdf.ln(10)

    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font("Helvetica", size=10)
    pdf.set_left_margin(pdf.epw / 3.8)
    headers = ("Name", "Position")
    pdf.set_font(style="B")
    for col_name in headers:
        pdf.cell(col_width, line_height, col_name, border=1, align="C")
    pdf.ln(line_height)
    pdf.set_font("Helvetica", size=8)
    pdf.set_font(style="")


    for row in squad:
        for datum in row:
            pdf.cell(col_width, line_height, datum, border=1, align="C")
        pdf.ln(line_height)


    pdf.output(f"{team.lower().replace(' ', '_')}-{year}.pdf")


if __name__ == "__main__":
    main()