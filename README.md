# Who played in that team?
#### Video Demo:  <https://www.youtube.com/watch?v=FWDvWDkMYok>
<br></br>
### **General description**:

This program allows the user to search for a specific roster of a certain team in a certain year, and prints out a pdf containing all the players names, their position within the team and the team logo.
<br></br>

### **The main() function:**

The main() function handles the structure of the program. It prompts the user for a country league, a team and a year. These values serve then as arguments for the get_team() function, which returns an url that, itself, serves as an argument for the get_squad() function.
This function returns two variables: the roster of the team in the specific year (under the form of a list of tuples) and the team logo.

These two return values serve as arguments for the get_pdf() function, which, as the name suggests, produces a pdf in which all the data are formatted and displayed correctly.
<br></br>

### **The get_country() function:**
This function prompts the user to enter a country and provides the two main leagues of that country in return.
The only countries allowed are: England, France, Germany, Italy and Spain.
<br></br>
### **The get_name() function:**
This function returns the team name entered by the user.

The regular expression at the beginning performs an initial skimming by allowing only names containing letters, numbers, whitespace, a single dot, and, among special characters, only "&" and "-".

If the name passes this first stage, it goes through a list of exceptions, because some team names cannot be traced back to a pattern and/or the user might search for a team using an informal name (e.g., "PSG" instead of "Paris Saint-Germain" or "Atleti" instead of "Atlético de Madrid").

The third stage of this function is the "general function," which accepts any valid name entered by the user and produces the exact name contained in the given national league url, so that the two (the one entered by the user and the one in the url) match exactly.
(For example, if the user enters, all in lower case, "juventus fc," the function will produce "Juventus FC," or if the team entered is "fc empoli," the result will be "FC Empoli."
<br></br>
### **The get_year() function:**
This function validates the year entered by the user and it returns it.
The year must consist of four digits only; it cannot go beyond the current year or be earlier than the year 1900.
I used the now() method from the datetime module to avoid hardcoding manually the current year.
<br></br>
### **The get_team() function:**
This function returns the url of the desired team roster in a desired year.

After setting the headers and completing the "URLs" with the chosen leagues suffixes, the function creates two lists, one for team names and the other for team links.

Using a for loop to iterate over the two league urls and using the "sleep" method (from the time module) to pause between the two iterations, the function uses the "request" module to make a request to the two URLs. It then parses the html for each using the BeautifulSoup library, cleans some things up, and adds to the two previously created lists the respective elements.

It then searches if, in the list of team names just compiled, there is a match with the team name entered by the user. If not, the program exits showing the message "Unable to find team." On the contrary, it pairs the team name in the list with the corresponding link in the other list using an "index" variable (which takes the index position of the team name in the list and applies the resulting value to the index position of the team link).
Finally the function returns the desired url.
<br></br>
### **The get_squad() function:**
This function,, after another little pause using the sleep module,  makes a request to the url resulting from the get_team() function and creates two lists, one for the players' names and one for their positions within the team.
After making the request it parses the html code and appends the data to the two previously created lists.
If the list of players is somehow empty the program exits showing the following message: "Sorry, unable to find any data."
It then cleans up the html to extract the team logo from the url and finally creates a list of tuples that match each player's name to his position.
These two results (the team logo url and the list of player name/position tuples) are returned.
<br></br>
### **The get_pdf() function:**
This function produces an A4 formatted pdf containing the team's roster in the year in question.

It first extracts from the team logo its least dominant color (using the getcolor() method from the PIL library) and stores it as RGB values.
It then extends the PDF class by setting the header() and footer() functions.
The header() function contains the team logo, positioned at the top left of the page and the text "data from: Transfermarkt.co.uk" positioned at the top right.
The footer() function, on the other hand, contains the number of the current page versus the number of total pages.

The function then initializes the pdf object, adds a page to it, and creates two horizontal lines within which the team name and team year are contained.
The color of these lines is derived from the less dominant color of the team logo, as is that of the text within them.
Then it creates a two-column table containing the players' names (in the left column) and their position within the team in the right column.

Finally, it outputs a pdf file with the team name and year entered by the user as the file name.

<br></br>

Gian Marco Ferronato - 2022