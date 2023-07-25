# Presentation

In this presentation, I discuss and conclude my findings on the short-term rental market in New York City. The questions I explore in the presentation are thus:
- Which is the most popular borough in New York?
- What is the most commonly rented property type across the boroughs?
- What is the average price per room type for each borough?
- What is the seasonal demand for short-term rentals within New York, how does this vary across room types?
- Which are the most in-demand neighbourhoods across New York?
- What is the property distribution like across the hosts with the largest total number of properties?
---
## Explaining the findings, question by question

1. **Which is the most popular borough in New York?**  
    To clearly shows this I used a pictogram bar chart with labels above and below to indicate the borough and the number of rentals situated in each. The most popular borough is Brooklyn at 10,460, followed closely by Manhattan at 10,322, there is then an almost 7,000 rental drop to Queens at 3,456. The Bronx comes after with only 697 and Staten Island comes last with 267.
    To find the answer to this question I counted the number of reviews across all the boroughs in the database.

2. **What is the most commonly rented property type across the boroughs?**  
    To answer this question I used another bar graph, this time showing the spread of room types across each borough. Across all the boroughs, the most commonly rented property type was entire houses/apartments and the least popular were shared rooms, leaving private rooms in the middle. If the top two districts, Brooklyn and Manhattan, are ignored then private rooms become the most popular.
   Here I displayed a dual-axis bar chart with little property-type pictograms situated uniformly across the top of the bars; with entire homes/apartments always on the left, private rooms in the middle and shared rooms on the right. The x-axis at the top of the graph shows the borough, also indicated by the colour. The y-axis is the count of the number of listings with the actual number indicated at the bottom of each bar graph.
   I found this result by counting the listing ID per property type by borough.

3. **What is the average price per room type for each borough?**  
    I decided to move away from bar graphs for this next slide and showed bubbles depicting the average price of the different room types across each borough. The average price across all of New York for entire homes/apartments was $197.20, private rooms were $81.70 and for shared rooms were $53.60.
    The largest average price was Manhattan and the lowest pricings were out at Staten Island.

4. **What is the seasonal demand for short-term rentals within New York, how does this vary across room types?**  
    Again I reverted back to a bar chart to show this information clearly. The peak demand occurs in the summer, namely June at around 12,500 bookings and reviews. This is over 7,500 more reviews than the second-highest month of July. The lowest demand is in February were the demand doesn't even reach 1,000. Overlayed on top of this bar chart is a line graph showing what room types this demand consists of.

5. **Which are the most in-demand neighbourhoods across New York?**  
    Taking a deeper dive into the data I decided to look at individual neighbourhoods within the boroughs to see which was the most popular. I used a horizontal bar graph this time ordered by descending popularity. The two most popular neighbourhoods were both in the Brooklyn borough, interestingly Manhattan has a lot more neighbourhoods in the top 10 than Brooklyn.

6. **What is the property distribution like across the hosts with the largest total number of properties?**  
    Finally, I finished the presentation with a table showing a spread of the top hosts on Airbnb in New York City, Pillow Palooza's direct competitors.

---
## Data cleaning

### Prices
- Loaded prices.csv into Python.
- Removed the word 'dollar' in the price column, and changed the values to integers.
- Deleted outliers, prices less than 0 and bigger than $4000.

### Room types
- Loaded room_types.xlsx into Python.
- Formatted data types to strings

### Reviews
- Loaded reviews.tsv into Python.
- Formatted the date column into date type.


## List of the SQL queries used to explore the cleaned data

#### Most popular room type:
```PostgreSQL
Select room_type, COUNT(*) AS number_of_type
FROM room_types
GROUP BY room_type
ORDER BY number_of_type DESC
```
Answer = entire home/apt 13266
***
#### Average price per room type:
```PostgreSQL
Select room_type, COUNT(*) AS number_of_type, AVG(price) AS avg_price
FROM room_types
INNER JOIN prices USING(listing_id)
GROUP BY room_type
ORDER BY number_of_type DESC
```
Answer = home/apt - $197.17, private - $81.67, shared - $53.65
***
#### Highest average price borough:
```PostgreSQL
SELECT borough, AVG(price) AS avg_price
FROM prices
GROUP BY borough
ORDER BY avg_price DESC
```
Answer = Manhattan - $184
***
#### Number of listings for different room types per borough
```PostgreSQL
SELECT borough, room_type, COUNT(*) AS number_of_listings
FROM prices
INNER JOIN room_types USING(listing_id)
GROUP BY room_type, borough
ORDER BY borough, number_of_listings DESC
```
***
#### Number of rooms with prices over $500, by room type
```PostgreSQL
SELECT room_type, COUNT(*) AS prices_over_500
FROM room_types
INNER JOIN prices USING(listing_id)
WHERE price > 500
GROUP BY room_type
ORDER BY prices_over_500 DESC
```
Answer = home/apt - 395, private - 19, shared - 1
***
#### Breakdown of pricings per neighbourhood
```PostgreSQL
SELECT neighbourhood, MIN(price), AVG(price), MAX(price)
FROM prices
GROUP BY neighbourhood
ORDER BY AVG(price) DESC
```
***
#### Total revenue per borough
```PostgreSQL
SELECT borough, SUM(booked_days_365*price) AS total_rev_per_borough
FROM reviews
INNER JOIN prices USING(listing_id)
GROUP BY borough
ORDER BY total_rev_per_borough DESC
```
***
#### Average price per month per neighbourhood
```PostgreSQL
SELECT neighbourhood, AVG(price_per_month) AS avg_price_per_month
FROM prices
GROUP BY neighbourhood
ORDER BY avg_price_per_month DESC
```
***
#### Trying to find missing/duplicate data
```PostgreSQL
SELECT COUNT(DISTINCT room_types.listing_id) AS rooms, 
    COUNT(DISTINCT reviews.listing_id) as reviews,
    COUNT(DISTINCT prices.listing_id) as price
FROM room_types
FULL JOIN reviews USING(listing_id)
FULL JOIN prices USING(listing_id)
```
***
#### Which listings are booked the most
```PostgreSQL
SELECT listing_id, price, price_per_month,  SUM(booked_days_365) AS number_of_booked_days
FROM prices
INNER JOIN reviews USING(listing_id)
GROUP BY listing_id, price, price_per_month
ORDER BY number_of_booked_days DESC
```
***
#### Correlation between the number of booked days per year and the price
```PostgreSQL
SELECT CORR(booked_days_365, price)
FROM prices
INNER JOIN reviews USING(listing_id)
```
***
#### Room types and average price if the property has more than 100 reviews and more than 200 days unbooked
```PostgreSQL
SELECT room_type, AVG(price)
FROM prices
INNER JOIN room_types USING(listing_id)
INNER JOIN reviews USING(listing_id)
GROUP BY room_type
HAVING SUM(number_of_reviews)>100 AND SUM(availability_365)>200
```
