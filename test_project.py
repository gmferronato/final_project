from project import get_name, get_team, get_year, get_country, get_squad
import pytest


def test_country():
    assert get_country("italy") == ("IT1", "IT2")
    assert get_country("germany") == ("L1", "L2")
    assert get_country("spain") == ("ES1", "ES2")
    with pytest.raises(SystemExit):
        get_country("poland")
    with pytest.raises(SystemExit):
        get_country("1234")
    with pytest.raises(SystemExit):
        get_country("argentina")
    with pytest.raises(SystemExit):
        get_country("cat")
    with pytest.raises(SystemExit):
        get_country("//123abc")


def test_names():
    assert get_name("juventus fc") == "Juventus FC"
    assert get_name("acf fiorentina") == "ACF Fiorentina"
    assert get_name("spal") == "SPAL"
    assert get_name("united") == "Manchester United"
    with pytest.raises(SystemExit):
        get_name("int")
    with pytest.raises(SystemExit):
        get_name("12343")
    with pytest.raises(SystemExit):
        get_name("//123abc")
    with pytest.raises(SystemExit):
        get_name("mil@n")

def test_year():
    assert get_year("2002") == "2002"
    assert get_year("1984") == "1984"
    assert get_year("1900") == "1900"
    with pytest.raises(SystemExit):
        get_year("12343")
    with pytest.raises(SystemExit):
        get_year("cat")
    with pytest.raises(SystemExit):
        get_year("2023")
    with pytest.raises(SystemExit):
        get_year("404")
    with pytest.raises(SystemExit):
        get_year("20")
    with pytest.raises(SystemExit):
        get_year("3")
    with pytest.raises(SystemExit):
        get_year("1899")
    with pytest.raises(SystemExit):
        get_year("cat")
    with pytest.raises(SystemExit):
        get_year("nineteen ninety four")


def test_get_team():

    assert get_team("L1", "L2", "Hamburger SV", "2022") == "https://www.transfermarkt.co.uk/hamburger-sv/startseite/verein/41/saison_id/2022/"
    assert get_team("GB1", "GB2", "Luton", "2022") == "https://www.transfermarkt.co.uk/luton-town/startseite/verein/1031/saison_id/2022/"
    with pytest.raises(SystemExit):
        get_team("GB1", "GB2", "Inter", "2022")

def test_get_squad():
    roster_monza = [('Luca Leone', 'Goalkeeper'), ('Luca Redaelli', 'Goalkeeper'), ('Luca Righi', 'Goalkeeper'), ('Patrick Moro', 'Defender'), ('Luca Suprani', 'Defender'), ('Manuel Benetti', 'Defender'), ('Cristiano Giaretta', 'Defender'), ('Marco Piccioni', 'Defender'), ('Davide Zoboli', 'Defender'), ('Cristian Maggioni', 'Defender'), ('Nicola Antonellini', 'Midfield'), ('Gianni Margheriti', 'Midfield'), ('Luca Leone', 'Midfield'), ('Mauro Borghetti', 'Midfield'), ('Luca Baldo', 'Midfield'), ('Stefano Pagani', 'Midfield'), ('Adriano Panepinto', 'Midfield'), ('Filippo Pensalfini', 'Midfield'), ('Giuseppe Ticli', 'Midfield'), ('Gabriele Davanzante', 'Attack'), ('Emanuele Cancellato', 'Attack'), ('Matteo Pelatti', 'Attack'), ('Davide Sinigaglia', 'Attack'), ('Pasquale Basilico', 'Attack')]
    roster_albacete = [('Fernando Marcos', 'Goalkeeper'), ('Juan Carlos Balaguer', 'Goalkeeper'), ('Evgeniy Plotnikov', 'Goalkeeper'), ('Coco', 'Defender'), ('José Ortega', 'Defender'), ('Juli Romero', 'Defender'), ('Jose Ángel Moreno', 'Defender'), ('Alejandro', 'Defender'), ('Alejandro Gonzalez Nappi', 'Defender'), ('Albert Tomàs', 'Defender'), ('Petar Vasiljevic', 'Defender'), ('José Carlos Soria', 'Defender'), ('Sotero López', 'Defender'), ('Mario Romero', 'Defender'), ('Juanjo Maqueda', 'Midfield'), ('Chito', 'Midfield'), ('Javi Luke', 'Midfield'), ('Emilio Gutiérrez', 'Midfield'), ('Juan Chesa', 'Midfield'), ('Miguel Ángel Brau', 'Midfield'), ('Josico', 'Midfield'), ('Alberto Monteagudo', 'Midfield'), ('Jesús Muñoz', 'Midfield'), ('Nenad Bjelica', 'Midfield'), ('Manolo Salvador', 'Midfield'), ('José Luis Zalazar', 'Midfield'), ('Paco Luna', 'Attack'), ('Pedro Riesco', 'Attack'), ('José Luis Garzón', 'Attack'), ('Xavier Escaich', 'Attack'), ('Velli Kasumov', 'Attack')]
    roster_psg = [('Luc Borrelli', 'Goalkeeper'), ('Bernard Lama', 'Goalkeeper'), ('Oumar Dieng', 'Defender'), ('Ricardo Gomes', 'Defender'), ('Antoine Kombouaré', 'Defender'), ('Didier Angan', 'Defender'), ('Alain Roche', 'Defender'), ('José Cobos', 'Defender'), ('Didier Domi', 'Defender'), ('Patrick Colleter', 'Defender'), ('Francis Llacer', 'Defender'), ('Christophe Soliveres', 'Midfield'), ('Antonio Tavares', 'Midfield'), ('Pierre Ducrocq', 'Midfield'), ('Paul Le Guen', 'Midfield'), ('Jean-Philippe Séchet', 'Midfield'), ('Daniel Bravo', 'Midfield'), ('Vincent Guérin', 'Midfield'), ('Edvin Murati', 'Midfield'), ('Valdo', 'Midfield'), ('Jérôme Leroy', 'Midfield'), ('Raí', 'Midfield'), ('David Ginola', 'Attack'), ('Bernard Allou', 'Attack'), ('Pascal Nouma', 'Attack'), ("Patrick M'Boma", 'Attack'), ('George Weah', 'Attack')]

    assert get_squad("https://www.transfermarkt.co.uk/ac-monza/startseite/verein/2919/saison_id/2002/") == (roster_monza, "https://tmssl.akamaized.net/images/wappen/head/2919.png")
    assert get_squad("https://www.transfermarkt.co.uk/albacete-balompie/startseite/verein/1532/saison_id/1995/") == (roster_albacete, "https://tmssl.akamaized.net/images/wappen/head/1532.png")
    assert get_squad("https://www.transfermarkt.co.uk/fc-paris-saint-germain/startseite/verein/583/saison_id/1994/") == (roster_psg, "https://tmssl.akamaized.net/images/wappen/head/583.png")
    with pytest.raises(SystemExit):
        get_squad("https://www.transfermarkt.co.uk/ssv-jahn-regensburg/startseite/verein/109/saison_id/1955/")
