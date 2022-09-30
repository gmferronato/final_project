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

    global league_1, league_2, team, year
    league_1, league_2 = get_country(input("Country: ").strip().lower())
    team = get_name(input("Team: ").strip().title())
    year = get_year(input("Year: ").strip())

    squad, logo = get_squad(get_team(league_1, league_2, team, year))

    get_pdf(squad, logo)

    print("Done!")


def get_team(league_1, league_2, team, year):

    """
    This function returns the url of a desired team.
    It parses the html of the championship chosen by the user and creates two lists, one for team names and the other for  related links.
    It then checks to see if the team name is in the list of teams and, if so, returns the correct url of the team with the requested year.
    """

    # Set the header
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    # Championships Urls
    URLS = [f"https://www.transfermarkt.com/serie-a/startseite/wettbewerb/{league_1}", f"https://www.transfermarkt.com/serie-a/startseite/wettbewerb/{league_2}"]

    # Create two lists, one for the team names and the other one for the links
    team_names_list = []
    team_links_list = []

    print("Loading...")

    # Make the first request to the server
    for URL in URLS:
        sec = uniform(1, 2)
        sleep(sec)
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

    # Exit if the name of the team is not in the list.
    if team not in team_names_list:
        sys.exit("Unable to find team.")

    # Pair the team name with the team url
    index = team_names_list.index(team)

    if team in team_names_list:
        URL2 = team_links_list[index]

        print("Compiling data...")

     # Return the team's url
        return URL2

def get_squad(url):

    """
    This function parses the url resulting from the get_team() function and creates two lists containing all the players' names and their positions.
    Using this data, it creates and returns a list of player name/position tuples. Then it extracts and returns the url of the team logo.
    """
    # Make a little pause before the request (to avoid having troubles making too many request to the server in a short amount of time while testing the function)
    sec = uniform(1,2)
    sleep(sec)
    # Make the second request to the server
    response2 = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})

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

    # If the players's list is empty, exit
    if len(players_list) == 0:
        sys.exit("Sorry, unable to find any data.")

    # Parse the html to obtain the team's logo
    team_logo = (str(logo).split('src="',1)[1].split('?lm=',1)[0])

    # Create a list of tuples in which every name of each player is paired to his role within the team
    squad_ = list(zip(players_list, positions_list))

    # return team's squad and logo
    return squad_, team_logo


def get_country(country):

    """
    This function returns the top two leagues of a country entered by the user.
    The only countries allowed are: England, France, Germany, Italy and Spain.
    """

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

    """
    This function returns the name entered by the user.
    The name can contain only letters, numbers, whitespace, and a single dot.
    There are some exceptions that cannot be traced to a pattern and therefore must be made explicit.
    The general function returns the name entered by the user exactly as it is shown on the league page.
    """

    # Create a general, wide range pattern for the team name
    matches = re.search(r"^1?\.? ?\w+? ?\w+?\.?-? ?[0-9a-zA-ZüÉé& ]+$", name)
    if matches:
        names = name.split()

        # French championships exceptions

        if name.title() in ["Psg", "Paris Saint Germain", "Paris", "Paris Sg"]:
            return "Paris Saint-Germain"
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
        elif name.title() in ["St. Pauli", "St Pauli", "Fc St Pauli"]:
            return "FC St. Pauli"

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

    """
    This function returns the year entered by the user.
    The year must consist of four digits only; it cannot go beyond the current year or be earlier than the year 1900.
    """

    x = datetime.datetime.now()
    current_year = x.year

    if year.isnumeric() == False:
        sys.exit("invalid year")
    elif len(year) <= 3 or int(year) > int(current_year) or int(year) < 1900:
        sys.exit("Invalid year")

    else:
        return year


def get_pdf(squad, logo):

    """
    This function produces a formatted pdf containing the lineup of the team in the year in question.
    It contains the team logo, team name and year contained in two lines, and all data about the players and their positions within the team.
    The lines, team name and year take the less dominant color of the team logo as their own color.
    """

    # Extract less dominant color from team logo
    im = Image.open(requests.get(logo, stream=True).raw)
    im = im.convert('RGB')
    colors = im.getcolors(im.size[0]*im.size[1])

    less_dominant_color = min(colors)

    value, RGB_values = less_dominant_color
    r, g, b = RGB_values

    # Extend PDF Class
    class PDF(FPDF):
        def header(self):
            self.ln(15)
            self.image(logo, 6, 4, 30)
            pdf.set_font("Helvetica")
            self.set_font_size(5)
            self.set_y(5)
            self.cell(0, 10, f"Data from: Transfermarkt.co.uk", align="R")
            self.ln(8)


        def footer(self):
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="R")

    # Create PDF
    pdf = PDF()

    pdf.add_page()

    pdf.set_fill_color(r=r, g=g, b=b)
    pdf.rect(45, 18, 185, 1, style="F")
    pdf.set_fill_color(r=r, g=g, b=b)
    pdf.rect(45, 28, 185, 1, style="F")

    pdf.set_text_color(r=r, g=g, b=b)
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