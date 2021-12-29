/*
SQL PRACTICE, ARTICLE "How to Use the SQL GROUP BY Clause and Aggregate Functions" BY TERENCE SHIN 
(https://towardsdatascience.com/how-to-use-the-sql-group-by-clause-and-aggregate-functions-cbaef410be91)
*/

/*displaying the whole table*/
SELECT * 
FROM albums;

/*showing the total count of artists listed, and the number of unique artist names*/
SELECT COUNT(DISTINCT artist) AS 'unique artists',
	COUNT(artist) AS 'total artists'
FROM albums;

/*trying to show count for albumbs with 1980 release date; ERROR: "execute command denied to user 'hopper_1546'@'%' for routine 'albums_db.COUNTIF'"*/
SELECT COUNTIF(release_date = 1980)  AS count
FROM albums;

/*taking the sum of total album sales*/
SELECT SUM(sales)
FROM albums;

/*total sales by genre*/
SELECT genre, SUM(sales) AS sales_by_genre
FROM albums
GROUP BY genre;

/*avergae sales by genre*/
SELECT genre, AVG(sales) AS avg_sales_by_genre
FROM albums
GROUP BY genre;

/*average release date and sales*/
SELECT AVG(release_date) AS avg_release_date,
	AVG(sales) AS avg_sales
FROM albums;

/*average sales by release year*/
SELECT release_date, AVG(sales) AS sales_by_release_date
FROM albums
GROUP BY release_date;

