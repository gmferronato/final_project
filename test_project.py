from project import get_name, get_team, get_year, get_country
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

# def test_get_team():
#     assert get_team("Hamburger SV", "2022") == "https://www.transfermarkt.co.uk/hamburger-sv/startseite/verein/41/saison_id/2022"