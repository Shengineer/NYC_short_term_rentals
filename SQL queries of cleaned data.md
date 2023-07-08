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
